<script setup>
  import {computed} from 'vue'

  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  
  const options = await fetch(`${base_url}/api/v1/agencies`).then((r) => r.json())
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

    <select 
      :id="name"
      class="usa-select"
      :name="name"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
    >
      <option
        disabled
        value=""
        selected
      >
        - Select -
      </option>
      <option
        v-for="option in options"
        :key="option.id"
        :value="option.id"
      >
        {{ option.name }}
      </option>
    </select>
  </div>
</template>