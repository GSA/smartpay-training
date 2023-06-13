<!--
  Process callbacks from UAA login by redirecting to the desired target page.
  This component is intended to be used only by the auth_callback.astro page.
-->

<script setup>
  import { ref } from 'vue'
  import AuthService from '../services/auth'
  import USWDSAlert from './USWDSAlert.vue'
  import { useStore } from '@nanostores/vue'
  import { redirectTarget, clearRedirectTarget } from '../stores/auth'
  import { getUserFromTokenExchange } from '../stores/user'

  const auth = new AuthService()
  const error = ref(null)
  const authRedirectTarget = useStore(redirectTarget)

  auth.loginCallback().then(async () => {
    const uaaToken = await auth.getAccessToken()
    await getUserFromTokenExchange(import.meta.env.PUBLIC_API_BASE_URL, uaaToken)
    window.location.href = authRedirectTarget.value
    clearRedirectTarget()
  }).catch((err) => {
    error.value = err
  })
</script>

<template>
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <div v-if="error">
      <USWDSAlert
        heading="Sorry, we encountered a problem while attempting to log in"
        status="error">
        {{ error }}
      </USWDSAlert>
      <p><a href="/">Return to Home</a></p>
    </div>
  </div>
</template>
