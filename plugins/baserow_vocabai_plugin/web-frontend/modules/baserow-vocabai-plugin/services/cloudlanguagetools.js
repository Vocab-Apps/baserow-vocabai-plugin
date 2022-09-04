export default (client) => {
  return {
    fetchAllLanguages() {
      return client.get(`/baserow_vocabai_plugin/language_list/`)
    },
    fetchAllTranslationOptions() {
      return client.get(`/baserow_vocabai_plugin/translation_options/`)
    },    
    fetchAllTransliterationOptions() {
      return client.get(`/baserow_vocabai_plugin/transliteration_options/`)
    },        
    fetchAllDictionaryLookupOptions() {
      return client.get(`/baserow_vocabai_plugin/dictionary_lookup_options/`)
    },            
    fetchTranslationServices(source_language, target_language) {
      return client.get(`/baserow_vocabai_plugin/translation_services/${source_language}/${target_language}`)
    },        
  }
}
