<script>
export default {
  props: {
    romanization: Object
  }
}
</script>

<template>
    <span>
        <span v-for="(solution, solution_index) in romanization.solutions">
            <span v-if="romanization.solution_overrides.length > solution_index">{{ solution[romanization.solution_overrides[solution_index]] }} </span>
            <span v-else>{{ solution[0] }} </span>
        </span>
    </span>
</template>