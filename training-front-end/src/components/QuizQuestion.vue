<script setup>
  import { ref } from "vue"
  const props = defineProps(['question', 'selection'])
  const emits = defineEmits(['select_answer'])
  const selected = ref()
</script>
<template>
  
  
  <h3 class="">{{ question.question }}</h3>

  <fieldset class="usa-fieldset margin-bottom-2">
    <div class="usa-radio" v-for="(answer, index) in question.answers">
      <input
        class="usa-radio__input usa-radio__input--tile"
        :id="index"
        type="radio"
        name="historical-figures"
        :checked="selection === index"
        @change="$emit('select_answer', $event.target.value)"
        :value="index"
      />
      <label class="usa-radio__label" :for="index"
      >{{answer}}</label
      >
    </div>
  </fieldset>
</template>