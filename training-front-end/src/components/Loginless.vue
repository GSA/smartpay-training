<script setup>
  /**
	 * Responsible for handling the form that generates and email link.
	 * After the form is submitted it displays a message telling the user
	 * to check their email.
	 */

  import { ref, reactive, computed, onMounted } from 'vue';
  import { profile, getUserFromToken } from '../stores/user'
  import { useStore } from '@nanostores/vue'

  import Alert from './Alert.vue';
  import ValidatedInput from './ValidatedInput.vue';
  import ValidatedSelect from './ValidatedSelect.vue';
  import { useVuelidate } from '@markmeyer/vuelidate-core';
  import { required, email } from '@markmeyer/vuelidate-validators';
  import agencyList from '../data/agencies.js';

  const base_url = import.meta.env.PUBLIC_API_BASE_URL

  const props = defineProps(['page_id', 'title'])
  const emit = defineEmits(['startLoading', 'endLoading', 'error'])

  const user = useStore(profile)
  const isLoggedIn = computed(() => Boolean(user.value.jwt))

  const user_input = reactive({
    name: undefined,
    email: undefined,
    agency_id: undefined
  })

  const validations_just_email = {
    email: {email, required}
  }
  const v_email$ = useVuelidate(validations_just_email, user_input)

  const validations_all_info = {
    name: {required},
    email: {email, required},
    agency_id: {required}
  }
  const v_all_info$ = useVuelidate(validations_all_info, user_input)

  const tempURL = ref('')
  const isLoaded = ref(false)
  const isLoading = ref(false)
  const error = ref()
  const isFlowComplete = ref(false)
  const emailValidated = ref(false)

  function clearToken() {
    const url = new URL(window.location);
    url.search = ''
    history.replaceState({}, '', url)
  }
  onMounted(async () => {
    // Handle token in url query if it exists
    const urlParams = new URLSearchParams(window.location.search);
    const parm_token = urlParams.get('t')

    if (parm_token) {
      try {
        await getUserFromToken(base_url, parm_token)
        clearToken();
      } catch(e) {
        emit('error', e)
      }
    } 
    isLoaded.value = true
  })

  async function start_email_flow() {
    const validation = emailValidated.value ? v_all_info$ : v_email$
    const isFormValid = await validation.value.$validate() 
    if (!isFormValid) {
     return
    }

    emit('startLoading')
    isLoading.value = true
    error.value = undefined
    
    const apiURL = new URL(`${base_url}/api/v1/get-link`)
    let res
    try {
       res = await fetch(apiURL,  {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({
          user: user_input, 
          dest: {page_id: props.page_id, title: props.title}
        })
      })
    } catch (err) {
      console.log("err", err)
      isLoading.value = false
      const e = new Error("Sorry, we had an error connecting to the server.")
      e.name = "Server Error"
      emit('error', e)
      emit('endLoading')
      return
    }
    
      if (! res.ok) { 
        throw new Error(res)
      }

      const json = await res.json()
      const status = res.status
      
      if (status == 201) {
        // the api sends a 201 if the token was created
        // in the cache and an email was sent
        tempURL.value = json.token // this is just temporary while in Dev
        isFlowComplete.value = true
      } else {
        // any other 2xx response should assume
        // it worked, but we need more info
        emailValidated.value = true
      }
      isLoading.value = false
      emit('endLoading')
  }
</script>

<template>

  <div v-if="!isLoggedIn && isLoaded">
    <div v-if="isFlowComplete" class="grid-row" data-test="post-submit">
      <div class="tablet:grid-col-8 usa-prose margin-y-4">
        <h2 class="usa-prose">Check your email</h2>
        <p>We just sent you an email at <b>{{user_input.email}}</b> with a link to access the training quiz. This link is only active for 24 hours</p>
        
        <p>Not the right email? <a href="/user_input">Send another email</a></p>
            
        <p><b>Temp for development</b></p>
        <p>
          URL that was emailed: {{ tempURL }}
        </p>
      </div>
    </div>
    <div v-else class="grid-row" data-test="pre-submit">
      <div class="tablet:grid-col-8">
        <h2>Getting access to quiz</h2>

        <p>Fill out this form to get access to the {{ title }}. You'll receive an email with a link to access the training.</p>
        <form
          v-if="!emailValidated"
          class="usa-form usa-form--large margin-bottom-3"
          @submit.prevent="start_email_flow"
          data-test="email-submit-form"
          >
          <fieldset class="usa-fieldset">
            <ValidatedInput 
              client:load
              v-model="user_input.email" 
              :isInvalid="v_email$.email.$error" 
              label="Email Address (*Required)"
              name="email"
              error_message="Please enter a valid email address"
            />  
            <input class="usa-button" type="submit" value="Submit" :disabled='isLoading' data-test="submit"/>
          </fieldset>
        </form>
        <form
          v-else
          class="usa-form usa-form--large margin-bottom-3"
          @submit.prevent="start_email_flow"
          data-test="name-submit-form"
          >
          <fieldset class="usa-fieldset">
            <ValidatedInput 
              client:load
              v-model="user_input.email" 
              :isInvalid="v_all_info$.email.$error" 
              label="Email Address (*Required)"
              name="email"
              error_message="Please enter a valid email address"
              :readonly=true
            />  
            <ValidatedInput 
              client:load
              v-model="user_input.name" 
              :isInvalid="v_all_info$.name.$error" 
              label="Name (*Required)"
              name="name"
              error_message="Please enter your full name"
            />
            <Suspense>
            <ValidatedSelect 
              client:load
              v-model="user_input.agency_id" 
              :isInvalid="v_all_info$.agency_id.$error" 
              :options="agencyList"
              label="Agency / organization (*Required)"
              name="agency"
              error_message="Please enter your agency"
            />
            </Suspense>
            <input class="usa-button" type="submit" value="Submit" :disabled='isLoading' data-test="submit"/>
          </fieldset>
        </form>

        <p>Didn’t receive the access email?</p>

      </div>
    </div>
  </div>
  <div v-else data-test="child-component">
    <slot v-if="isLoaded"></slot>
  </div>
</template>
