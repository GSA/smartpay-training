<script setup>
  import { ref, onErrorCaptured } from "vue"
  import { useStore } from '@nanostores/vue'
  import { profile} from '../stores/user'
  import { computed } from "vue"
  import AdminReportDownload from "./AdminReportGSPC.vue";
  import USWDSAlert from './USWDSAlert.vue'

  const error = ref()
  const user = useStore(profile)
  const isAdminUser = computed(() => user.value.roles.includes('Admin'))


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
  <section 
    v-if="isAdminUser"  
    class="usa-prose"
  >
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
          <ul class="usa-card-group">
            <AdminReportDownload />
            <li class="usa-card tablet:grid-col-12">
              <div class="usa-card__container">
                <div class="usa-card__header">
                  <h4 class="usa-card__heading">
                    Report 01
                  </h4>
                </div>
                <div class="usa-card__body">
                  <p>
                    We’ve created a report for you in CSV format. You can open it in the spreadsheet 
                    application of your choice (e.g. Microsoft Excel, Google Sheets, Apple Numbers).
                  </p>
                </div>         
                <div class="usa-card__footer">
                  <a
                    href="./report01/"
                    class="card_link usa-button"
                  >
                    Access Report
                  </a>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
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