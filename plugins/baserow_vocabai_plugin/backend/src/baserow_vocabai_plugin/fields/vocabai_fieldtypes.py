from django.db import models
from django.core.exceptions import ValidationError
from baserow.contrib.database.fields.field_cache import FieldCache

from rest_framework import serializers

from baserow.contrib.database.fields.registries import FieldType
from baserow.contrib.database.fields.models import Field
from baserow.contrib.database.views.handler import ViewHandler

from baserow.contrib.database.fields.dependencies.models import FieldDependency

from baserow.core.models import GROUP_USER_PERMISSION_ADMIN, GroupUser

from .vocabai_models import TranslationField, TransliterationField, LanguageField, DictionaryLookupField, ChineseRomanizationField, CHOICE_PINYIN, CHOICE_JYUTPING

from ..cloudlanguagetools.tasks import run_clt_translation_all_rows, run_clt_transliteration_all_rows, run_clt_lookup_all_rows
from ..cloudlanguagetools import clt_interface

import logging
logger = logging.getLogger(__name__)

# see https://community.baserow.io/t/anonymous-api-access-or-universal-token/788/18 for background
# the idea suggested by Nigel was to enhance Update Collector to run the lambdas at the end, at the right time
# however this will require a baserow update, and it's more complicated to do when this code is running as a baserow plugin.
USE_ENHANCED_UPDATE_COLLECTOR = False

class LanguageTextField(models.TextField):
    pass

class LanguageFieldType(FieldType):
    type = "language_text"
    model_class = LanguageField
    allowed_fields = ["language"]
    serializer_field_names = ["language"]

    def get_serializer_field(self, instance, **kwargs):
        required = kwargs.get("required", False)
        return serializers.CharField(
            **{
                "required": required,
                "allow_null": not required,
                "allow_blank": not required,
                "default": None,
                **kwargs,
            }
        )

    def get_model_field(self, instance, **kwargs):
        return LanguageTextField(
            default='', blank=True, null=True, **kwargs
        )


class TranslationTextField(models.TextField):
    requires_refresh_after_update = True


class TransformationFieldType(FieldType):
    def get_field_dependencies(self, field_instance: Field, field_lookup_cache: FieldCache):
        # logger.info(f'get_field_dependencies')
        if field_instance.source_field != None:
            return [
                FieldDependency(
                    dependency=field_instance.source_field,
                    dependant=field_instance
                )
            ]     
        return []    

    def after_create(self, field, model, user, connection, before, field_kwargs):
        self.update_all_rows(field)

    def after_update(
        self,
        from_field,
        to_field,
        from_model,
        to_model,
        user,
        connection,
        altered_column,
        before,
        to_field_kwargs
    ):
        self.update_all_rows(to_field)        

    def get_transformed_value(self, field, source_value, usage_user_id):
        if source_value == None or len(source_value) == 0:
            return ''
        transformed_value = self.transform_value(field, source_value, usage_user_id)
        return transformed_value

    def get_usage_user_id(self, field):
        """get the user_id that this usage will be associated with"""

        # find the admin in the group
        group = field.table.database.group

        admin_users = GroupUser.objects.filter(group_id=group.id, permissions=GROUP_USER_PERMISSION_ADMIN)
        for admin_user in admin_users:
            logger.info(f'admin_user: {admin_user.user}')
            return admin_user.user.id

        logger.error(f'admin user not found in group {group} group.id: {group.id}')
        return None

    def process_transformation(self, field, starting_row):
        source_internal_field_name = f'field_{field.source_field.id}'
        target_internal_field_name = f'field_{field.id}'

        if isinstance(starting_row, list):
            row_list = starting_row
        else:
            row_list = [starting_row]

        rows_to_bulk_update = []
        for row in row_list:
            source_value = getattr(row, source_internal_field_name)
            transformed_value = self.get_transformed_value(field, source_value, self.get_usage_user_id(field))
            setattr(row, target_internal_field_name, transformed_value)
            rows_to_bulk_update.append(row)

        model = field.table.get_model()
        model.objects.bulk_update(rows_to_bulk_update, fields=[field.db_column])


    def row_of_dependency_deleted(
        self,
        field,
        starting_row,
        update_collector,
        field_cache,
        via_path_to_starting_table):
        # don't do anything
        pass

    def row_of_dependency_moved(
        self,
        field,
        starting_row,
        update_collector,
        field_cache,
        via_path_to_starting_table):    
        # don't do anything
        pass

class TranslationFieldType(TransformationFieldType):
    type = "translation"
    model_class = TranslationField
    allowed_fields = [
        'source_field_id',
        'target_language',
        'service'
    ]
    serializer_field_names = [
        'source_field_id',
        'target_language',
        'service'
    ]
    serializer_field_overrides = {
        "source_field_id": serializers.IntegerField(
            required=False,
            allow_null=True,
            source="source_field.id",
            help_text="The id of the field to translate",
        ),
        "target_language": serializers.CharField(
            required=True,
            allow_null=False,
            allow_blank=False
        ),
        'service': serializers.CharField(
            required=True,
            allow_null=False,
            allow_blank=False
        )
    }

    can_be_primary_field = False

    def prepare_value_for_db(self, instance, value):
        return value

    def get_serializer_field(self, instance, **kwargs):
        return serializers.CharField(
            **{
                "required": False,
                "allow_null": True,
                "allow_blank": True,
                **kwargs,
            }        
        )

    def get_model_field(self, instance, **kwargs):
        return TranslationTextField(
            default=None,
            blank=True, 
            null=True, 
            **kwargs
        )


    def transform_value(self, field, source_value, usage_user_id):
        source_language = field.source_field.language  
        target_language = field.target_language
        translation_service = field.service
        if source_value == None or len(source_value) == 0:
            return ''
        translated_text = clt_interface.get_translation(source_value, source_language, target_language, translation_service, usage_user_id)
        return translated_text

    def row_of_dependency_updated(
        self,
        field,
        starting_row,
        update_collector,
        field_cache: "FieldCache",
        via_path_to_starting_table,
    ):

        if USE_ENHANCED_UPDATE_COLLECTOR:
            # as per nigel, it's preferrable to use the update collector to do the update at the end
            def translate_rows(rows):
                source_language = field.source_field.language  
                target_language = field.target_language
                translation_service = field.service          
                source_internal_field_name = f'field_{field.source_field.id}'
                target_internal_field_name = f'field_{field.id}'
                for row in rows:
                    text = getattr(row, source_internal_field_name)
                    if text != None:
                        translated_text = clt_interface.get_translation(text, source_language, target_language, translation_service)
                        setattr(row, target_internal_field_name, translated_text)

            update_collector.add_field_with_pending_update_function(
                field,
                update_function=translate_rows,
                via_path_to_starting_table=via_path_to_starting_table,
            )       
        else:
            self.process_transformation(field, starting_row)

        ViewHandler().field_value_updated(field)     

        super().row_of_dependency_updated(
            field,
            starting_row,
            update_collector,
            field_cache,
            via_path_to_starting_table,
        )        


    def update_all_rows(self, field):
        logger.info(f'update_all_rows')
        source_field_language = field.source_field.language
        target_language = field.target_language
        translation_service = field.service          
        source_field_id = f'field_{field.source_field.id}'
        target_field_id = f'field_{field.id}'

        table_id = field.table.id

        logger.info(f'after_update table_id: {table_id} source_field_id: {source_field_id} target_field_id: {target_field_id}')

        run_clt_translation_all_rows.delay(table_id, 
                                           source_field_language, 
                                           target_language,
                                           translation_service,
                                           source_field_id, 
                                           target_field_id,
                                           self.get_usage_user_id(field))


class TransliterationFieldType(TransformationFieldType):
    type = "transliteration"
    model_class = TransliterationField
    allowed_fields = [
        'source_field_id',
        'transliteration_id'
    ]
    serializer_field_names = [
        'source_field_id',
        'transliteration_id'
    ]
    serializer_field_overrides = {
        "source_field_id": serializers.IntegerField(
            required=False,
            allow_null=True,
            source="source_field.id",
            help_text="The id of the field to translate",
        ),
        "transliteration_id": serializers.CharField(
            required=True,
            allow_null=False,
            allow_blank=False
        ),
    }

    can_be_primary_field = False

    def prepare_value_for_db(self, instance, value):
        return value

    def get_serializer_field(self, instance, **kwargs):
        return serializers.CharField(
            **{
                "required": False,
                "allow_null": True,
                "allow_blank": True,
                **kwargs,
            }        
        )

    def get_model_field(self, instance, **kwargs):
        return TranslationTextField(
            default=None,
            blank=True, 
            null=True, 
            **kwargs
        )

    def transform_value(self, field, source_value, usage_user_id):
        transliteration_id = field.transliteration_id
        transliterated_text = clt_interface.get_transliteration(source_value, transliteration_id, usage_user_id)
        return transliterated_text

    def row_of_dependency_updated(
        self,
        field,
        starting_row,
        update_collector,
        field_cache: "FieldCache",
        via_path_to_starting_table,
    ):


        if USE_ENHANCED_UPDATE_COLLECTOR:

            def transliterate_rows(rows):
                transliteration_id = field.transliteration_id
                source_internal_field_name = f'field_{field.source_field.id}'
                target_internal_field_name = f'field_{field.id}'
                for row in rows:
                    text = getattr(row, source_internal_field_name)
                    if text != None:
                        transliterated_text = clt_interface.get_transliteration(text, transliteration_id)
                        setattr(row, target_internal_field_name, transliterated_text)

            update_collector.add_field_with_pending_update_function(
                field,
                update_function=transliterate_rows,
                via_path_to_starting_table=via_path_to_starting_table,
            )       

        else:
            self.process_transformation(field, starting_row)

        ViewHandler().field_value_updated(field)     

        super().row_of_dependency_updated(
            field,
            starting_row,
            update_collector,
            field_cache,
            via_path_to_starting_table,
        )        


    def update_all_rows(self, field):
        logger.info(f'update_all_rows')
        transliteration_id = field.transliteration_id
        source_field_id = f'field_{field.source_field.id}'
        target_field_id = f'field_{field.id}'

        table_id = field.table.id


        run_clt_transliteration_all_rows.delay(table_id, 
                                                transliteration_id,
                                                source_field_id, 
                                                target_field_id,
                                                self.get_usage_user_id(field))



class DictionaryLookupFieldType(TransformationFieldType):
    type = "dictionary_lookup"
    model_class = DictionaryLookupField
    allowed_fields = [
        'source_field_id',
        'lookup_id'
    ]
    serializer_field_names = [
        'source_field_id',
        'lookup_id'
    ]
    serializer_field_overrides = {
        "source_field_id": serializers.IntegerField(
            required=False,
            allow_null=True,
            source="source_field.id",
            help_text="The id of the field for which to do dictionary lookup",
        ),
        "lookup_id": serializers.CharField(
            required=True,
            allow_null=False,
            allow_blank=False
        ),
    }

    can_be_primary_field = False

    def prepare_value_for_db(self, instance, value):
        return value

    def get_serializer_field(self, instance, **kwargs):
        return serializers.CharField(
            **{
                "required": False,
                "allow_null": True,
                "allow_blank": True,
                **kwargs,
            }        
        )

    def get_model_field(self, instance, **kwargs):
        return TranslationTextField(
            default=None,
            blank=True, 
            null=True, 
            **kwargs
        )


    def transform_value(self, field, source_value, usage_user_id):
        lookup_id = field.lookup_id
        lookup_result = clt_interface.get_dictionary_lookup(source_value, lookup_id, usage_user_id)
        return lookup_result

    def row_of_dependency_updated(
        self,
        field,
        starting_row,
        update_collector,
        field_cache,
        via_path_to_starting_table,
    ):

        if USE_ENHANCED_UPDATE_COLLECTOR:
            def perform_dictionary_lookup_rows(rows):
                lookup_id = field.lookup_id
                source_internal_field_name = f'field_{field.source_field.id}'
                target_internal_field_name = f'field_{field.id}'
                for row in rows:
                    text = getattr(row, source_internal_field_name)
                    if text != None:
                        lookup_result = clt_interface.get_dictionary_lookup(text, lookup_id)
                        setattr(row, target_internal_field_name, lookup_result)

            update_collector.add_field_with_pending_update_function(
                field,
                update_function=perform_dictionary_lookup_rows,
                via_path_to_starting_table=via_path_to_starting_table,
            )       
        else:
            self.process_transformation(field, starting_row)

        ViewHandler().field_value_updated(field)     

        super().row_of_dependency_updated(
            field,
            starting_row,
            update_collector,
            field_cache,
            via_path_to_starting_table,
        )        


    def update_all_rows(self, field):
        logger.info(f'update_all_rows')
        lookup_id = field.lookup_id
        source_field_id = f'field_{field.source_field.id}'
        target_field_id = f'field_{field.id}'

        table_id = field.table.id

        run_clt_lookup_all_rows.delay(table_id, 
                                        lookup_id, 
                                        source_field_id, 
                                        target_field_id,
                                        self.get_usage_user_id(field))

class ChineseRomanizationFieldType(TransformationFieldType):
    type = "chinese_romanization"
    model_class = ChineseRomanizationField
    allowed_fields = [
        'source_field_id',
        'correction_table_id',
        'transformation',
        'tone_numbers',
        'spaces'
    ]

    can_be_primary_field = False

    def prepare_value_for_db(self, instance, value):
        return value

    def get_serializer_field(self, instance, **kwargs):
        return serializers.JSONField(**kwargs)

    def get_model_field(self, instance, **kwargs):
        return models.JSONField(default={}, **kwargs)

    def transform_value(self, field, source_value, usage_user_id):
        if field.transformation == CHOICE_PINYIN:
            return clt_interface.get_pinyin(source_value, field.tone_numbers, field.spaces)
        elif field.transformation == CHOICE_JYUTPING:
            return clt_interface.get_jyutping(source_value, field.tone_numbers, field.spaces)

    def row_of_dependency_updated(
        self,
        field,
        starting_row,
        update_collector,
        field_cache: "FieldCache",
        via_path_to_starting_table,
    ):

        self.process_transformation(field, starting_row)

        ViewHandler().field_value_updated(field)     

        super().row_of_dependency_updated(
            field,
            starting_row,
            update_collector,
            field_cache,
            via_path_to_starting_table,
        )        


    def update_all_rows(self, field):
        # TODO write this
        pass
        # logger.info(f'update_all_rows')
        # transliteration_id = field.transliteration_id
        # source_field_id = f'field_{field.source_field.id}'
        # target_field_id = f'field_{field.id}'

        # table_id = field.table.id


        # run_clt_transliteration_all_rows.delay(table_id, 
        #                                         transliteration_id,
        #                                         source_field_id, 
        #                                         target_field_id,
        #                                         self.get_usage_user_id(field))