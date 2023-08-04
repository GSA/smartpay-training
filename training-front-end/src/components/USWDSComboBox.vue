<script setup>
  import { onMounted } from 'vue';
  import USWDS from "@uswds/uswds/js";
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
    }
  })
  const emit = defineEmits(['update:modelValue'])
  onMounted(() => {
    comboBox.init()
  })
  function selected(event) {
    emit('update:modelValue', event.target.value)
  }
</script>
<template>
  <label
    class="usa-label"
    :for="name"
  >
    {{ label }}
  </label>
  <div class="usa-combo-box">
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
</template>