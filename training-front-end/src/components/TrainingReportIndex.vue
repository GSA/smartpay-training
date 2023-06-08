<script setup>
  import { ref, onErrorCaptured } from "vue"
  import Loginless from './LoginlessFlow.vue';
  import CertificateTable from "./CertificateTable.vue";
  import CertificateUserTable from "./CertificateUserTable.vue";
  import { useStore } from '@nanostores/vue'
  import { profile} from '../stores/user'
  import USWDSAlert from './USWDSAlert.vue'

  const user = useStore(profile)

  const error = ref()

  function startLoading() {
    error.value = undefined
  }

	function setError(event){
    error.value = event
	}

  onErrorCaptured((err) => {
    setError(err)
    return false
  })
</script>

<template>
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <div class="grid-row">
      <div class="tablet:grid-col-12">
        <USWDSAlert
          v-if="error"
          class="tablet:grid-col-8"
          status="warning"
          :heading="error.name"
        >
          {{ error.message }}
        </USWDSAlert>

        <Loginless
          page-id="pageId"
          title="Training Reprts"
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

          <div class="usa-prose">
            <h2>
              Welcome {{ user.name }}!
            </h2>
            <CertificateUserTable />
            <div class="margin-top-6">
              
            </div>
          </div>
        </Loginless>
      </div>
    </div>
  </div>
</template>