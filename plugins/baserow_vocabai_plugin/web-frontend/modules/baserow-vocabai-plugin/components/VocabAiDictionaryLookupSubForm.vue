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
        v-model="values.lookup_id"
        @input="dictionaryLookupOptionSelected"
      >
        <DropdownItem
          v-for="option in dictionaryLookupOptions"
          :key="option.lookup_id"
          :name="option.lookup_shortname"
          :value="option.lookup_id"
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
  name: 'VocabAiDictionaryLookupSubForm',
  mixins: [form, fieldSubForm],
  created() {
    if (this.$store.getters['cloudlanguagetools/allLanguages'].length == 0) {
      this.$store.dispatch('cloudlanguagetools/fetchAll', '', { root: true });
    }
  },    
  data() {
    return {
      allowedValues: ['source_field_id', 'lookup_id'],
      values: {
        source_field_id: '',
        lookup_id: '',
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
    async dictionaryLookupOptionSelected() {
      console.log('dictionary lookup option: ', this.values.lookup_id);
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
    dictionaryLookupOptions() {
      if (this.selectedSourceFieldLanguage == '') {
        return [];
      }
      const dictionaryLookupOptions = this.$store.getters['cloudlanguagetools/dictionaryLookupOptionsForLanguage'](this.selectedSourceFieldLanguage);
      return dictionaryLookupOptions;
    },
  }  
}
</script>
