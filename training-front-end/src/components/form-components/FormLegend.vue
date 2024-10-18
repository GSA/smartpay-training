<script setup>
  const props = defineProps({
    'value': {
      type: String,
      required: true
    },
    'required': {
      type: Boolean,
      required: true
    },
  });
</script>

<template>
  <legend
    class="usa-legend"
  >
    {{ props.value }}<span
      v-if="props.required"
      class="text-secondary-dark"
    >
      (*Required)
    </span>
    <span v-else>
      (optional)
    </span>
  </legend>
</template>