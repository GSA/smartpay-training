<script setup>
  const props = defineProps({
    'question': {
      type: Object,
      required: true
    },
    'selection': {
      type: Object,
      required: false,
      default: undefined
    }
  })
  const emit = defineEmits(['select_answer'])

  function select_answer(event) {
    var response_id = parseInt(event.target.value)
    var response = props.question.choices[response_id]
    const answer = {
      'question_id': props.question.id, 
      'question': props.question.text,
      'response_id': response_id,
      'response': response.text,
      'correct': response.correct
    }

    emit('select_answer', answer)
  }
</script>
<template>
  <fieldset class="usa-fieldset margin-bottom-2">
    <legend class="quiz-question">
      {{ question.text }}
    </legend>
    <div
      v-for="({id, text}) in question.choices"
      :key="id"
      class="usa-radio"
    >
      <input
        :id="id"
        class="usa-radio__input usa-radio__input--tile"
        type="radio"
        name="historical-figures"
        :checked="selection && selection.response_id == id"
        :value="id"
        @change="select_answer"
      >
      <label
        class="usa-radio__label"
        :for="id"
      >{{ text }}</label>
    </div>
  </fieldset>
</template>