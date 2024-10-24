<script setup>
import { onMounted } from 'vue';
import USWDS from "@uswds/uswds/js";
import FormLabel from "./form-components/FormLabel.vue";

  const { comboBox } = USWDS;

  defineProps({
    'modelValue': {
      type: String,
      required: false,
      default: undefined
    },
    items: {
      type: Array,
      required: true
    },
    name: {
      type:String,
      required: true
    },
    label: {
      type: String,
      required: true
    },
    'required': {
      type: Boolean,
      required: false,
      default: false
    },
    'validator': {
      type: Object,
      required: false,
      default: {}
    },
  })
  const emit = defineEmits(['update:modelValue'])
  onMounted(() => {
    comboBox.init();
    
  })
  function selected(event) {
    emit('update:modelValue', event.target.value)
  }
</script>
<template>
  <div
      class="usa-form-group"
      :class="{ 'usa-form-group--error':validator.$error}"
  >
    <FormLabel
        :id="`${name}-label`"
        :for="`${name}`"
        :value="`${ label }`"
        :required="required"
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
  <div class="usa-combo-box" :data-default-value="modelValue">
    <!-- uswds changes the select element in such a way that neither onblur or oninput work -->
    <!-- eslint-disable-next-line vuejs-accessibility/no-onchange -->
    <select 
      :id="name"
      class="usa-select" 
      :name="name"
      :value="modelValue"
      @change="selected"
    >
      <option 
        v-for="item in items" 
        :key="item.id"
        :value="item.id"
      >
        {{ item.name }}
      </option>
    </select>
  </div>
  </div>
</template>