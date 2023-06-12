<!--
  This component can be wrapped around anything that requires authentication.
-->

<script setup>
  import { ref, onMounted } from 'vue'
  import AuthService from '../services/auth'
  import USWDSAlert from './USWDSAlert.vue'
  import { setRedirectTarget } from '../stores/auth'

  const auth = new AuthService()
  const isAuthenticated = ref(false)

  onMounted(() => {
    auth.getUser().then(user => {
      if (user) {
        isAuthenticated.value = true
      } else {
        setRedirectTarget(window.location.href)
      }
    })
  })

  const handleLogin = () => {
    auth.login()
  }

  const handleLogout = () => {
    auth.logout()
  }
</script>

<template>
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <div v-if="!isAuthenticated">
      <USWDSAlert :hasHeading="false" status="error">
        You need to sign in to use this feature.
      </USWDSAlert>

      <button class="usa-button" @click="handleLogin">
        Sign in using SecureAuth
      </button>
    </div>

    <button v-if="isAuthenticated" class="usa-button" @click="handleLogout">
      Logout
    </button>
    <slot v-if="isAuthenticated"/>
  </div>
</template>
