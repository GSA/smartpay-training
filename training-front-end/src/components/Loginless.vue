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
  
  const emit = defineEmits(['startLoading', 'endLoading', 'error'])

  const user = reactive({
    first_name: '',
    last_name: '',
    email: '',
    agency: ''
  })

  const validations = {
    first_name: {required},
    last_name: {required},
    email: {email, required},
    agency: {required}
  }
  const v$ = useVuelidate(validations, user)

  const token = ref('')
  const isLoading = ref(false)
  const error = ref('')
  const isFormSubmitted = ref(false)

  async function start_email_flow() {
    const isFormCorrect = await v$.value.$validate();

    if (!isFormCorrect) {
      return
    }
    emit('startLoading')
    isLoading.value = true
    error.value = ''
    
    const url = new URL(`${base_url}/api/v1/get-link`);

    await fetch(url,  {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify(user)
    })
    .then(res => {
      if (res.ok) {
        return res.json()
      }
      return Promise.reject(res)
    })
    .then(json => {
      token.value =  json.token
      isLoading.value = false
      isFormSubmitted.value = true
      emit('endLoading')
    })
    .catch((err) => {
      isLoading.value = false
      error.value = err
      emit('endLoading')
    })
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
      <Alert v-if="error" heading="Error" status="error" data-test="error"> <!-- This happens on server error -->
        There was an error with input.
      </Alert> 

      <h2>Getting access to quiz</h2>

      <p>Fill out this form to get access to the Travel training for card / account holders and approving officials. You'll receive an email with a link to access the training.</p>
      <form class="usa-form usa-form--large margin-bottom-3" @submit.prevent="start_email_flow">
        <fieldset class="usa-fieldset">

          <ValidatedInput 
            client:load
            v-model="user.first_name" 
            :isInvalid="v$.first_name.$error" 
            label="First name (*Required)"
            name="first_name"
            error_message="Please enter your first name"
          />
          <ValidatedInput 
            client:load
            v-model="user.last_name" 
            :isInvalid="v$.last_name.$error" 
            label="Last name (*Required)"
            name="last_name"
            error_message="Please enter your last name"
          />
          <ValidatedInput 
            client:load
            v-model="user.email" 
            :isInvalid="v$.email.$error" 
            label="Email Address (*Required)"
            name="email"
            error_message="Please enter a valid email address"
          />
          <ValidatedSelect 
            client:load
            v-model="user.agency" 
            :isInvalid="v$.agency.$error" 
            :options="agencyList"
            label="Agency / organization (*Required)"
            name="agency"
            error_message="Please enter your agency"
          />

          <input class="usa-button" type="submit" value="Submit" :disabled='isLoading' data-test="submit"/>

          <p>Didn’t receive the access email?</p>
        </fieldset>
      </form>
    </div>
  </div>
 

</template>
