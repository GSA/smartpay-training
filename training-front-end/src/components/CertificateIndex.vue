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
          class="tablet:grid-col-12"
          status="error"
          :heading="error.name"
        >
          {{ error.message }}
        </USWDSAlert>

        <Loginless
          page-id="certificates"
          title="Access Certificates"
          header="header"
          link-destination-text="your past certificates"
          :allow-registration="false"
          @start-loading="startLoading"
          @error="setError"
        >
          <template #initial-greeting>
            <p>Enter your email address to get access to your previously earned certificates. You'll receive an email with an access link.</p>
          </template>
            
          <template #more-info>
            <h2>Welcome! </h2>
            <p>Before you can access the certificate page, you'll need to create and complete your profile.</p>
          </template>

          <div class="usa-prose">
            <h2>
              Welcome {{ user.name }}!
            </h2>
            <CertificateUserTable />
            <div class="margin-top-6">
              <CertificateTable />
            </div>
          </div>
        </Loginless>
      </div>
    </div>
  </div>
</template>