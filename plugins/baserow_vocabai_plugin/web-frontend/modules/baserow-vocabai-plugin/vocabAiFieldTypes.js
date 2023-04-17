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

  getFormComponent() {
    return VocabAiChineseRomanizationSubForm
  }

  getGridViewFieldComponent() {
    return GridViewVocabAiChineseRomanizationField
  }

  getRowEditFieldComponent() {
    return RowEditFieldText
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

}