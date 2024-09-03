import { FieldType } from '@baserow/modules/database/fieldTypes'

import GridViewFieldText from '@baserow/modules/database/components/view/grid/fields/GridViewFieldText'
import RowEditFieldText from '@baserow/modules/database/components/row/RowEditFieldText'
import VocabAiTranslationSubForm from '@baserow-vocabai-plugin/components/VocabAiTranslationSubForm'
import VocabAiTransliterationSubForm from '@baserow-vocabai-plugin/components/VocabAiTransliterationSubForm'
import VocabAiDictionaryLookupSubForm from '@baserow-vocabai-plugin/components/VocabAiDictionaryLookupSubForm'
import VocabAiChineseRomanizationSubForm from '@baserow-vocabai-plugin/components/VocabAiChineseRomanizationSubForm'
import VocabAiLanguageTextSubForm from '@baserow-vocabai-plugin/components/VocabAiLanguageTextSubForm'
import FunctionalGridViewFieldText from '@baserow/modules/database/components/view/grid/fields/FunctionalGridViewFieldText'
import GridViewVocabAiChineseRomanizationField from '@baserow-vocabai-plugin/components/GridViewVocabAiChineseRomanizationField'
import GridViewVocabAiChineseRomanizationFunctionalGrid from '@baserow-vocabai-plugin/components/GridViewVocabAiChineseRomanizationFunctionalGrid'
import RowEditVocabAiChineseRomanizationField from '@baserow-vocabai-plugin/components/RowEditVocabAiChineseRomanizationField'


export class LanguageFieldType extends FieldType {
  static getType() {
    return 'language_text'
  }

  getIconClass() {
    return 'font'
  }

  getName() {
    return 'Language Text'
  }

  getFormComponent() {
    return VocabAiLanguageTextSubForm
  }

  getGridViewFieldComponent() {
    return GridViewFieldText
  }

  getRowEditFieldComponent() {
    return RowEditFieldText
  }

  getFunctionalGridViewFieldComponent() {
    return FunctionalGridViewFieldText
  }

  getDocsDataType(field) {
    return 'string'
  }

  getDocsDescription(field) {
    return this.app.i18n.t('fieldDocs.text')
  }

  getDocsRequestExample(field) {
    return 'string'
  }  

  getCanImport() {
    return true
  }

}

export class TranslationFieldType extends FieldType {
  static getType() {
    return 'translation'
  }

  getIconClass() {
    return 'list-ol'
  }

  getName() {
    return 'Translation'
  }

  // field must be set as read-only, otherwise it won't get updated after a PATCH request
  // https://community.baserow.io/t/custom-fields-in-my-plugin-after-upgrading-from-1-19-to-1-26-a-patch-request-doesnt-populate-derived-fields-anymore-i-suspect-a-front-end-issue/6003/4
  getIsReadOnly() {
    return true
  }

  getFormComponent() {
    return VocabAiTranslationSubForm
  }

  getGridViewFieldComponent() {
    return GridViewFieldText
  }

  getRowEditFieldComponent() {
    return RowEditFieldText
  }

  getFunctionalGridViewFieldComponent() {
    return FunctionalGridViewFieldText
  }

  getDocsDataType(field) {
    return 'string'
  }

  getDocsDescription(field) {
    return this.app.i18n.t('fieldDocs.text')
  }

  getDocsRequestExample(field) {
    return 'string'
  }  

}

export class TransliterationFieldType extends FieldType {
  static getType() {
    return 'transliteration'
  }

  getIconClass() {
    return 'list-ol'
  }

  getName() {
    return 'Transliteration'
  }

  getIsReadOnly() {
    return true
  }  

  getFormComponent() {
    return VocabAiTransliterationSubForm
  }

  getGridViewFieldComponent() {
    return GridViewFieldText
  }

  getRowEditFieldComponent() {
    return RowEditFieldText
  }

  getFunctionalGridViewFieldComponent() {
    return FunctionalGridViewFieldText
  }

  getDocsDataType(field) {
    return 'string'
  }

  getDocsDescription(field) {
    return this.app.i18n.t('fieldDocs.text')
  }

  getDocsRequestExample(field) {
    return 'string'
  }  

}

export class DictionaryLookupFieldType extends FieldType {
  static getType() {
    return 'dictionary_lookup'
  }

  getIconClass() {
    return 'list-ol'
  }

  getName() {
    return 'Dictionary Lookup'
  }

  getIsReadOnly() {
    return true
  }  

  getFormComponent() {
    return VocabAiDictionaryLookupSubForm
  }

  getGridViewFieldComponent() {
    return GridViewFieldText
  }

  getRowEditFieldComponent() {
    return RowEditFieldText
  }

  getFunctionalGridViewFieldComponent() {
    return FunctionalGridViewFieldText
  }

  getDocsDataType(field) {
    return 'string'
  }

  getDocsDescription(field) {
    return this.app.i18n.t('fieldDocs.text')
  }

  getDocsRequestExample(field) {
    return 'string'
  }  

}

export class ChineseRomanizationFieldType extends FieldType {
  static getType() {
    return 'chinese_romanization'
  }

  getIconClass() {
    return 'list-ol'
  }

  getName() {
    return 'Chinese Romanization'
  }

  getIsReadOnly() {
    return true
  }  

  getFormComponent() {
    return VocabAiChineseRomanizationSubForm
  }

  getGridViewFieldComponent() {
    return GridViewVocabAiChineseRomanizationField
  }

  getRowEditFieldComponent() {
    return RowEditVocabAiChineseRomanizationField
  }

  getFunctionalGridViewFieldComponent() {
    return GridViewVocabAiChineseRomanizationFunctionalGrid
  }

  getDocsDataType(field) {
    return 'string'
  }

  getDocsDescription(field) {
    return this.app.i18n.t('fieldDocs.text')
  }

  getDocsRequestExample(field) {
    return 'string'
  }  

  prepareValueForCopy(field, value) {
    if (value === undefined || 
        value === null || 
        value.rendered_solution === undefined ||
        value.rendered_solution === null) {
      return ''
    }
    return value.rendered_solution;
  }  

}