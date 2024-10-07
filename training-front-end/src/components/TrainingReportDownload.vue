<script setup>
  import { computed } from "vue"
  import { useStore } from '@nanostores/vue'
  import { profile} from '../stores/user'
  import USWDSAlert from './USWDSAlert.vue'

  const user = useStore(profile)
  const isReportUser = computed(() => user.value.roles.includes('Report'))
  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const report_url = `${base_url}/api/v1/users/download-user-quiz-completion-report`

</script>
<template>
  <section 
    v-if="isReportUser"  
    class="usa-prose"
  >
    <h2>Download Your Report</h2>
    <p>
      We’ve created a report for you in CSV format. You can open it in the spreadsheet 
      application of your choice (e.g. Microsoft Excel, Google Sheets, Apple Numbers).
    </p>
    <form
      :action="report_url"
      method="post"
    >
      <input 
        type="hidden"
        name="jwtToken"
        :value="user.jwt"
      >
      <button
        class="usa-button"
        type="submit"
      >
        Download Report
      </button>
    </form>
  </section>
  <section v-else>
    <USWDSAlert      
      status="error"
      class="usa-alert"
      heading="You are not authorized to receive reports."
    >
      Your email account is not authorized to access training reports. If you should be authorized, you can 
      <a
        class="usa-link"
        href="mailto:gsa_smartpay@gsa.gov"
      >
        contact the GSA SmartPay team
      </a> to gain access.
    </USWDSAlert>
  </section>
</template>