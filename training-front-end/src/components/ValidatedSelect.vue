<script setup>
  import {computed} from 'vue'  
  
  const props = defineProps({
    'modelValue': {
      type: String,
      required: false,
      default: undefined
    },
    'validator': {
      type: Object,
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
    'options': {
      type: Array,
      required: true
    }
  })
  
  defineEmits(['update:modelValue'])

  var error_id = computed(() => props.name + '-input-error-message')
</script>
<template>
  <div
    class="usa-form-group"
    :class="{ 'usa-form-group--error':validator.$error}"
  >
    <label
      class="usa-label"
      :for="name"
    >{{ label }} <span class="text-secondary-dark">(*Required)</span></label>
    <span v-if="validator.$error">
      <span
        v-for="error in validator.$errors"
        :id="error_id"
        :key="error.$property"
        class="usa-error-message"
        role="alert"
      >
        {{ error.$message }}
      </span>
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