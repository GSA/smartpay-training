<script setup>
    import { ref, reactive } from 'vue'
    import Alert from '@/components/uswds/Alert.vue'
    import Hero from '@/components/smartpay/Hero.vue'
    import hero_image from '@/assets/images/hero_smarttax.jpg'

    const base_url = import.meta.env.VITE_API_BASE_URL

    const user = reactive({
        first_name: '',
        last_name: '',
        email: '',
        agency: ''
    })
    const token = ref('')
    const isLoading = ref(false)
    const error = ref('')
    const isSubmitted = ref(false)

    function start_email_flow() {
        isLoading.value = true
        error.value = ''
 
        const url = new URL(`${base_url}/api/v1/get-link`);

        fetch(url,  {
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

    <Alert v-if="error" heading="Error">There was an error with input</Alert> <!-- This happens on server error -->
    <div v-if="isSubmitted" class="grid-container" >
        <h3>Check your email</h3>
        <p>We just send an email to:</p>
        <p><b>{{user.email}}</b></p>
        
        <p>Check you email and click the link to begin you quiz</p>
        
        
        <p><b>Temp for development</b></p>
        <p>
            URL that was emailed: {{ token }}
        </p>
    </div>

    <div v-else class="grid-container" >
        <h2>Getting access to training</h2>
        <p>Fill out this form to get access to the Travel training for card / account holders and approving officials. You'll receive an email with a link to access the training.</p>
        <form class="usa-form usa-form--large margin-bottom-3" @submit.prevent="start_email_flow">
            <fieldset class="usa-fieldset">
                <label class="usa-label" for="given-name">First name (*Required)</label>
                <input
                    class="usa-input usa-input--xl"
                    id="given-name"
                    name="first-name"
                    aria-describedby="gnHint"
                    v-model="user.first_name"
                    required
                />
                <label class="usa-label" for="family-name">Last name (*Required)</label>
                <input
                    class="usa-input usa-input--xl"
                    id="family-name"
                    name="last-name"
                    aria-describedby="lnHint"
                    v-model="user.last_name"
                    required
                />
                <label class="usa-label" for="middle-name">Email Address (*Required)</label>
                <input
                    class="usa-input usa-input--xl"
                    id="email-address"
                    name="email-address"
                    type="email" 
                    oninvalid="setCustomValidity('Please provide a valid email address')"
                    pattern="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$"
                    v-model="user.email"
                    required
                />
                <label class="usa-label" for="middle-name">Agency / organization(*Required)</label>
                <input
                    class="usa-input usa-input--xl"
                    id="agency"
                    name="agency"
                    v-model="user.agency"
                    required
                />
            
                <input class="usa-button" type="submit" value="Submit" :disabled='isLoading'/>

                <p>Didn’t receive the access email?</p>
            </fieldset>
        </form>
    </div>

</template>

<style scoped>

</style>
