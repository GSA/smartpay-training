<script setup>
  import { ref, reactive } from 'vue';
  import USWDSAlert from './USWDSAlert.vue'
  import ValidatedTextArea from './ValidatedTextArea.vue';
  import ValidatedDatePicker from './ValidatedDatepicker.vue';
  import { useVuelidate } from '@vuelidate/core';
  import { required, helpers } from '@vuelidate/validators';
  import SpinnerGraphic from './SpinnerGraphic.vue'
  import { useStore } from '@nanostores/vue'
  import { profile} from '../stores/user'

  const user = useStore(profile)
  const { withMessage } = helpers
  const base_url = import.meta.env.PUBLIC_API_BASE_URL

  const showSuccessMessage = ref(false)
  const showFailedMessage = ref(false)
  const failedEmailList = ref('')
  const successCount = ref(0)
  const isLoading = ref(false)
  const showSpinner = ref(false)

  const emit = defineEmits(['startLoading', 'endLoading', 'error'])

  const user_input = reactive({
    emailAddresses: undefined,
    certificationExpirationDate: undefined
  })

  const isNotPast = helpers.withParams(
    { type: 'notPast' },
    (value) => {
      const currentDate = new Date();
      const inputDate = new Date(value);
      return inputDate >= currentDate;
    }
  );

  /* Form validation for additional information if we allow registation here */
  const validations_all_info = {
    emailAddresses: {
      required: withMessage('Please enter the email addresses to invite', required)
    },
    certificationExpirationDate: {
      required: withMessage('Please enter the cerification experation date', required),
      isNotPast: withMessage('The date must not be in the past', isNotPast)
    },
  }

  const v_all_info$ = useVuelidate(validations_all_info, user_input)

  async function cancel(){
    isLoading.value = true;
    showSpinner.value = true;

    // Clear out the fields
    user_input.emailAddresses = undefined;
    user_input.certificationExpirationDate = undefined;

    isLoading.value = false;
    showSpinner.value = false;
  }

  async function submitGspcInvites(){
    const validation = v_all_info$
    const isFormValid = await validation.value.$validate()

    if (!isFormValid) {
      showSpinner.value = false;
      return
    }

    emit('startLoading')
    isLoading.value = true;
    showSpinner.value = true;

    const apiURL = new URL(`${base_url}/api/v1/gspc-invite`)

    try {
      let res = await fetch(apiURL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json','Authorization': `Bearer ${user.value.jwt}` },
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

      if (res.status == 200) {
        const data = await res.json();

        if (data.valid_emails.length > 0) {
          showSuccessMessage.value = true;
          successCount.value = data.valid_emails.length;
        } else{
          showSuccessMessage.value = false;
        }
        
        if (data.invalid_emails.length > 0) {
          showFailedMessage.value = true
          failedEmailList.value = data.invalid_emails.join(', ');
        } else{
          showFailedMessage.value = false
        }
      }

      isLoading.value = false
      showSpinner.value = false
      emit('endLoading')
    
    } catch (err) {
      isLoading.value = false
      showSpinner.value = false
      const e = new Error("Sorry, we had an error connecting to the server.")
      e.name = "Server Error"
      emit('endLoading')
      throw e
    }
  }
  
</script>
<template>
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <h2>Send Invitations for GSA SmartPay Program Certification</h2>
    <p>
      After the attendees finish the necessary coursework for the GSA SmartPay Program Certification (GSPC), as stated in Smart Bulletin 22 during the GSA SmartPay Training Forum, you can use the form below to send each attendee an email containing a link. This link will enable them to certify their hands-on experience and obtain a PDF copy of their GSPC.
    </p>
    <p>
      Please fill out the form below by entering the attendees' email addresses as a comma-separated list and selecting an expiration date for their certificate. The expiration date should be three years from the date of the GSA SmartPay Training Forum. This form will verify the entered email addresses and notify you if any are invalid.
    </p>
    <v-form
      ref="form"
      class="usa-form usa-form--large margin-bottom-3"
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
      <div>
        <USWDSAlert
          v-if="showFailedMessage"
          status="error"
          class="usa-alert--slim"
          :has-heading="false"
        >
          Emails failed to send to: {{ failedEmailList }}
        </USWDSAlert>
        <USWDSAlert
          v-if="showSuccessMessage"
          status="success"
          class="usa-alert--slim"
          :has-heading="false"
        >
          Emails successfully sent to {{ successCount }} people.
        </USWDSAlert>
      </div>
      <div class="grid-row grid-gap margin-top-3">
        <div class="grid-col">
          <input
            class="usa-button"
            type="submit"
            value="Send Invitations"
            :disabled="isLoading"
            data-test="submit"
          >
          <button
            id="cancel"
            type="button"
            class="usa-button usa-button--outline"
            :disabled="is_saving"
            @click="cancel"
          >
            Cancel
          </button>
        </div>
        <!--display spinner along with submit button in one row for desktop-->
        <div
          v-if="showSpinner"
          class="display-none tablet:display-block tablet:grid-col-1 tablet:padding-top-3 tablet:margin-left-neg-1"
        >
          <SpinnerGraphic />
        </div>
      </div>
      <!--display spinner under submit button for mobile view-->
      <div
        v-if="showSpinner"
        class="tablet:display-none margin-top-1 text-center"
      >
        <SpinnerGraphic />
      </div>
    </v-form>
  </div>
</template>
<style>
  .usa-textarea {
    height: 15rem;
  }
</style>