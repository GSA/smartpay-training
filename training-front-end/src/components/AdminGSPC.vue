<script setup>
  import { reactive } from 'vue';
  import USWDSAlert from './USWDSAlert.vue'
  import ValidatedTextArea from './ValidatedTextArea.vue';
  import ValidatedDatePicker from './ValidatedDatePicker.vue';
  import { useVuelidate } from '@vuelidate/core';
  import { required, email, helpers } from '@vuelidate/validators';

  const { withMessage } = helpers

  // const props = defineProps({
  //   'emailAddresses': {
  //     type: String,
  //     required: true
  //   },
  //   'certificationExpirationDate': {
  //     type: Date,
  //     required: true
  //   },
  // })

  const emit = defineEmits(['startLoading', 'endLoading', 'error'])

  const user_input = reactive({
    emailAddresses: undefined,
    certificationExpirationDate: undefined
  })

  /* Form validation for additional information if we allow registation here */
  const validations_all_info = {
    emailAddresses: {
      required: withMessage('Please enter your full name', required)
    },
    certificationExpirationDate: {
      required: withMessage('Please enter your agency', required),
    },
  }
  const v_all_info$ = useVuelidate(validations_all_info, user_input)


</script>

<template>
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <h2>GSPC Send Email Notifications</h2>
    <p>
      Content here duis vulputate pellentesque commodo. Nullam congue nibh a diam porta, at tincidunt mi pellentesque. Curabitur at mollis erat. Pellentesque ultricies libero sem, sed ornare nisl faucibus sit amet. In vel dictum tortor. Nullam iaculis efficitur ipsum. Quisque pharetra euismod augue et placerat.
    </p>
    <p>
      Duis congue, eros eu volutpat suscipit, odio dui varius nisi, id bibendum ipsum nisi at libero. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer felis velit, sollicitudin a leo sagittis, iaculis efficitur turpis. Vivamus id mi sed sapien facilisis consequat pulvinar sed orci. Morbi tellus quam, consectetur in aliquet eu, auctor id urna.
    </p>
    <form
      class="usa-form usa-form--large margin-bottom-3 "
      data-test="gspc-form"
      @submit.prevent="start_email_flow"
    >
      <ValidatedTextArea
        v-model="user_input.emailAddresses"
        client:load
        :validator="v_all_info$.emailAddresses"
        label="Email Addresses of GSA SmartPay Forum Attendees"
        name="email-list"
      />
      <ValidatedDatePicker
        v-model="user_input.certificationExpirationDate"
        client:load
        :validator="v_all_info$.certificationExpirationDate"
        label="Certification Expiration Date"
        name="certification-expiration-date"
        hint-text="For example: January 19 2000"
      />
      <button 
        class="usa-button"
        type="submit"
      >
        <span class="usa-search__submit-text">
          Search
        </span>
      </button>
    </form>
  </div>
</template>