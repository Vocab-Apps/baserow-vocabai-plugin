import logging
import redis
import json
import datetime
import cloudlanguagetools.servicemanager

from .quotas import get_usage_record
from ..fields.vocabai_models import VocabAiLanguageData

from django.conf import settings

logger = logging.getLogger(__name__)

manager = cloudlanguagetools.servicemanager.ServiceManager() 
manager.configure_default()

def get_servicemanager():
    return manager

def update_language_data():
    logger.info('retrieving language data')
    language_list = manager.get_language_list()
    language_data = manager.get_language_data_json_v2()

    language_data_records = VocabAiLanguageData.objects.all()
    
    if len(language_data_records) == 1:
        language_data_record = language_data_records[0]
    else:
        # create new record
        language_data_record = VocabAiLanguageData()
    
    # update the record
    language_data_record.language_list = language_list
    language_data_record.free_transformation_options = language_data['free']
    language_data_record.premium_transformation_options = language_data['premium']

    # update database
    language_data_record.save()

    logger.info('saved language data')
        
def get_language_data_record():
    language_data_records = VocabAiLanguageData.objects.all()
    if len(language_data_records) != 1:
        raise Exception(f'could not find language data record')
    return language_data_records[0]

def get_language_list():
    return get_language_data_record().language_list

def get_translation_options():
    return get_language_data_record().premium_transformation_options['translation_options']

def get_transliteration_options():
    return get_language_data_record().premium_transformation_options['transliteration_options']

def get_dictionary_lookup_options():
    return get_language_data_record().premium_transformation_options['dictionary_lookup_options']

def get_translation_services_source_target_language(source_language, target_language):
    translation_options = get_translation_options()
    source_language_options = [x for x in translation_options if x['language_code'] == source_language]
    target_language_options = [x for x in translation_options if x['language_code'] == target_language]
    source_services = [x['service'] for x in source_language_options]
    target_services = [x['service'] for x in target_language_options]
    service_list = list(set(source_services).intersection(target_services))
    return service_list


def get_translation(text, source_language, target_language, service, usage_user_id):
    translation_options = get_translation_options()
    source_language_options = [x for x in translation_options if x['language_code'] == source_language and x['service'] == service]
    target_language_options = [x for x in translation_options if x['language_code'] == target_language and x['service'] == service]
    source_language_key = source_language_options[0]['language_id']
    target_language_key = target_language_options[0]['language_id']

    usage_record = get_usage_record(usage_user_id)
    character_cost = manager.service_cost(text, service, cloudlanguagetools.constants.RequestType.translation)    
    logger.debug(f'character_cost: {character_cost}, service: {service}')
    usage_record.check_quota_available(character_cost)

    translated_text = manager.get_translation(text, service, source_language_key, target_language_key)


    usage_record.update_usage(character_cost)

    return translated_text


def get_transliteration(text, transliteration_id, usage_user_id):
    transliteration_options = get_transliteration_options()
    transliteration_option = [x for x in transliteration_options if x['transliteration_id'] == transliteration_id]
    service = transliteration_option[0]['service']
    transliteration_key = transliteration_option[0]['transliteration_key']

    usage_record = get_usage_record(usage_user_id)
    character_cost = manager.service_cost(text, service, cloudlanguagetools.constants.RequestType.transliteration)
    usage_record.check_quota_available(character_cost)

    translated_text = manager.get_transliteration(text, service, transliteration_key)


    usage_record.update_usage(character_cost)

    return translated_text    


def get_dictionary_lookup(text, lookup_id, usage_user_id):
    dictionary_lookup_options = get_dictionary_lookup_options()
    lookup_option = [x for x in dictionary_lookup_options if x['lookup_id'] == lookup_id]
    service = lookup_option[0]['service']
    lookup_key = lookup_option[0]['lookup_key']

    usage_record = get_usage_record(usage_user_id)
    character_cost = manager.service_cost(text, service, cloudlanguagetools.constants.RequestType.dictionary)
    usage_record.check_quota_available(character_cost)

    try:
        lookup_result = manager.get_dictionary_lookup(text, service, lookup_key)

        usage_record.update_usage(character_cost)        

        if isinstance(lookup_result, list):
            return ' / '.join(lookup_result)
        elif isinstance(lookup_result, dict):
            result_list = []
            for key, value in lookup_result.items():
                result_list.append(key + ': ' + ' / '.join(value))
            return ', '.join(result_list)
        else:
            return str(lookup_result)
    except cloudlanguagetools.errors.NotFoundError:
        return None


def get_pinyin(text, tone_numbers, spaces, corrections=[]):
    romanization_solution = manager.get_pinyin(text, tone_numbers, spaces, corrections=corrections)
    return {
        'solution_overrides': [],
        'solutions': romanization_solution
    }

def get_jyutping(text, tone_numbers, spaces, corrections=[]):
    romanization_solution =  manager.get_jyutping(text, tone_numbers, spaces, corrections=corrections)    
    return {
        'solution_overrides': [],
        'solutions': romanization_solution
    }