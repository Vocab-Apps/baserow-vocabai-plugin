<template>
  <div>
    
    <FormGroup
      small-label
      label="Select Source Field"
      class="margin-bottom-2"
      required
    >    
    
      <Dropdown
        v-model="values.source_field_id"
        @input="sourceFieldSelected"
        :fixed-items="true"
      >
        <DropdownItem
          v-for="field in tableFields"
          :key="field.id"
          :name="field.name"
          :value="field.id"
          :icon="field.icon"
        ></DropdownItem>
      </Dropdown>

    </FormGroup>

    <FormGroup
      small-label
      label="Select Language to translate to"
      class="margin-bottom-2"
      required
    >    
      <Dropdown
        v-model="values.target_language"
        @input="languageSelected"
        :fixed-items="true"
      >
        <DropdownItem
          v-for="language in languageList"
          :key="language.id"
          :name="language.name"
          :value="language.id"
          icon="font"
        ></DropdownItem>
      </Dropdown>      
    </FormGroup>

    <FormGroup
      small-label
      label="Select Translation Service"
      class="margin-bottom-2"
      required
    >    

      <Dropdown
        v-model="values.service"
        @input="translationServiceSelected"
        :fixed-items="true"
      >
        <DropdownItem
          v-for="service in serviceList"
          :key="service"
          :name="service"
          :value="service"
          icon="font"
        ></DropdownItem>
      </Dropdown>      
    </FormGroup>

  </div>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'

import fieldSubForm from '@baserow/modules/database/mixins/fieldSubForm'


export default {
  name: 'VocabAiTranslationSubForm',
  mixins: [form, fieldSubForm],
  created() {
    if (this.$store.getters['cloudlanguagetools/allLanguages'].length == 0) {
      this.$store.dispatch('cloudlanguagetools/fetchAll', '', { root: true });
    }
  },  
  data() {
    return {
      allowedValues: ['source_field_id', 'target_language', 'service'],
      values: {
        source_field_id: '',
        target_language: '',
        service: '',
      },
      selectedSourceFieldLanguage: '',
    }
  },
  methods: {
    isFormValid() {
      return true
    },
    async sourceFieldSelected() {
      console.log('TranslationSubForm: sourceFieldSelected, source_field_id: ', this.values.source_field_id);
      const selectedField = this.$store.getters['field/get'](
          this.values.source_field_id
      );
      // console.log('selectedField: ', selectedField);
      this.selectedSourceFieldLanguage = selectedField.language;
      console.log('selectedSourceFieldLanguage: ', this.selectedSourceFieldLanguage);
    },    
    async languageSelected() {
      console.log('target language: ', this.values.target_language);
    },        
    async translationServiceSelected() {
      console.log('translation_service: ', this.values.translation_service);
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

      console.log('allFields: ', allFields);

      const allLanguageFields = allFields.filter((f) => {
              return f != undefined && f.type == "language_text"
            });


      console.log('allLanguageFields: ', allLanguageFields);

      return allLanguageFields;
    },
    languageList() {
      console.log("computed: languageList");
      const allLanguages = this.$store.getters['cloudlanguagetools/allLanguages'];
      console.log("allLanguages: ", allLanguages);
      return allLanguages;
    },
    serviceList() {
      console.log("computed: serviceList");
      if( this.selectedSourceFieldLanguage != '' && this.values.target_language != '') {
        const serviceList = this.$store.getters['cloudlanguagetools/translationServicesForLanguages'](this.selectedSourceFieldLanguage, this.values.target_language);
        console.log("filtered service list: ", serviceList);
        return serviceList;
      } else {
        const serviceList = this.$store.getters['cloudlanguagetools/allTranslationServices'];
        console.log("serviceList, all services: ", serviceList);
        return serviceList;
      }
    }
  }  
}
</script>
