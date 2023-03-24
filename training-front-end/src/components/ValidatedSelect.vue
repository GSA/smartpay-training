<script setup>

const options_api = await fetch('http://127.0.0.1:8000/api/v1/agencies/').then((r) => r.json())
const props = defineProps({
    options: {
            type: Array,
            default: ['']
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
      <option disabled value="" selected>- Select -</option>
      <option v-for="option in options_api" :value="option.id" :key="option.id">{{option.name}}</option>
    </select>
  </div>
</template>