<!--
  Process callbacks from UAA login by redirecting to the desired target page.
  This component is intended to be used only by the auth_callback.astro page.
-->

<script setup>
  import { ref } from 'vue'
  import AuthService from '../services/auth'
  import USWDSAlert from './USWDSAlert.vue'
  import { useStore } from '@nanostores/vue'
  import { $redirectTarget } from '../stores/auth'

  const auth = new AuthService()
  const error = ref(null)
  const authRedirectTarget = useStore($redirectTarget)

  auth.loginCallback().then(() => {
    window.location.href = authRedirectTarget.value
  }).catch((err) => {
    error.value = err
  })
</script>

<template>
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <div v-if="error">
      <USWDSAlert heading="Sorry, we encountered a problem while attempting to log in" status="error">
        {{ error }}
      </USWDSAlert>
    </div>
  </div>
</template>
