<script setup>
  const props = defineProps(['question', 'selection'])
  const emit = defineEmits(['select_answer'])

  function select_answer(event) {
    const answer = {'question_id': props.question.id, 'response_ids': [parseInt([event.target.value])] }
    emit('select_answer', answer)
  }
</script>
<template>
  <h3 class="">{{ question.text }}</h3>

  <fieldset class="usa-fieldset margin-bottom-2">
    <div class="usa-radio" v-for="({id, text}) in question.choices">
      <input
        class="usa-radio__input usa-radio__input--tile"
        :id="id"
        type="radio"
        name="historical-figures"
        :checked="selection && selection.response_ids.includes(id)"
        @change="select_answer"
        :value="id"
      />
      <label class="usa-radio__label" :for="id"
      >{{text}}</label>
    </div>
  </fieldset>
</template>