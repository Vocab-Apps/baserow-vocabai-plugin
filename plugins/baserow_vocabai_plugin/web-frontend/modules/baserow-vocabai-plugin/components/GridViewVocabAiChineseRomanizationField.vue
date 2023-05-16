<script>
import gridField from '@baserow/modules/database/mixins/gridField'
import gridFieldInput from '@baserow/modules/database/mixins/gridFieldInput'

export default {
  mixins: [gridField, gridFieldInput],
  methods: {
    select_romanization_alternative(word_index, alternative_index)
    {
      console.log(`selecting ${word_index}, ${alternative_index}`);
      this.copy.solution_overrides[word_index] = alternative_index;
      // this will trigger the http patch request to update the backend
      this.save();
    },
    afterEdit() {
      // console.log('chinese romanization afterEdit');
      // we need this to ensure we're working on a deep copy
      this.copy = JSON.parse(JSON.stringify(this.value));
    },
    onClick() {
      // start edit mode
      if (!this.editing) {
        this.edit(null, event)
      } else {
        // cancel edit in progress
        this.cancel();
      }
    }
  }
}
</script>


<template>
    <div
      ref="cell"
      class="grid-view__cell active"
      :class="{ editing: editing }"
      @contextmenu="stopContextIfEditing($event)"
    >
      <div v-if="value" class="grid-field-text" @click="onClick()">{{ value.rendered_solution }}</div>
      <div v-if="editing && value" class="dropdown dropdown--floating dropdown--floating">
        <div class="dropdown__items" style="width: 100%;">
        <table>
          <tr v-for="(solution, solution_index) in value.solutions">
            <td>{{ value.word_list[solution_index] }}</td>
            <td >
              <span class="chinese_romanization_word">
              <span
                v-on:click="select_romanization_alternative(solution_index, romanization_index)" 
                v-for="(romanization, romanization_index) in solution" 
                class="chinese_romanization_alternative" 
                :class="{ 
                        'background-color--blue': value.solution_overrides[solution_index] == romanization_index,
                        'background-color--light-gray': value.solution_overrides[solution_index] != romanization_index }"                
                >
                {{ romanization }}
                  </span>
                </span>
              </td>
            </tr>
        </table>
        </div>
      </div>
    </div>
  </template>
  
