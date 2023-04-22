<script setup>
  import { ref, onMounted } from "vue"
  import Loginless from './LoginlessFlow.vue';
  import CertificateTable from "./CertificateTable.vue";
  import { useStore } from '@nanostores/vue'
  import { profile} from '../stores/user'
  // import USWDSAlert from './USWDSAlert.vue'

  const user = useStore(profile)
  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const certificates = ref([]) 
  onMounted(async() => {
    certificates.value = await fetch(`${base_url}/api/v1/certificates/${user.value.id}`).then((r) => r.json())
    console.log(certificates)

  })
  const error = ref()

  function startLoading() {
    error.value = undefined
  }

	function setError(event){
    console.log(event)
    error.value = event
	}
</script>

<template>
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <div class="grid-row">
      <div class="tablet:grid-col-12">
        <Loginless
          page-id="pageId"
          title="Access Certificates"
          header="header"
          :allow-registration="false"
          @start-loading="startLoading"
          @error="setError"
        >
          <template #initial-greeting>
            <p>Enter your email address to get access to your previously earned certificates. You'll receive an email with an access link.</p>
          </template>
            
          <template #more-info>
            <h2>Welcome ! </h2>
            <p>Before you can access the certificate page, you'll need to create and complete your profile.</p>
          </template>

          <div>
            <h2>
              Welcome {{ user.name }}!
            </h2>
            <CertificateTable :certificates="certificates" />
          </div>
        </Loginless>
      </div>
    </div>
  </div>
</template>