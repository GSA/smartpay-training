<script setup>
  import {computed} from 'vue'
  import FormLabel from "./FormLabel.vue"
  
  const props = defineProps({
    'label': {
      type: String,
      required: true
    },
    'modelValue': {
      type: [String, Number],
      required: false,
      default: undefined
    },
    'name': {
      type: String,
      required: true
    },
    'options': {
      type: Array,
      required: true
    },
    'required': {
      type: Boolean,
      required: false,
      default: false
    },
    'validator': {
      type: Object,
      required: true
    },
  })
  
  defineEmits(['update:modelValue'])

  var error_id = computed(() => props.name + '-input-error-message')
</script>
<template>
  <div
    class="usa-form-group"
    :class="{ 'usa-form-group--error':validator.$error}"
  >
    <FormLabel
      :id="`${name}-label`"
      :for="`${name}`"
      :value="`${ props.label }`"
      :required="props.required"
    />
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
        :disabled="required ? '' : disabled"
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