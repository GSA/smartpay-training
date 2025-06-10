<script setup>
  import {ref, reactive, computed} from 'vue';
  import USWDSAlert from './USWDSAlert.vue'
  import ValidatedTextArea from './form-components/ValidatedTextArea.vue';
  import ValidatedMemorableDatepicker from './form-components/ValidatedMemorableDatepicker.vue';
  import { useVuelidate } from '@vuelidate/core';
  import { required, helpers } from '@vuelidate/validators';
  import SpinnerGraphic from './SpinnerGraphic.vue'
  import { RepositoryFactory } from "./RepositoryFactory.vue";
  import { useStore } from "@nanostores/vue";
  import { profile } from "../stores/user.js";
  
  const adminRepository = RepositoryFactory.get('admin')
  const { withMessage } = helpers

  const user = useStore(profile)
  const isAdminUser = computed(() => user.value.roles.includes('Admin'))
  const showSuccessMessage = ref(false)
  const showFailedMessage = ref(false)
  const showFollowUpSuccessMessage = ref(false)
  const failedEmailList = ref('')
  const successCount = ref(0)
  const isLoading = ref(false)
  const showSpinner = ref(false)

  const user_input = reactive({
    emailAddresses: "",
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

  /* Form validation for additional information if we allow registration here */
  const validations_all_info = {
    emailAddresses: {
      required: withMessage('Please enter the email addresses to invite', required)
    },
    certificationExpirationDate: {
      required: withMessage('Please enter the certification expiration date', required),
      isNotPast: withMessage('The date must not be in the past', isNotPast)
    },
  }

  const v_all_info$ = useVuelidate(validations_all_info, user_input)

  async function startLoading() {
    isLoading.value = true;
    showSpinner.value = true;
  }

  async function endLoading() {
    isLoading.value = false;
    showSpinner.value = false;
  }

  async function cancel() {
    startLoading()

    // Clear out the fields
    user_input.emailAddresses = "";
    user_input.certificationExpirationDate = undefined;

    endLoading()
  }

  async function sendGspcFollowUps() {
    startLoading()

    // reset result message
    showFollowUpSuccessMessage.value = false;

    try {
      // send request
      await adminRepository.sendGspcFollowUps()

      showFollowUpSuccessMessage.value = true;
    } catch {
      throw new Error("Sorry, we had an error connecting to the server.", { name: "Server Error" })
    }

    endLoading()
  }

  async function submitGspcInvites() {
    startLoading()

    // reset result messages 
    showSuccessMessage.value = false;
    showFailedMessage.value = false;

    // validate form
    const validation = v_all_info$
    const isFormValid = await validation.value.$validate()

    if (!isFormValid) {
      endLoading()
      return
    }

    try {
      // send request
      let data = await adminRepository.sendGspcInvites(user_input.emailAddresses, user_input.certificationExpirationDate)

      // display results
      if (data.valid_emails.length > 0) {
        successCount.value = data.valid_emails.length;
        showSuccessMessage.value = true;
      }

      if (data.invalid_emails.length > 0) {
        failedEmailList.value = data.invalid_emails.join(', ');
        showFailedMessage.value = true
      }
    } catch {
      throw new Error("Sorry, we had an error connecting to the server.", { name: "Server Error" })
    }

    endLoading()
  }

  async function handlePaste(){
      // Let the paste happen normally, then format automatically
      setTimeout(() => {
        formatTextArea();
      }, 100);
  }

  async function formatTextArea(){
    if (!(user_input.emailAddresses)) return;
    
    // Detect if this looks like an Excel paste
    // Excel pastes often have repeated items with no separators or just spaces
    const text = user_input.emailAddresses.trim();
    const lines = text.split(/\s+/);
    
    if (lines.length > 1) {
      user_input.emailAddresses = lines
        .filter(line => line.trim() !== '')
        .map(line => line.replace(/,$/, '').trim()) // Remove trailing comma if it already exists
        .join(', ');
    }
  }
</script>
<template>
  <section
      v-if="isAdminUser"
      class="usa-prose"
  >
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <ul class="usa-card-group">
      <li class="usa-card tablet:grid-col-12">
        <div class="usa-card__container">
          <div class="usa-card__header">
            <h2 class="usa-card__heading">
              Send Invitations for GSA SmartPay Program Certification
            </h2>
          </div>
          <div class="usa-card__body">
            <p>
              After the attendees finish the necessary coursework for the GSA SmartPay Program Certification (GSPC), as
              stated in Smart Bulletin 22 during the GSA SmartPay Training Forum, you can use the form below to send
              each attendee an email containing a link. This link will enable them to certify their hands-on experience
              and obtain a PDF copy of their GSPC.
            </p>
            <p>
              Please fill out the form below by entering the attendees' email addresses as a comma-separated list and
              selecting an expiration date for their certificate. The expiration date should be three years from the
              date of the GSA SmartPay Training Forum. This form will verify the entered email addresses and notify you
              if any are invalid.
            </p>
            <form
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
                :required="true"
                @update:paste="handlePaste"
              />
              <ValidatedMemorableDatepicker
                v-model="user_input.certificationExpirationDate"
                client:load
                :validator="v_all_info$.certificationExpirationDate"
                label="Certification Expiration Date"
                name="certification-expiration-date"
                hint-text="For example: January 19 2000"
                :required="true"
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
                  Emails sending to {{ successCount }} people.
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
                    :disabled="isLoading"
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
            </form>
          </div>
        </div>
      </li>
      <li class="usa-card tablet:grid-col-12">
        <div class="usa-card__container">
          <div class="usa-card__header">
            <h2 class="usa-card__heading">
              Send Follow Ups for GSA SmartPay Program Certification
            </h2>
          </div>
          <div class="usa-card__body">
            <p>
              Sends out follow up GSPC invite emails to users who have
              <ul>
                <li>Received the original GSPC invite within the last 6 months</li>
                <li>Hasn't already completed the GSPC survey</li>
                <li>Hasn't already received both follow up notifications</li>
                <li>Hasn't received the last GSPC email within 12 hours</li>
              </ul>
            </p>
            <p>
              The system will send the subsequent needed notification based on the last one received by the user.
            </p>
            <div>
              <USWDSAlert
                v-if="showFollowUpSuccessMessage"
                status="success"
                class="usa-alert--slim"
                :has-heading="false"
              >
                Sending out GSPC follow up emails.
              </USWDSAlert>
            </div>
            <div class="grid-row grid-gap margin-top-3">
              <div class="grid-col">
                <button
                  id="send-out-follow-ups"
                  type="button"
                  class="usa-button"
                  :disabled="isLoading"
                  @click="sendGspcFollowUps"
                >
                  Send Out Follow Ups
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
            <div
              v-if="showSpinner"
              class="tablet:display-none margin-top-1 text-center"
            >
              <SpinnerGraphic />
            </div>
          </div>
        </div>
      </li>
    </ul>
  </div>
  </section>
  <section v-else>
    <USWDSAlert
        status="error"
        class="usa-alert"
        heading="You are not authorized to GSPC."
    >
      Your email account is not authorized to access this page. If you should be authorized, you can
      <a
          class="usa-link"
          href="mailto:gsa_smartpay@gsa.gov"
      >
        contact the GSA SmartPay team
      </a> to gain access.
    </USWDSAlert>
  </section>
</template>
<style>
.usa-textarea {
  height: 15rem;
}
</style>