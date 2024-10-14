<script setup>
import { computed } from 'vue';
import FormLegend from './FormLegend.vue';

const props = defineProps({
  legend: {
    type: String,
    default: 'Choose Options',
  },
  modelValue: {
    type: Array,
    default: () => [],
  },
  options: {
    type: Array,
    required: true,
    default: () => [],
  },
  required: {
    type: Boolean,
    default: false,
  },
  validator: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['update:modelValue']);

// Create a computed property for two-way binding with v-model
const localCheckedValues = computed({
  get: () => props.modelValue,
  set: (newValues) => {
    emit('update:modelValue', newValues);
  },
});
</script>

<template>
  <fieldset class="usa-fieldset">
    <FormLegend
      :value="legend"
      :required="required"
    />
    <span v-if="validator.$error">
      <span
        v-for="error in validator.$errors"
        :key="error.$property"
        class="usa-error-message"
        role="alert"
      >
        {{ error.$message }}
      </span>
    </span>
    <div
      v-for="option in options"
      :key="option.value"
      class="usa-checkbox"
    >
      <input
        :id="option.value"
        type="checkbox"
        :value="option.value"
        class="usa-checkbox__input"
        :checked="localCheckedValues.includes(option.value)"
        @change="(event) => {
          if (event.target.checked) {
            localCheckedValues.push(option.value); // Add the value if checked
          } else {
            const index = localCheckedValues.indexOf(option.value);
            if (index > -1) {
              localCheckedValues.splice(index, 1); // Remove the value if unchecked
            }
          }
          emit('update:modelValue', localCheckedValues); // Emit updated values
        }"
      >
      <label
        class="usa-checkbox__label"
        :for="option.value"
      >
        {{ option.label }}
      </label>
    </div>
  </fieldset>
</template>
