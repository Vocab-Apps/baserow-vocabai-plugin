<template>
  <div>
    <div class="control">
      <label class="control__label control__label--small">
          Select the source field
      </label>
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
      <label class="control__label control__label--small">
          Select transformation type
        </label>      
      <Dropdown
        v-model="values.transformation"
      >
        <DropdownItem
          v-for="option in transformations"
          :key="option.transformation_id"
          :name="option.transformation_name"
          :value="option.transformation_id"
          icon="font"
        ></DropdownItem>
      </Dropdown>      
    </div>    

    <div class="control">
      <div class="control__elements">
        <Checkbox v-model="values.tone_numbers">Tone Numbers</Checkbox>
      </div>
    </div>

    <div class="control">
      <div class="control__elements">
        <Checkbox v-model="values.spaces">Spaces between characters</Checkbox>
      </div>
    </div>    

  </div>
</template>

<script>
import form from '@baserow/modules/core/mixins/form'

import fieldSubForm from '@baserow/modules/database/mixins/fieldSubForm'

export default {
  name: 'VocabAiChineseRomanizationSubForm',
  mixins: [form, fieldSubForm],
  created() {
    if (this.$store.getters['cloudlanguagetools/allLanguages'].length == 0) {
      this.$store.dispatch('cloudlanguagetools/fetchAll', '', { root: true });
    }
  },    
  data() {
    return {
      allowedValues: ['source_field_id', 'transformation', 'tone_numbers', 'spaces'],
      values: {
        source_field_id: '',
        transformation: '',
        tone_numbers: false,
        spaces: false,
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
    transformations() {
      return [
        {
          'transformation_name': 'Pinyin',
          'transformation_id': 'pinyin'
        },
        {
          'transformation_name': 'Jyutping',
          'transformation_id': 'jyutping'
        }
      ];
    },
  }  
}
</script>
