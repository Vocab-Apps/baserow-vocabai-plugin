import * as Sentry from "@sentry/browser";
import { BrowserTracing } from "@sentry/tracing";

import {PluginNamePlugin} from '@baserow-vocabai-plugin/plugins'
import {LanguageFieldType} from '@baserow-vocabai-plugin/vocabAiFieldTypes'
import {TranslationFieldType} from '@baserow-vocabai-plugin/vocabAiFieldTypes'
import {TransliterationFieldType} from '@baserow-vocabai-plugin/vocabAiFieldTypes'
import {DictionaryLookupFieldType} from '@baserow-vocabai-plugin/vocabAiFieldTypes'

Sentry.init({
  dsn: "https://33f709910b214ed282315bd91344bae0@o968582.ingest.sentry.io/6742673",

  // Alternatively, use `process.env.npm_package_version` for a dynamic release version
  // if your build tool supports it.
  integrations: [new BrowserTracing()],

  // Set tracesSampleRate to 1.0 to capture 100%
  // of transactions for performance monitoring.
  // We recommend adjusting this value in production
  tracesSampleRate: 1.0,

});

import cloudlanguagetoolsStore from '@baserow-vocabai-plugin/store/cloudlanguagetools'

export default (context) => {
  const { store, app, isDev } = context
  
  app.$registry.register('plugin', new PluginNamePlugin(context))

  store.registerModule('cloudlanguagetools', cloudlanguagetoolsStore)

  app.$registry.register('field', new LanguageFieldType(context))
  app.$registry.register('field', new TranslationFieldType(context))
  app.$registry.register('field', new TransliterationFieldType(context))
  app.$registry.register('field', new DictionaryLookupFieldType(context))
}
