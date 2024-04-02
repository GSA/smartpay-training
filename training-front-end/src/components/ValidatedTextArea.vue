<script setup>
  import {computed} from 'vue'
  const props = defineProps({
    'modelValue': {
      type: String,
      required: true,
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
    <textarea
      :id="name"
      :v-model="props.modelValue"
      class="usa-textarea tablet:grid-col-12"
      :class="{ 'usa-input--error':validator.$error, 'error-focus': validator.$error }"
      :name="name"
      :aria-describedby="validator.$error? error_id: null"
      :readonly="readonly"
      rows="10"
      @input="$emit('update:modelValue', $event.target.value)"
    />
  </div>    
</template>