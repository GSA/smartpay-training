<script setup>
    import { ref, reactive } from 'vue'
    import Alert from './Alert.vue'
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
    
    <Alert v-if="error" heading="Error">There was an error with input</Alert> <!-- This happens on server error -->
    <div v-if="isSubmitted">
        <h3>Check your email</h3>
        <p>We just send an email to the address you provided. Check you email and click the link to begin you quiz</p>
        link: {{ token }}
    </div>

    <div v-else>
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
                    v-model="user.first_name"
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
                    v-model="user.last_name"
                />
                <label class="usa-label" for="middle-name">Email Address</label>
                <input
                    class="usa-input usa-input--xl"
                    id="email-address"
                    name="email-address"
                    v-model="user.email"
                />
                <label class="usa-label" for="middle-name">Agency</label>
                <input
                    class="usa-input usa-input--xl"
                    id="agency"
                    name="agency"
                    v-model="user.agency"
                />
            
                <input class="usa-button" type="submit" value="Email Quiz Link" :disabled='isLoading'/>

            </fieldset>
        </form>
    </div>

</template>

<style scoped>

</style>
