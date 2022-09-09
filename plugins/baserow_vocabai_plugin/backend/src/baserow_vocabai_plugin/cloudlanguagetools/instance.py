import logging
import redis
import json
import cloudlanguagetools.servicemanager

from django.conf import settings

logger = logging.getLogger(__name__)

clt_instance = cloudlanguagetools.servicemanager.ServiceManager() 
clt_instance.configure_default()

redis_url = settings.REDIS_URL
logger.info(f'connecting to {redis_url}')
redis_client = redis.Redis.from_url( redis_url )

def get_servicemanager():
    return clt_instance

def get_language_list():
    redis_key = 'cloudlanguagetools:language_data:language_list'
    return json.loads(redis_client.get(redis_key))

def get_translation_options():
    redis_key = 'cloudlanguagetools:language_data:translation_options'
    return json.loads(redis_client.get(redis_key))

def get_transliteration_options():
    redis_key = 'cloudlanguagetools:language_data:transliteration_options'
    return json.loads(redis_client.get(redis_key))

def get_dictionary_lookup_options():
    redis_key = 'cloudlanguagetools:language_data:dictionary_lookup_options'
    return json.loads(redis_client.get(redis_key))    

def get_translation_services_source_target_language(source_language, target_language):
    translation_options = get_translation_options()
    source_language_options = [x for x in translation_options if x['language_code'] == source_language]
    target_language_options = [x for x in translation_options if x['language_code'] == target_language]
    source_services = [x['service'] for x in source_language_options]
    target_services = [x['service'] for x in target_language_options]
    service_list = list(set(source_services).intersection(target_services))
    return service_list


def get_translation(text, source_language, target_language, service):
    translation_options = get_translation_options()
    source_language_options = [x for x in translation_options if x['language_code'] == source_language and x['service'] == service]
    target_language_options = [x for x in translation_options if x['language_code'] == target_language and x['service'] == service]
    source_language_key = source_language_options[0]['language_id']
    target_language_key = target_language_options[0]['language_id']
    translated_text = clt_instance.get_translation(text, service, source_language_key, target_language_key)
    return translated_text


def get_transliteration(text, transliteration_id):
    transliteration_options = get_transliteration_options()
    transliteration_option = [x for x in transliteration_options if x['transliteration_id'] == transliteration_id]
    service = transliteration_option[0]['service']
    transliteration_key = transliteration_option[0]['transliteration_key']

    translated_text = clt_instance.get_transliteration(text, service, transliteration_key)
    return translated_text    


def get_dictionary_lookup(text, lookup_id):
    dictionary_lookup_options = get_dictionary_lookup_options()
    lookup_option = [x for x in dictionary_lookup_options if x['lookup_id'] == lookup_id]
    service = lookup_option[0]['service']
    lookup_key = lookup_option[0]['lookup_key']

    try:
        lookup_result = clt_instance.get_dictionary_lookup(text, service, lookup_key)
        if isinstance(lookup_result, list):
            return ' / '.join(lookup_result)
        else:
            return str(lookup_result)
    except cloudlanguagetools.errors.NotFoundError:
        return None