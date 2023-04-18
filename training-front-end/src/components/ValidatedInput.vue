<script setup>
  import {computed} from 'vue'
  const props = defineProps({
    'modelValue': {
      type: String,
      required: false,
      default: undefined
    },
    'isInvalid': {
      type: Boolean,
      required: true
    },
    'name': {
      type: String,
      required: true
    },
    'label': {
      type: String,
      required: true
    },
    'errorMessage': {
      type: String,
      required: true
    },
    'readonly': {
      type: Boolean,
      required: false,
      default: false
    }
  })
  defineEmits(['update:modelValue'])
  var error_id = computed(() => props.name + '-input-error-message')
</script>

<template>
  <div
    class="usa-form-group"
    :class="{ 'usa-form-group--error':isInvalid}"
  >
    <label
      class="usa-label"
      :for="name"
    >{{ label }}</label>
    <span
      v-if="isInvalid"
      :id="error_id"
      class="usa-error-message"
      role="alert"
    >
      {{ errorMessage }}
    </span>
    <input
      :id="name"
      class="usa-input usa-input"
      :class="{ 'usa-input--error':isInvalid, 'error-focus': isInvalid }"
      :name="name"
      :value="modelValue"
      :aria-describedby="error_id"
      :readonly="readonly"
      @input="$emit('update:modelValue', $event.target.value)"
    >
  </div>    
</template>