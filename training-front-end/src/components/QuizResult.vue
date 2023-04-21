<script setup>
  import Cancel from './icons/CancelIcon.vue';
  import CheckCircleIcon from './icons/CheckCircleIcon.vue';

  const props = defineProps({
    index: {
      type: Number,
      required: true
    },
    question: {
      type: Object,
      required: true
    }, 
    result: {
      type: Object,
      required: true
    }
  })
  const label = answerIndex => {
    if (props.result.correct_ids.includes(answerIndex)){
      return "Correct:"
    }
    if (props.result.selected_ids.includes(answerIndex)) {
      return props.result.correct ? "Correct:" : "You Selected:"
    } 
    return ''
  }

  const isHighlighted = answer_index => {
    return props.result.correct_ids.includes(answer_index)
    || (props.result.selected_ids.includes(answer_index) && props.result.correct)
  }
</script>

<template>
  <h4 class="usa-accordion__heading">
    <button
      type="button"
      class="usa-accordion__button"
      aria-expanded="false"
      :aria-controls="index"
    > 
      <div class="">
        <div 
          v-if="result.correct" 
          class="usa-icon-list__icon text-green width-4 float-left"
        >
          <CheckCircleIcon />
        </div>
        <div 
          v-else
          class="usa-icon-list__icon text-secondary-dark width-4 float-left"
        >
          <Cancel />
        </div>
        <div
          class="width-4 text-right float-left"
        >
          {{ index + 1 }}. 
        </div>
        <div class="margin-left-9">
          {{ question.text }}
        </div>
      </div>
    </button>
  </h4>
  <div 
    :id="index"
    class="usa-accordion__content usa-prose "
  >
    <div 
      v-for="({id, text}, answer_index) in question.choices"
      :key="id"
      class="display-flex margin-y-1"
      :class="{'bg-base-lightest': isHighlighted(answer_index)}"
      data-test="answers"
    >
      <div class="flex-shrink-0 width-15 text-right display-inline-block">
        <b>
          {{ label(answer_index) }} 
        </b>
      </div>
      <div class="margin-left-2">
        {{ text }}
      </div>
    </div>
  </div>
</template>
