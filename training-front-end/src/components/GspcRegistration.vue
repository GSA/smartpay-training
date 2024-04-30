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
  const certPassed = ref(false)
  const certFailed = ref(false)
  const error = ref()
  let redirectExpirationDateString = ""
  let expirationDate = ""

  onBeforeMount(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    expirationDate = urlParams.get('expirationDate')
    redirectExpirationDateString = 'expirationDate=' + expirationDate
  })

  function startLoading() {
    error.value = undefined
  }

	function setError(event){
    error.value = event
	}

  function downloadCert(){
    //console.log('todo')
	}

  async function submitGspcRegistration(user_answers) {
    const url = `${base_url}/api/v1/gspc/submission`
   
    let res
    
    try {
      res = await fetch(url, { 
        method: "POST", 
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.value.jwt}`
        },
        body:  JSON.stringify( {'responses': user_answers, 'expiration_date': expirationDate}) 
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
    var result = await res.json()
    if(result.passed){
      certPassed.value = true
    } else{
      certFailed.value = true
    }
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
              :parameters="redirectExpirationDateString"
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
              <div v-if="certPassed">
                <h2>Congratulations You Earned Your GSA SmartPay® Program Certificate (GSPC)</h2>
                <p>You have met the requirements to earn a GSA SmartPay® Program Certificate (GSPC). Your certificate has been emailed to you. Or, you may download your certificate below.</p>
                <button
                  class="usa-button"
                  @click="downloadCert"
                >
                  Download your certificate
                </button>
                <br><br>
                <a href="/">Return to the GSA SmartPay Training Home Page</a>
              </div>
              <div v-else-if="certFailed">
                <h2>You Don't Meet the Requirements for GSA SmartPay® Program Certification (GSPC)</h2>
                <p>Once you have met the coursework and experience requirement of six months of continuous, hands-on experience working with the GSA SmartPay program please return to the link  in your email to reapply.</p>
                <p>If you have any questions ,please reference <a href="">Smart Bulletin No. 022</a> or contact the GSPC Program Manager at <a href="mailto:smartpaygspc@gsa.gov">smartpaygspc@gsa.com</a>.</p>
                <a href="/">Return to the GSA SmartPay Training Home Page</a>
              </div>
              <div v-else>
                <GspcQuestions
                  :expiration-date="expirationDate"
                  @submit-gspc-registration="submitGspcRegistration"
                />
              </div>
            </Loginless>
          </Suspense>
        </div>
      </div>
    </div>
  </div>
</template>