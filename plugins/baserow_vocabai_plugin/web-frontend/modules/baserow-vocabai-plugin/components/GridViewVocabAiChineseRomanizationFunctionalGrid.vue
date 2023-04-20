<template functional>
    <div ref="cell" class="grid-view__cell" :class="data.staticClass || ''">
      <div class="grid-field-text">
        <span v-if="props.value">
          {{ props.value.rendered_solution }}
        </span>
      </div>
    </div>
</template>
  