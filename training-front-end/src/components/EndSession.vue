<script setup>
  import { onMounted } from 'vue'
  import { clearUser } from '../stores/user'
 
  onMounted(() => {
    clearUser()
    window.location.replace("/")
  })
</script>
<template>
  <span />
</template>