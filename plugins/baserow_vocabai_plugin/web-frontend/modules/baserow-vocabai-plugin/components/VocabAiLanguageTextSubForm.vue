<template>
  <div>
    <div class="control">
      <label class="control__label control__label--small">
          Select Language
      </label>
      <Dropdown
        v-model="values.language"
        @input="languageSelected"
      >
        <DropdownItem
          v-for="language in languageList"
          :key="language.id"
          :name="language.name"
          :value="language.id"
          icon="font"
        ></DropdownItem>
      </Dropdown>

    </div>
  </div>
</template>


<script>
import form from '@baserow/modules/core/mixins/form'

import fieldSubForm from '@baserow/modules/database/mixins/fieldSubForm'

export default {
  name: 'FieldTextSubForm',
  mixins: [form, fieldSubForm],
  created() {
    console.log('VocabAiLanguageTextSubForm created');
    if (this.$store.getters['cloudlanguagetools/allLanguages'].length == 0) {
      this.$store.dispatch('cloudlanguagetools/fetchAll', '', { root: true });
    }
  },
  data() {
    return {
      allowedValues: ['language'],
      values: {
        language: '',
      },
    }
  },
  computed: {
    languageList() {
      console.log("computed: languageList");
      const allLanguages = this.$store.getters['cloudlanguagetools/allLanguages'];
      console.log("allLanguages: ", allLanguages);
      return allLanguages;
    },    
  },  
  methods: {
    async languageSelected() {
      console.log('language: ', this.values.language);
    },        
    isFormValid() {
      return true
    },
  },
}
</script>
