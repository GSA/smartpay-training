<script setup>
  import { ref } from 'vue';
  import AuthService from '../services/auth'

  const auth = new AuthService()

  const error = ref(null)

  auth.loginCallback().then(() => {
    window.location.href = '../admin'
  }).catch(function (err) {
    console.log(err)
    error.value = err
  });
</script>

<template>
  <div v-if="error">
    <p>Sorry, we encountered an error while attempting to log in:</p>
    <p>{{ error }}</p>
  </div>
</template>
