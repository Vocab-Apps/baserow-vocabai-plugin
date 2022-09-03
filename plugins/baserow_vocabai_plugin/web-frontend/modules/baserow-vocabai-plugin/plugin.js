import {PluginNamePlugin} from '@baserow-vocabai-plugin/plugins'
import {LanguageFieldType} from '@baserow-vocabai-plugin/vocabAiFieldTypes'

import cloudlanguagetoolsStore from '@baserow-vocabai-plugin/store/cloudlanguagetools'

export default (context) => {
  const { app } = context
  app.$registry.register('plugin', new PluginNamePlugin(context))

  app.$registry.register('field', new LanguageFieldType(context))
}
