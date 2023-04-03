<script setup>
  import { onMounted, ref } from 'vue'
  import { profile, getUserFromToken } from '../stores/user'
  import { useStore } from '@nanostores/vue'
  import Loginless from './Loginless.vue';
  
  const user = useStore(profile)
  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const loaded = ref(false)

  onMounted(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('t')

    if (token) {
        try {
            await getUserFromToken(base_url, token)
        } catch(e) {
            console.log("error", e)
            loaded.value = true
        }
    } 
    loaded.value = true
  })
</script>

<template>
  <Loginless v-if="loaded"/>
</template>