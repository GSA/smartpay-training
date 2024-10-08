<script setup>
  import { useStore } from '@nanostores/vue'
  import { profile} from '../stores/user'
  import { computed } from "vue"
  import USWDSAlert from './USWDSAlert.vue'

  const user = useStore(profile)
  const isAdminUser = computed(() => user.value.roles.includes('Admin'))

  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const gspc_report_url = `${base_url}/api/v1/gspc/download-gspc-completion-report`

  async function downloadGspcReport() {

            const response = await fetch( gspc_report_url, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${user.value.jwt}` },
            });

            if (response.ok) {
                const blob = await response.blob();
                downloadBlobAsFile(blob, 'GspcCompletionReport.csv')
            } else {
                console.error('Failed to download report', response.statusText);
            }
        }

  async function downloadBlobAsFile(blob, filename){
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
  }


</script>
<template>
  <section 
    v-if="isAdminUser"  
    class="usa-prose"
  >
    <h2>Download GSPC Report</h2>
    <p>
      We’ve created a report for you in CSV format. You can open it in the spreadsheet 
      application of your choice (e.g. Microsoft Excel, Google Sheets, Apple Numbers).
    </p>
    <button
      class="usa-button"
      @click="downloadGspcReport"
    >
      Download Report
    </button>
  </section>
  <section v-else>
    <USWDSAlert      
      status="error"
      class="usa-alert"
      heading="You are not authorized to receive reports."
    >
      Your email account is not authorized to access admin reports. If you should be authorized, you can 
      <a
        class="usa-link"
        href="mailto:gsa_smartpay@gsa.gov"
      >
        contact the GSA SmartPay team
      </a> to gain access.
    </USWDSAlert>
  </section>
</template>