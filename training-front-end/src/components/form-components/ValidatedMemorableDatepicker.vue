<script setup>
  import {computed , reactive, watch} from 'vue'
  import FormLegend from './FormLegend.vue';
  
  const props = defineProps({
    'hintText': {
      type: String,
      required: false,
      default: ''
    },
    'label': {
      type: String,
      required: true
    },
    'modelValue': {
      type: Date,
      required: false,
      default: undefined
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
  
  const options = [
    { txt: '- Select -', value: ""},
    { txt: '01 - January', value: 0 },
      { txt: '02 - February', value: 1 },
      { txt: '03 - March', value: 2 },
      { txt: '04 - April', value: 3 },
      { txt: '05 - May', value: 4 },
      { txt: '06 - June', value: 5 },
      { txt: '07 - July', value: 6 },
      { txt: '08 - August', value: 7 },
      { txt: '09 - September', value: 8 },
      { txt: '10 - October', value: 9 },
      { txt: '11 - November', value: 10 },
      { txt: '12 - December', value: 11 }
    ]

  const emit = defineEmits(['update:modelValue']);

  const error_id = computed(() => props.name + '-input-error-message');

  const user_input = reactive({
    day: '',
    month: '',
    year: ''
  });

  const updateMonth = (selectedValue) => {
    user_input.month = selectedValue;
    updateDate()
  }

  const updateDate = () =>  {
    const year = user_input.year;
    const month = user_input.month;
    const day = user_input.day;
    if (year.length == 4 && month && day) {
      const newDate = new Date(year, month, day, '00', '00', '00');
      if (!isNaN(newDate)) {
        emit('update:modelValue', newDate);
      } 
    }
  }

  watch(() => props.modelValue, (newValue) => {
    const newDate = new Date(newValue);
    if (!isNaN(newDate)) {
      user_input.day = String(newDate?.getDate())
      user_input.month = newDate?.getMonth()
      user_input.year = String(newDate?.getFullYear())
    } else{
      user_input.day = '';
      user_input.month = '';
      user_input.year = '';
    }
  });
  
</script>
<template>
  <div
    class="usa-form-group"
    :class="{ 'usa-form-group--error':validator.$error}"
  >
    <fieldset class="usa-fieldset">
      <FormLegend
        :value="`${ props.label }`"
        :required="props.required"
      />
      <span 
        v-if="hintText !== ''"
        id="mdHint"
        class="usa-hint"
      >
        {{ hintText }}
      </span>
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
      <div class="usa-memorable-date">
        <div class="usa-form-group usa-form-group--month usa-form-group--select">
          <label 
            class="usa-label" 
            :for="props.name + '-month'"
          >
            Month
          </label>
          <select 
            :id="props.name + '-month'"
            v-model="user_input.month"
            class="usa-select" 
            :name="props.name + '-month'"
            aria-describedby="mdHint"
            :required="validator.$dirty"
            @change="updateMonth($event.target.value)"
          >
            <option
              v-for="option in options" 
              :key="option.value"
              :value="option.value"
            >
              {{ option.txt }}
            </option>
          </select>
        </div>
        <div class="usa-form-group usa-form-group--day">
          <label 
            class="usa-label" 
            :for="props.name + '-day'"
          >
            Day
          </label>
          <input 
            :id="props.name + '-day'"
            v-model="user_input.day"
            class="usa-input" 
            aria-describedby="mdHint" 
            :name="props.name + '-day'"
            maxlength="2" 
            pattern="[0-9]*" 
            inputmode="numeric" 
            :required="validator.$dirty" 
            @input="updateDate"
          >
        </div>
        <div class="usa-form-group usa-form-group--year">
          <label 
            class="usa-label" 
            :for="props.name + '-year'"
          >
            Year
          </label>
          <input 
            :id="props.name + '-year'"
            v-model="user_input.year"
            class="usa-input" 
            aria-describedby="mdHint" 
            :name="props.name + '-year'" 
            minlength="4" 
            maxlength="4" 
            pattern="[0-9]*" 
            inputmode="numeric" 
            :required="validator.$dirty"
            @input="updateDate"
          >
        </div>
      </div>
    </fieldset>
  </div>
</template>