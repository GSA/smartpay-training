<script setup>
  const props = defineProps({
    'for': {
      type: String,
      required: true
    },
    'id': {
      type: String,
      required: true
    },
    'required': {
      type: Boolean,
      required: true
    },
    'value': {
      type: String,
      required: true
    },
  });
</script>

<template>
  <label
    v-if="!props.useLegend"
    :id="`${props.id}`"
    class="usa-label"
    :for="`${props.for}`"
  >{{ props.value }}<span
    v-if="props.required"
    class="text-secondary-dark"
  >
    (*Required)
  </span>
    <span v-else>
      (optional)
    </span>
  </label>
</template>