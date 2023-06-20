<script setup>
  import { ref, onErrorCaptured } from "vue"
  import Loginless from './LoginlessFlow.vue';
  import TrainingReportDownload from "./TrainingReportDownload.vue";
  import USWDSAlert from './USWDSAlert.vue'

  const error = ref()

  function startLoading() {
    error.value = undefined
  }

	function setError(event){
    error.value = event
	}

  onErrorCaptured((err) => {
    if (err.message == 'Unauthorized'){
      err = {
        name: 'You are not authorized to receive reports.',
        message: 'Your email account is not authorized to access training reports. If you should be authorized, you can <a class="usa-link" href="mailto:gsa_smartpay@gsa.gov">contact the SmartPay team</a> to gain access.'
      }
      setError(err)
    }
    return false
  })
</script>

<template>
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <div class="grid-row">
      <div class="tablet:grid-col-12">
        <USWDSAlert
          v-if="error"
          class="tablet:grid-col-12 margin-bottom-4"
          status="error"
          :heading="error.name"
        >
          <!-- eslint-disable-next-line vue/no-v-html -->
          <span v-html="error.message" />
        </USWDSAlert>

        <Loginless
          page-id="training_reports"
          title="Training Reports"
          header="header"
          link-destination-text="the training reports you are eligible to receive"
          :allow-registration="false"
          @start-loading="startLoading"
          @error="setError"
        >
          <template #initial-greeting>
            <h2>Confirm your email to gain report access</h2>
            <p>Enter your email address to get access to reports. You'll receive an email with an access link.</p>
          </template>
            
          <template #more-info>
            <h2>Welcome! </h2>
            <p>Before you can access reports, you'll need to create and complete your profile.</p>
          </template>

          <TrainingReportDownload />
        </Loginless>
      </div>
    </div>
  </div>
</template>