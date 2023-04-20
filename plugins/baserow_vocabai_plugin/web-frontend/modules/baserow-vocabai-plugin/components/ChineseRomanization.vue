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
            {{ solution[0] }}
        </span>
    </span>
</template>