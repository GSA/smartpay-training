<script setup>
  import { ref, reactive } from 'vue'
  import Alert from '@/components/uswds/Alert.vue'
  import Hero from '@/components/smartpay/Hero.vue'
  import ValidatedInput from '@/components/loginless/ValidatedInput.vue'
  import hero_image from '@/assets/images/Training_TravelAH_Hero.jpg'
  import { useVuelidate } from '@vuelidate/core'
  import { required, email } from '@vuelidate/validators'

  const base_url = import.meta.env.VITE_API_BASE_URL

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
  const isSubmitted = ref(false)

  async function start_email_flow() {
    const isFormCorrect = await v$.value.$validate();
    if (!isFormCorrect) {
      return
    }

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
      isSubmitted.value = true
    })
    .catch((err) => {
      isLoading.value = false
      error.value = err
    })
  }

</script>

<template>
  <Hero :hero_image="hero_image">
    <template #default>
      Travel Training for Card / Account Holders and Approving officials
    </template>
  </Hero>

  <div v-if="isSubmitted" class="grid-container" data-test="post-submit">
    <h3>Check your email</h3>
    <p>We just send an email to:</p>
    <p><b>{{user.email}}</b></p>
    
    <p>Check you email and click the link to begin you quiz</p>
          
    <p><b>Temp for development</b></p>
    <p>
      URL that was emailed: {{ token }}
    </p>
  </div>

  <div v-else class="grid-container" data-test="pre-submit">
    <Alert v-if="error" heading="Error" status="error" data-test="error"> <!-- This happens on server error -->
      There was an error with input.
    </Alert> 

    <h2>Getting access to training</h2>

    <p>Fill out this form to get access to the Travel training for card / account holders and approving officials. You'll receive an email with a link to access the training.</p>
    <form class="usa-form usa-form--large margin-bottom-3" @submit.prevent="start_email_flow">
      <fieldset class="usa-fieldset">

        <ValidatedInput 
          v-model="user.first_name" 
          :isInvalid="v$.first_name.$error" 
          label="First name (*Required)"
          name="first_name"
          error_message="Please enter your first name"
        />
        <ValidatedInput 
          v-model="user.last_name" 
          :isInvalid="v$.last_name.$error" 
          label="Last name (*Required)"
          name="last_name"
          error_message="Please enter your last name"
        />
        <ValidatedInput 
          v-model="user.email" 
          :isInvalid="v$.email.$error" 
          label="Email Address (*Required)"
          name="email"
          error_message="Please enter a valid email address"
        />
        <ValidatedInput 
          v-model="user.agency" 
          :isInvalid="v$.agency.$error" 
          label="Agency / organization(*Required)"
          name="agency"
          error_message="Please enter your agency"
        />

        <input class="usa-button" type="submit" value="Submit" :disabled='isLoading' data-test="submit"/>

        <p>Didn’t receive the access email?</p>
      </fieldset>
    </form>
  </div>

</template>
