<script setup>
  import { onMounted } from 'vue'
  import { clearUser } from '../stores/user'
 
  onMounted(() => {
    clearUser()
    window.location.replace(import.meta.env.BASE_URL)
  })
</script>
<template>
  <span />
</template>