<template>
  <div>
    <div class="control">

      <Dropdown
        v-model="values.source_field_id"
        @input="sourceFieldSelected"
      >
        <DropdownItem
          v-for="field in tableFields"
          :key="field.id"
          :name="field.name"
          :value="field.id"
          :icon="field.icon"
        ></DropdownItem>
      </Dropdown>
    </div>

    <div class="control">
      <Dropdown
        v-model="values.transliteration_id"
        @input="translationServiceSelected"
      >
        <DropdownItem
          v-for="option in transliterationOptions"
          :key="option.transliteration_id"
          :name="option.transliteration_shortname"
          :value="option.transliteration_id"
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
  name: 'VocabAiTransliterationSubForm',
  mixins: [form, fieldSubForm],
  created() {
    if (this.$store.getters['cloudlanguagetools/allLanguages'].length == 0) {
      this.$store.dispatch('cloudlanguagetools/fetchAll', '', { root: true });
    }
  },    
  data() {
    return {
      allowedValues: ['source_field_id', 'transliteration_id'],
      values: {
        source_field_id: '',
        transliteration_id: '',
      },
      selectedSourceFieldLanguage: '',
    }
  },
  methods: {
    isFormValid() {
      return true
    },
    async sourceFieldSelected() {
      console.log('source_field_id: ', this.values.source_field_id);
      const selectedField = this.$store.getters['field/get'](
          this.values.source_field_id
      );
      // console.log('selectedField: ', selectedField);
      this.selectedSourceFieldLanguage = selectedField.language;
      console.log('selectedSourceFieldLanguage: ', this.selectedSourceFieldLanguage);
    },    
    async translationServiceSelected() {
      console.log('translation_service: ', this.values.transliteration_id);
    },            
  },
  computed: {
    tableFields() {
      console.log("computed: tableFields");
      // collect all fields, including primary field in this table
      const primaryField = this.$store.getters['field/getPrimary'];
      const fields = this.$store.getters['field/getAll']

      let allFields = [primaryField];
      allFields = allFields.concat(fields);

      const allLanguageFields = allFields.filter((f) => {
              return f != undefined && f.type == "language_text"
            });


      console.log('allLanguageFields: ', allLanguageFields);

      return allLanguageFields;
    },
    transliterationOptions() {
      if (this.selectedSourceFieldLanguage == '') {
        return [];
      }
      const transliterationOptions = this.$store.getters['cloudlanguagetools/transliterationOptionsForLanguage'](this.selectedSourceFieldLanguage);
      return transliterationOptions;
    },
  }  
}
</script>
