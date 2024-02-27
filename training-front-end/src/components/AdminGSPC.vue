<script setup>
  import { reactive, onMounted } from 'vue';
  import USWDSAlert from './USWDSAlert.vue'
  import ValidatedTextArea from './ValidatedTextArea.vue';
  import ValidatedDatePicker from './ValidatedDatepicker.vue';
  import { useVuelidate } from '@vuelidate/core';
  import { required, email, helpers } from '@vuelidate/validators';
  import { getUserFromToken } from '../stores/user'

  const { withMessage } = helpers
  const base_url = import.meta.env.PUBLIC_API_BASE_URL

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
      required: withMessage('Please enter the email addresses to invite', required)
    },
    certificationExpirationDate: {
      required: withMessage('Please enter the cerification experation date', required),
    },
  }
  const v_all_info$ = useVuelidate(validations_all_info, user_input)

  async function submitGspcInvites(){
    const apiURL = new URL(`${base_url}/api/v1/gspc-invite`)

    try {
      console.log('certificationExpirationDate value:')
      console.log(user_input.certificationExpirationDate)

      let res = await fetch(apiURL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email_addresses: user_input.emailAddresses,
          certification_expiration_date: user_input.certificationExpirationDate
        })
      });

    if (!res.ok) {
      if (res.status == 401) {
        throw new Error("Unauthorized")
      }
      throw new Error("Error contacting server")
    }

      const data = await res.json();
      console.log('Server response:', data); // Logging the server response


    // Handle response as needed
  } catch (err) {
    // Handle errors
  }
  }
  
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
      @submit.prevent="submitGspcInvites"
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
          Submit
        </span>
      </button>
    </form>
  </div>
</template>