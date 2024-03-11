<script setup>
  import {computed , reactive} from 'vue'  
  
  const props = defineProps({
    'modelValue': {
      type: Date,
      required: false,
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
    'hintText': {
      type: String,
      required: false,
      default: ''
    },
  });

  const emit = defineEmits(['update:modelValue']);

  const error_id = computed(() => props.name + '-input-error-message');

  const user_input = reactive({
    day: '',
    month: '',
    year: ''
  });

  const updateDate = () =>  {
    const year = user_input.year;
    const month = user_input.month;
    const day = user_input.day;
    if (year && month && day) {
      const newDate = new Date(`${year}-${month}-${day}`);
      if (!isNaN(newDate)) {
        emit('update:modelValue', newDate);
      } 
    }
  }
  
</script>
<template>
  <div
    class="usa-form-group"
    :class="{ 'usa-form-group--error':validator.$error}"
  >
    <fieldset class="usa-fieldset">
      <legend class="usa-legend">
        {{ label }}
        <span class="text-secondary-dark">(*Required)</span>
      </legend>
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
            @input="updateDate"
          >
            <option value="">
              - Select -
            </option>
            <option value="1">
              01 - January
            </option>
            <option value="2">
              02 - February
            </option>
            <option value="3">
              03 - March
            </option>
            <option value="4">
              04 - April
            </option>
            <option value="5">
              05 - May
            </option>
            <option value="6">
              06 - June
            </option>
            <option value="7">
              07 - July
            </option>
            <option value="8">
              08 - August
            </option>
            <option value="9">
              09 - September
            </option>
            <option value="10">
              10 - October
            </option>
            <option value="11">
              11 - November
            </option>
            <option value="12">
              12 - December
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