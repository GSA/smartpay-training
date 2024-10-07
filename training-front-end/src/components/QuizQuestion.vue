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
    const answer = {'question_id': props.question.id, 'response_ids': [parseInt([event.target.value])] }
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
        :checked="selection && selection.response_ids.includes(id)"
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