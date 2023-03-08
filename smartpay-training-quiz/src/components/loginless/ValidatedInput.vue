<script setup>
  import {computed} from 'vue'
  const props = defineProps({
    'modelValue': String,
    'isInvalid': Boolean,
    'name': String,
    'label': String,
    'error_message': String
  })
  defineEmits(['update:modelValue'])
  var error_id = computed(() => props.name + '-input-error-message')
</script>

<template>
  <div class="usa-form-group" :class="{ 'usa-form-group--error':isInvalid}">
    <label class="usa-label" :for="name">{{label}}</label>
    <span v-if="isInvalid" class="usa-error-message" :id="error_id" role="alert">
      {{ error_message }}
    </span>
    <input
        class="usa-input usa-input"
        :class="{ 'usa-input--error':isInvalid, 'error-focus': isInvalid }"
        :id="name"
        :name="name"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :aria-describedby="error_id"
    />
  </div>    
</template>