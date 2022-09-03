export default (client) => {
  return {
    fetchAllLanguages() {
      return client.get(`/database/cloudlanguagetools/language_list/`)
    },
    fetchAllTranslationOptions() {
      return client.get(`/database/cloudlanguagetools/translation_options/`)
    },    
    fetchAllTransliterationOptions() {
      return client.get(`/database/cloudlanguagetools/transliteration_options/`)
    },        
    fetchAllDictionaryLookupOptions() {
      return client.get(`/database/cloudlanguagetools/dictionary_lookup_options/`)
    },            
    fetchTranslationServices(source_language, target_language) {
      return client.get(`/database/cloudlanguagetools/translation_services/${source_language}/${target_language}`)
    },        
  }
}
