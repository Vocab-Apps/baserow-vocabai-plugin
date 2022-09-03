import CloudLanguageToolsService from '@baserow-vocabai-plugin/services/cloudlanguagetools'

export const state = () => ({
  allLanguages: [],
  allTranslationOptions: [],
  allTransliterationOptions: [],
  allTranslationServices: [],
  allDictionaryLookupOptions: [],
})

export const mutations = {
  SET_ALL_LANGUAGES(state, allLanguages) {
    state.allLanguages = allLanguages;
  },
  SET_ALL_TRANSLATION_OPTIONS(state, allTranslationOptions) {
    state.allTranslationOptions = allTranslationOptions;
  },
  SET_ALL_TRANSLITERATION_OPTIONS(state, allTransliterationOptions) {
    state.allTransliterationOptions = allTransliterationOptions;
  },  
  SET_ALL_DICTIONARY_LOOKUP_OPTIONS(state, allDictionaryLookupOptions) {
    state.allDictionaryLookupOptions = allDictionaryLookupOptions;
  },    
  SET_ALL_TRANSLATION_SERVICES(state, allTranslationServices) {
    state.allTranslationServices = allTranslationServices;
  },  
}

export const actions = {

  async fetchAll({ dispatch}) {
    console.log('store/cloudlanguagetools fetchAll');
    await dispatch('fetchAllLanguages');
    await dispatch('fetchAllTranslationOptions');
    await dispatch('fetchAllTransliterationOptions');
    await dispatch('fetchAllDictionaryLookupOptions');
  },

  async fetchAllLanguages({ commit, getters, dispatch }, table) {
    console.log('store/cloudlanguagetools fetchAllLanguages');
    return new Promise((resolve, reject) => {
        // const { data } = await CloudLanguageToolsService(this.$client).fetchAllLanguages()
        CloudLanguageToolsService(this.$client).fetchAllLanguages().then((response) => {
            let languagesArray = [];
            for (const language_id in response.data) {
                languagesArray.push({
                id: language_id,
                name: response.data[language_id]
                });
            }
            languagesArray = languagesArray.sort((a, b) => a.name.localeCompare(b.name));
            commit('SET_ALL_LANGUAGES', languagesArray);
            resolve();
        });
    });
  },

  async fetchAllTranslationOptions({ commit, getters, dispatch }, table) {
    console.log('store/cloudlanguagetools fetchAllTranslationOptions');
    return new Promise((resolve, reject) => {
        CloudLanguageToolsService(this.$client).fetchAllTranslationOptions().then((response) => {
            commit('SET_ALL_TRANSLATION_OPTIONS', response.data);
            // get list of all services
            const services = Object.keys(response.data.reduce((result, key) => {
                // console.log('result: ', result, 'key: ', key);
                result[key['service']] = true;
                return result;
            }, {}));
            commit('SET_ALL_TRANSLATION_SERVICES', services);
            resolve();
        });
    });
  },  


  async fetchAllTransliterationOptions({ commit, getters, dispatch }, table) {
    console.log('store/cloudlanguagetools fetchAllTransliterationOptions');
    return new Promise((resolve, reject) => {
        CloudLanguageToolsService(this.$client).fetchAllTransliterationOptions().then((response) => {
            commit('SET_ALL_TRANSLITERATION_OPTIONS', response.data);
            // console.log("retrieved all transliteratino options: ", response.data);
            resolve();
        });
    });
  },  

  async fetchAllDictionaryLookupOptions({ commit, getters, dispatch }, table) {
    return new Promise((resolve, reject) => {
        CloudLanguageToolsService(this.$client).fetchAllDictionaryLookupOptions().then((response) => {
            commit('SET_ALL_DICTIONARY_LOOKUP_OPTIONS', response.data);
            resolve();
        });
    });
  },    


}

export const getters = {
    allLanguages(state) {
        return state.allLanguages;
    },
    allTranslationServices(state) {
        return state.allTranslationServices;
    },
    translationServicesForLanguages: (state) => (sourceLanguage, targetLanguage) => {
        const sourceLanguageServices = Object.keys(state.allTranslationOptions.filter((entry) => entry['language_code'] == sourceLanguage).
            reduce((result, entry) => {
                result[entry['service']] = true;
                return result;
            }, {}));
        const targetLanguageServices = Object.keys(state.allTranslationOptions.filter((entry) => entry['language_code'] == targetLanguage).
            reduce((result, entry) => {
                result[entry['service']] = true;
                return result;
            }, {}));            
        
        const commonServices = sourceLanguageServices.filter(value => targetLanguageServices.includes(value));
        return commonServices.sort((a, b) => a.localeCompare(b));
      },    

      transliterationOptionsForLanguage: (state) => (language) => {
        return state.allTransliterationOptions.filter((entry) => entry['language_code'] == language);
      },

      dictionaryLookupOptionsForLanguage: (state) => (language) => {
        return state.allDictionaryLookupOptions.filter((entry) => entry['language_code'] == language);
      },      
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
