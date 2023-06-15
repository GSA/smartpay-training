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
    console.log(event)
    emit('update:modelValue', event.target.value)
  }
</script>
<template>
  <label class="usa-label" :for="name">{{ label }}</label>
  <div class="usa-combo-box">
    <select class="usa-select" 
      test="hello"
      :name="name"
      :id="name"
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