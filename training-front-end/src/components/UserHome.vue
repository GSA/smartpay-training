<script setup>
  import { onMounted } from "vue"
  import { profile, getUserFromToken, clearUser} from '../stores/user'
  import { useStore } from '@nanostores/vue'

  const user = useStore(profile)

  onMounted(async () =>{
    // remove token from url query now that we are here.
    const url = new URL(window.location);
    url.search = ''
    history.replaceState({}, '', url)
    // validate FWT here and 
    // call clearUser here is jwt is not longer valid.
  })
</script>
<template>
    <div>
        <h2>Welcome {{ user.first_name }}</h2>
        {{ user.first_name }} {{ user.last_name }} {{ user.agency }}
        
        <p>for testing: <br />{{ user.jwt }} </p>
    </div>
</template>