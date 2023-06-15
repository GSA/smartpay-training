<!--
  This component can be wrapped around anything that requires authentication.
-->

<script setup>
  import { useStore } from '@nanostores/vue'
  import AuthService from '../services/auth'
  import USWDSAlert from './USWDSAlert.vue'
  import { setRedirectTarget } from '../stores/auth'
  import { profile } from '../stores/user'

  const auth = await AuthService.instance()
  const user = useStore(profile)
  const isAuthenticated = !!user.value.jwt

  const handleLogin = () => {
    setRedirectTarget(window.location.href)
    auth.login()
  }
</script>

<template>
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <div v-if="!isAuthenticated">
      <USWDSAlert
        :has-heading="false"
        status="error"
      >
        You need to sign in to use this feature.
      </USWDSAlert>

      <button
        class="usa-button"
        @click="handleLogin"
      >
        Sign in using SecureAuth
      </button>
    </div>
    <slot v-if="isAuthenticated" />
  </div>
</template>
