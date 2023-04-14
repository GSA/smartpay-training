<script setup>
  import {computed} from 'vue'

  const base_url = import.meta.env.PUBLIC_API_BASE_URL

  const options = await fetch(`${base_url}/api/v1/agencies`).then((r) => r.json())

  const props = defineProps({
      'modelValue': String,
      'isInvalid': Boolean,
      'name': String,
      'label': String,
      'error_message': String
  })

  var error_id = computed(() => props.name + '-input-error-message')
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
      <option v-for="option in options" :value="option.id" :key="option.id">{{option.name}}</option>
    </select>
  </div>
</template>