from django.db import models

from baserow.contrib.database.fields.models import Field


# after making changes, run
# ./dev.sh run backend manage makemigrations
# ./dev.sh run backend manage migrate

# as a plugin:
# docker-compose run baserow-vocabai-plugin /baserow.sh backend-cmd manage makemigrations
# docker-compose run baserow-vocabai-plugin /baserow.sh backend-cmd manage migrate

# I find that I have to run this:
# docker container exec e214ca3b3644 /baserow.sh backend-cmd manage makemigrations baserow_vocabai_plugin
# docker container exec e214ca3b3644 /baserow.sh backend-cmd manage migrate baserow_vocabai_plugin

# undoing a migration:
# ./dev.sh run backend manage migrate database 0084

class LanguageField(Field):
    language = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Language",
    )    


class TranslationField(Field):
    source_field = models.ForeignKey(
        LanguageField,
        on_delete=models.CASCADE,
        help_text="The field to translate.",
        null=True,
        blank=True,
        related_name='+'
    )    
    target_language = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Target Language",
    )        
    service = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Translation Service",
    )            

class TransliterationField(Field):
    source_field = models.ForeignKey(
        LanguageField,
        on_delete=models.CASCADE,
        help_text="The field to transliterate.",
        null=True,
        blank=True,
        related_name='+'
    )    
    transliteration_id = models.CharField(
        max_length=2048,
        blank=True,
        default="",
        help_text="Transliteration key for this service",
    )        

class DictionaryLookupField(Field):
    source_field = models.ForeignKey(
        LanguageField,
        on_delete=models.CASCADE,
        help_text="The field to do dictionary lookup for.",
        null=True,
        blank=True,
        related_name='+'
    )    
    lookup_id = models.CharField(
        max_length=2048,
        blank=True,
        default="",
        help_text="Dictionary lookup key for this service",
    )            