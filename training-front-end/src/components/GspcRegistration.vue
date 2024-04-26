<script setup>
  import { ref, onErrorCaptured, onBeforeMount } from 'vue';
  import { useStore } from '@nanostores/vue'
  import { profile} from '../stores/user'
  import USWDSAlert from './USWDSAlert.vue'
  import Loginless from './LoginlessFlow.vue';
  import GspcQuestions from './GspcQuestions.vue';

  onErrorCaptured((err) => {
    setError(err)
    return false
  })

  const user = useStore(profile)
  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const quiz = ref()
  const userSelections = ref([])
  const error = ref()
  let expirationDate = ""

  onBeforeMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    expirationDate = 'expirationDate=' + urlParams.get('expirationDate')
  })

  function startLoading() {
    error.value = undefined
  }

	function setError(event){
    error.value = event
	}

  async function submitGspcRegistration(user_answers) {
    userSelections.value = user_answers
    const url = `${base_url}/api/v1/gspc/submission`
    
    let res
    
    try {
      res = await fetch(url, { 
        method: "POST", 
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.value.jwt}`
        },
        body:  JSON.stringify( {'responses': user_answers}) 
      })
    } catch(e) {
      const err = new Error("There was a problem connecting with the server")
      err.name = "Server Error"
      setError(err)
      return 
    }
    if (!res.ok){
      // non 2xx response from server
      // TODO: this could happen with an expired jwt
      // should offer solution for user in that case.
      const e = new Error("There was a problem connecting with the server")
      e.name = "Server Error"
      setError(e)
    }
    
    quizResults.value = await res.json()
    isStarted.value = false
    isSubmitted.value = true
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
              link-destination-text="the GSA SmartPay Program Certification (GSPCS)"
              :parameters="expirationDate"
              @start-loading="startLoading"
              @error="setError"
            >
              <template #initial-greeting>
                <h2>Verify GSPC coursework and experience</h2>
                <p>Enter your email address to get access to verify your coursework and experience to receive your GSA SmartPay Program Certification (GSPC). You'll receive an email with an access link.</p>
              </template>
              
              <template #more-info>
                <h2>Welcome!</h2>
                <p>Before verifying your GSPC coursework and experience, you'll need to create and complete your profile.</p>
              </template>

              <GspcQuestions
                :expiration-date="expirationDate"
                @submit-gspc-registration="submitGspcRegistration"
              />
            </Loginless>
          </Suspense>
        </div>
      </div>
    </div>
  </div>
</template>