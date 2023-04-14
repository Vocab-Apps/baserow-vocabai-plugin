import {PluginNamePlugin} from '@baserow-vocabai-plugin/plugins'
import {LanguageFieldType} from '@baserow-vocabai-plugin/vocabAiFieldTypes'
import {TranslationFieldType} from '@baserow-vocabai-plugin/vocabAiFieldTypes'
import {TransliterationFieldType} from '@baserow-vocabai-plugin/vocabAiFieldTypes'
import {DictionaryLookupFieldType} from '@baserow-vocabai-plugin/vocabAiFieldTypes'
import {ChineseRomanizationFieldType} from '@baserow-vocabai-plugin/vocabAiFieldTypes'

import cloudlanguagetoolsStore from '@baserow-vocabai-plugin/store/cloudlanguagetools'

export default (context) => {
  const { store, app, isDev } = context
  
  app.$registry.register('plugin', new PluginNamePlugin(context))

  store.registerModule('cloudlanguagetools', cloudlanguagetoolsStore)

  app.$registry.register('field', new LanguageFieldType(context))
  app.$registry.register('field', new TranslationFieldType(context))
  app.$registry.register('field', new TransliterationFieldType(context))
  app.$registry.register('field', new DictionaryLookupFieldType(context))
  app.$registry.register('field', new ChineseRomanizationFieldType(context))
}
