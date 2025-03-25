<script setup>
  import {computed} from 'vue'
  import FormLabel from "./FormLabel.vue"

  const props = defineProps({
    'label': {
      type: String,
      required: true
    },
    'modelValue': {
      type: String,
      required: true,
      default: undefined
    },
    'name': {
      type: String,
      required: true
    },
    'readonly': {
      type: Boolean,
      required: false,
      default: false
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

  defineEmits(['update:modelValue', 'update:paste'])
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
    <textarea
      :id="name"
      :value="modelValue"
      class="usa-textarea tablet:grid-col-12"
      :class="{ 'usa-input--error':validator.$error, 'error-focus': validator.$error }"
      :name="name"
      :aria-describedby="validator.$error? error_id: null"
      :readonly="readonly"
      rows="10"
      @paste="$emit('update:paste', $event.target.value)"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>    
</template>