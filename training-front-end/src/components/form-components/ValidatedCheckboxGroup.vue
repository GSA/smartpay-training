<script setup>
import { ref } from 'vue';
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
const localCheckedValues = ref([]);

function checkAll(){
   for (const option of props.options) {
     if (!localCheckedValues.value.includes(option.value)) {
       localCheckedValues.value.push(option.value)
     }
   }
  emit('update:modelValue', localCheckedValues);
}

function deselectAll(){
  localCheckedValues.value = [];
  emit('update:modelValue', localCheckedValues);
}

function handleCheckboxChange(){
  emit('update:modelValue', localCheckedValues); // Emit updated values
}
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
    <button 
        class="usa-button usa-button--hover margin-bottom-2"
        type="button"
        @click="checkAll">
      Select All
    </button>
    <button 
        class="usa-button usa-button--hover margin-bottom-2"
        type="button"
        @click="deselectAll">
      Deselect All
    </button>
    <div
      v-for="option in options"
      :key="option.value"
      class="usa-checkbox"
    >
      <input
        :id="option.value"
        type="checkbox"
        :value="option.value"
        v-model="localCheckedValues"
        class="usa-checkbox__input"
        :checked="localCheckedValues.includes(option.value)"
        @change="handleCheckboxChange()"
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
