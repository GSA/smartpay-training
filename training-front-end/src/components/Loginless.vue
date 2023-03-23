<script setup>
  /**
	 * Responsible for handling the form that generates and email link.
	 * After the form is submitted it displays a message telling the user
	 * to check their email.
	 */

  import { ref, reactive } from 'vue';
  import Alert from './Alert.vue';
  import ValidatedInput from './ValidatedInput.vue';
  import ValidatedSelect from './ValidatedSelect.vue';
  import hero_image from '/images/Training_TravelAH_Hero.jpg';
  import { useVuelidate } from '@markmeyer/vuelidate-core';
  import { required, email } from '@markmeyer/vuelidate-validators';
  import agencyList from '../data/agencies.js';

  const base_url = import.meta.env.PUBLIC_API_BASE_URL

  const props = defineProps(['page_id'])
  const emit = defineEmits(['startLoading', 'endLoading', 'error'])

  const user = reactive({
    name: undefined,
    email: '',
    agency: undefined
  })

  const validations_just_email = {
    email: {email, required},
  }
  const v_email$ = useVuelidate(validations_just_email, user)

  const validations_all_info = {
    name: {required},
    email: {email, required},
    agency: {required}
  }
  const v_all_info$ = useVuelidate(validations_all_info, user)

  const token = ref('')
  const isLoading = ref(false)
  const error = ref()
  const isFormSubmitted = ref(false)
  const emailValidated = ref(false)

  async function start_email_flow() {
    const validation = emailValidated ? v_email$ : v_all_info$
    const isFormValid = await validation.value.$validate() 
    emit('startLoading')
    if (!isFormValid) {
     return
    }
    isLoading.value = true
    error.value = undefined
    
    const apiURL = new URL(`${base_url}/api/v1/get-link`);
    let res;
    try {
       res = await fetch(apiURL,  {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({...user, page_id:props.page_id})
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
        // this indicates a server error 
        // — what should we tell the user?
        throw new Error(res)
      }

      const json = await res.json()
      const status = res.status
      
      if (status == 200) {
          emailValidated.value = true
      } else {
          token.value =  json.token
          isFormSubmitted.value = true
      }
      isLoading.value = false
      emit('endLoading')
  }
</script>

<template>

  <div v-if="isFormSubmitted" class="grid-row" data-test="post-submit">
    <div class="tablet:grid-col-8 usa-prose margin-y-4">
      <h2 class="usa-prose">Check your email</h2>
      <p>We just sent you an email at <b>{{user.email}}</b> with a link to access the training quiz. This link is only active for 24 hours</p>
      
      <p>Not the right email? <a href="/user">Send another email</a></p>
          
      <p><b>Temp for development</b></p>
      <p>
        URL that was emailed: {{ token }}
      </p>
    </div>
  </div>


  <div v-else class="grid-row" data-test="pre-submit">
    <div class="tablet:grid-col-8">
      <h2>Getting access to quiz</h2>

      <p>Fill out this form to get access to the Travel training for card / account holders and approving officials. You'll receive an email with a link to access the training.</p>
      <form
        v-if="!emailValidated"
        class="usa-form usa-form--large margin-bottom-3"
        @submit.prevent="start_email_flow"
        data-test="email-submit-form"
        >
        <fieldset class="usa-fieldset">
          <ValidatedInput 
            client:load
            v-model="user.email" 
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
            v-model="user.email" 
            :isInvalid="v_all_info$.email.$error" 
            label="Email Address (*Required)"
            name="email"
            error_message="Please enter a valid email address"
            :readonly=true
          />  
          <ValidatedInput 
            client:load
            v-model="user.name" 
            :isInvalid="v_all_info$.name.$error" 
            label="Name name (*Required)"
            name="name"
            error_message="Please enter your full name"
          />
          <ValidatedSelect 
            client:load
            v-model="user.agency" 
            :isInvalid="v_all_info$.agency.$error" 
            :options="agencyList"
            label="Agency / organization (*Required)"
            name="agency"
            error_message="Please enter your agency"
          />
          <input class="usa-button" type="submit" value="Submit" :disabled='isLoading' data-test="submit"/>
        </fieldset>
      </form>

      <p>Didn’t receive the access email?</p>

    </div>
  </div>
</template>
