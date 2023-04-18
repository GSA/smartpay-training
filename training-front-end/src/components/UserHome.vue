<script setup>
  /**
   * Responsible for fetching and displaying user information
   * This depends on a valid JWT being present in the store
   */
  import { onMounted } from "vue"
  import { profile, getUserFromToken, clearUser} from '../stores/user'
  import { useStore } from '@nanostores/vue'

  const user = useStore(profile)

  onMounted(async () =>{
    // remove token from url query now that we are here.
    const url = new URL(window.location);
    url.search = ''
    history.replaceState({}, '', url)
    // validate JWT here and 
    // call clearUser here is jwt is not longer valid.
  })
</script>
<template>
  <div>
    <h2>Welcome {{ user.name }}</h2>
        
    <p>for testing: <br>{{ user.jwt }} </p>
  </div>
</template>