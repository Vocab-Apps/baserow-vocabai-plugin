<template functional>
    <div ref="cell" class="grid-view__cell" :class="data.staticClass || ''">
      <div class="grid-field-text">
        <span v-if="props.value" v-for="word in props.value.solutions">
          {{ word[0] }}
        </span>
      </div>
    </div>
</template>
  