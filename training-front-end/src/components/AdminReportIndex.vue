<script setup>
  import { ref, onErrorCaptured } from "vue"
  import AdminReportDownload from "./AdminReportDownload.vue";
  import USWDSAlert from './USWDSAlert.vue'

  const error = ref()


	function setError(event){
    error.value = event
	}

  onErrorCaptured((err) => {
    if (err.message == 'Unauthorized'){
      err = {
        name: 'You are not authorized to receive admin reports.',
        message: 'Your email account is not authorized to access admin reports. If you should be authorized, you can <a class="usa-link" href="mailto:gsa_smartpay@gsa.gov">contact the GSA SmartPay® team</a> to gain access.'
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
        <AdminReportDownload />
      </div>
    </div>
  </div>
</template>