<script setup>
  import { onMounted, watch, ref, nextTick } from 'vue'  
  import USWDS from "@uswds/uswds/js";
  import FormLabel from "./FormLabel.vue"
  const { dateRangePicker }  = USWDS;
  const { datePicker }  = USWDS;
  
  const props = defineProps({
    'modelValue': {
    type: Array,
    default: () => [],
    },
    'hintText': {
      type: String,
      required: false,
      default: 'mm/dd/yyyy'
    },
    'label': {
      type: String,
      required: true
    },
    'name': {
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
      required: true
    },
  });

  const emit = defineEmits(['update:modelValue'])

  // refs for start and end date values
  const startDate = ref('');
  const endDate = ref('');

  // refs for input elements
  const startInputRef = ref(null);
  const endInputRef = ref(null);

  // Initialize start and end dates
  watch(() => props.modelValue, (newVal) => {
    if (Array.isArray(newVal) && newVal.length === 2) {
      // Initialize only if new values are different from the current ones
      if (newVal[0] !== startDate.value || newVal[1] !== endDate.value) {
        startDate.value = newVal[0];
        endDate.value = newVal[1];
      }
    }
  });

  // Emits on value changes
  watch(startDate, (newValue, oldValue) => {
    if (newValue !== oldValue) {
      emit('update:modelValue', [newValue, endDate.value]);
    }
  });

  watch(endDate, (newValue, oldValue) => {
    if (newValue !== oldValue) {
      emit('update:modelValue', [startDate.value, newValue]);
    }
  });

  onMounted(async () => {
    // Ensures DOM is fully rendered for event listeners
    await nextTick()

    // Initialize USWDS Date Range Picker
    datePicker.init() // yes this is needed otherwise it will break USWDS internal javascript
    dateRangePicker.init()

  
    // Attach event listeners for changes in the date inputs as datepicker changes will not directly update the values
    startInputRef.value.addEventListener('change', (event) => {
      emit('update:modelValue', [event.target.value, endDate.value]);
    });

    endInputRef.value.addEventListener('change', (event) => {
      emit('update:modelValue', [startDate.value, event.target.value]);
    });
  });

</script>

<template>
  <div class="usa-date-range-picker">
    <div class="usa-form-group">
      <FormLabel
        :id="`${name}-start-label`"
        :for="`${name}-start`"
        :value="`${ props.label } start`"
        :required="props.required"
      />
      <div
        :id="`${name}-start-hint`"
        class="usa-hint"
      >
        {{ props.hintText }}
      </div>
      <div class="usa-date-picker">
        <input
          :id="`${name}-start`"
          ref="startInputRef"
          v-model="startDate"
          class="usa-input"
          :name="`${name}-start`"
          :aria-labelledby="`${name}-start-label`"
          :aria-describedby="`${name}-start-hint`"
          type="date"
        >
      </div>
    </div>
    <div class="usa-form-group">
      <FormLabel
        :id="`${name}-end-label`"
        :for="`${name}-end`"
        :value="`${ props.label } end`"
        :required="props.required"
      />
      <div
        :id="`${name}-end-hint`"
        class="usa-hint"
      >
        {{ props.hintText }}
      </div>
      <div class="usa-date-picker">
        <input
          :id="`${name}-end`"
          ref="endInputRef"
          v-model="endDate"
          class="usa-input"
          :name="`${name}-end`"
          :aria-labelledby="`${name}-end-label`"
          :aria-describedby="`${name}-end-hint`"
          type="date"
        >
      </div>
    </div>
  </div>
</template>