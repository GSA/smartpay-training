<script setup>
  import { ref } from "vue"
  import Loginless from './LoginlessFlow.vue';
  import { useStore } from '@nanostores/vue'
  import { profile} from '../stores/user'
  import USWDSAlert from './USWDSAlert.vue'

  const user = useStore(profile)
  const base_url = import.meta.env.PUBLIC_API_BASE_URL

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
                Welcome {{user.name}}!
              </h2>
              <h3>
                Account Details
              </h3>
              <h3>
                Certificates
              </h3>
              <h3>
                Available Trainings
              </h3>
            </div>
          </Loginless>
        </div>
      </div>
  </div>
</template>