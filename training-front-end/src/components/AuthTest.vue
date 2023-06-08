<script setup>
  import { ref, onMounted } from 'vue';
  import AuthService from '../services/auth'

  const auth = new AuthService()
  const isAuthenticated = ref(false)
  const userEmail = ref("")

  onMounted(() => {
    auth.getUser().then(user => {
      if (user) {
        isAuthenticated.value = true
        userEmail.value = user.profile.email
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
    <button @click="handleLogin">Login</button>
    <button @click="handleLogout">Logout</button>
    <p>Authenticated: {{ isAuthenticated }}</p>
    <div v-if="isAuthenticated">
      <p>User: {{ userEmail }}</p>
    </div>
  </div>
</template>
