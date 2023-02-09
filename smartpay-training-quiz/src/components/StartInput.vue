<script setup>
import { ref } from 'vue'
    const base_url = import.meta.env.VITE_API_BASE_URL

    const first_name = ref('')
    const last_name = ref('')
    const email = ref('')
    const agency = ref('')
    const token = ref('')
    const loading = ref(false)
    const error = ref('')

    function start_email_flow() {
        loading.value = true
        error.value = ''
        
        const data = {
            first_name: first_name.value,
            last_name: last_name.value,
            email: email.value,
            agency: agency.value
        }
        const url = new URL(`${base_url}/api/v1/get-link`);

        fetch(url,  {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
        .then(res => {
            if (res.ok) {
                return res.json()
            }
            return Promise.reject(res)
        })
        .then(json => {
            token.value =  json.token
            loading.value = false
        })
        .catch((err) => {
            loading.value = false
        })
    }

</script>

<template>
    
  <div class="greetings">
    <form class="usa-form usa-form--large margin-bottom-3" @submit.prevent="start_email_flow">
        <fieldset class="usa-fieldset">
            <legend class="usa-legend usa-legend--large">Tell us about yourself</legend>
            <label class="usa-label" for="given-name">First or given name</label>
            <div class="usa-hint" id="gnHint">For example, Jose, Darren, or Mai</div>
            <input
                class="usa-input usa-input--xl"
                id="given-name"
                name="first-name"
                aria-describedby="gnHint"
                v-model="first_name"
            />
            <label class="usa-label" for="family-name">Last or family name</label>
            <div class="usa-hint" id="lnHint">
                For example, Martinez Gonzalez, Gu, or Smith
            </div>
            <input
                class="usa-input usa-input--xl"
                id="family-name"
                name="last-name"
                aria-describedby="lnHint"
                v-model="last_name"
            />
            <label class="usa-label" for="middle-name">Email Address</label>
            <input
                class="usa-input usa-input--xl"
                id="email-address"
                name="email-address"
                v-model="email"
            />
            <label class="usa-label" for="middle-name">Agency</label>
            <input
                class="usa-input usa-input--xl"
                id="agency"
                name="agency"
                v-model="agency"
            />
           
            <input class="usa-button" type="submit" value="Email Quiz Link" />

        </fieldset>
    </form>
  </div>
  Token: {{ token }}
</template>

<style scoped>

</style>
