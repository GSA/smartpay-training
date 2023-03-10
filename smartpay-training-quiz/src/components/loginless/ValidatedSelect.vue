<script setup>

const props = defineProps({
    options: {
            type: Array,
            default: []
    },
    'modelValue': String,
    'isInvalid': Boolean,
    'name': String,
    'label': String,
    'error_message': String
})
</script>
<template>
  <div class="usa-form-group" :class="{ 'usa-form-group--error':isInvalid}">
    <label class="usa-label" :for="name">{{label}}</label>
    <span v-if="isInvalid" class="usa-error-message" :id="error_id" role="alert">
      {{ error_message }}
    </span>
    <select 
      class="usa-select"
      :id="name"
      :name="name"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      >
      <option value disabled>- Select -</option>
      <option v-for="option in options" :value="option">{{option}}</option>
    </select>
  </div>
</template>