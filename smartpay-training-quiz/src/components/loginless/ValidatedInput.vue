<script setup>
  import {computed} from 'vue'
  const props = defineProps({
    'modelValue': String,
    'isValid': Boolean,
    'name': String,
    'label': String,
    'error_message': String
  })
  defineEmits(['update:modelValue'])
  var error_id = computed(() => props.name + '-input-error-message')
</script>

<template>
  <div class="usa-form-group" :class="{ 'usa-form-group--error':isValid}">
    <label class="usa-label" :for="name">{{label}}</label>
    <span v-if="isValid" class="usa-error-message" :id="error_id" role="alert">
      {{ error_message }}
    </span>
    <input
        class="usa-input usa-input"
        :class="{ 'usa-input--error':isValid, 'error-focus': isValid }"
        :id="name"
        :name="name"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :aria-describedby="error_id"
    />
  </div>    
</template>