<template>
    <div
      ref="cell"
      class="grid-view__cell active"
      :class="{ editing: editing }"
      @contextmenu="stopContextIfEditing($event)"
    >
      <div v-if="!editing && value" class="grid-field-text">{{ value.solutions }}</div>
      <div v-else class="grid-field-text">(edit): {{ value.solutions }}</div>
    </div>
  </template>
  
  <script>
  import gridField from '@baserow/modules/database/mixins/gridField'
  import gridFieldInput from '@baserow/modules/database/mixins/gridFieldInput'
  
  export default {
    mixins: [gridField, gridFieldInput],
    /*
    methods: {
      afterEdit() {
        this.$nextTick(() => {
          this.$refs.input.focus()
          this.$refs.input.selectionStart = this.$refs.input.selectionEnd = 100000
        })
      },
    },
    */
  }
  </script>
  