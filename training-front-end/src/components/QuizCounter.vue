<script setup>
  const props = defineProps({
    'current': Number,
    'total': Number
  })
</script>
<template>
<div class="usa-step-indicator__header">
        <h4 class="usa-step-indicator__heading margin-top-0">
          <span class="usa-step-indicator__heading-counter">
          <span class="usa-step-indicator__current-step margin-right-1">{{ current }} </span>
          <span class="usa-step-indicator__total-steps">of {{ total }}</span> </span><span class="usa-step-indicator__heading-text">Questions</span>
        </h4>
      </div>
</template>