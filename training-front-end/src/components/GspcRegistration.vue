<script setup>
  import { ref, onErrorCaptured, onBeforeMount } from 'vue';
  import USWDSAlert from './USWDSAlert.vue'
  import Loginless from './LoginlessFlow.vue';

  onErrorCaptured((err) => {
    setError(err)
    return false
  })

  let expirationDate = ""

  onBeforeMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    expirationDate = urlParams.get('expirationDate')
    console.log(expirationDate)
  })


	const error = ref()


  function startLoading() {
    error.value = undefined
  }

	function setError(event){
    error.value = event
	}
</script>

<template>
  <div 
    class="padding-top-4 padding-bottom-4" 
    :class="{'bg-base-lightest': isStarted && !isSubmitted}"
  >
    <div
      class="grid-container"
      data-test="post-submit"
    >
      <div class="grid-row">
        <div class="tablet:grid-col-12">
          <USWDSAlert
            v-if="error"
            class="tablet:grid-col-8"
            status="error"
            :heading="error.name"
          >
            {{ error.message }}
          </USWDSAlert>
          <Suspense>
            <template #fallback>
              …Loading
            </template>
            <Loginless
              page-id="gspc_registration"
              title="gspc_registration"
              :header="header"
              link-destination-text="GSPC Registration"
              :parameters="expirationDate"
              @start-loading="startLoading"
              @error="setError"
            >
              <template #initial-greeting>
                <h2>GSPC Registration</h2>
                <p>Enter your email address to login. You'll receive an email with an access link.</p>
              </template>
              
              <template #more-info>
                <h2>Welcome!</h2>
                <p>Before you can register for GSPC, you'll need to create and complete your profile.</p>
              </template>

              <h2>GSPC Placeholder</h2>
              <p>logged in</p>
            </Loginless>
          </Suspense>
        </div>
      </div>
    </div>
  </div>
</template>