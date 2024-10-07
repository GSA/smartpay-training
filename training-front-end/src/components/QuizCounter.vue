<script setup>
  defineProps({
    'current': {
      type: Number,
      required: true
    },
    'total':{ 
      type: Number,
      required: true
    }
  })
</script>
<template>
  <div
    class="usa-step-indicator__header"
    data-test="quiz-counter"
  >
    <h2 class="usa-step-indicator__heading margin-top-0">
      <span class="usa-step-indicator__heading-counter">
        <span class="usa-sr-only">Question </span>
        <span class="usa-step-indicator__current-step margin-right-0"> {{ current }}</span>
        <span class="usa-step-indicator__total-steps margin-right-0"> of {{ total }}</span> 
      </span>
      <span class="usa-step-indicator__heading-text"> Questions</span>
    </h2>
  </div>
</template>