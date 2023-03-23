<script setup>
  import {onMounted} from 'vue'
  import { profile } from '../stores/user'
  const props = defineProps(['title'])
  import { useStore } from '@nanostores/vue'

  const user = useStore(profile)
  onMounted(async () =>{
    // remove token from url query now that we are here.
    const url = new URL(window.location);
    url.search = ''
    history.replaceState({}, '', url)
    // validate JWT here and 
  })
</script>
<template>
    <h2> A Quiz goes here</h2>
    <h3> {{ title }}</h3>
    <p class="usa-prose">
    Welome {{ user.name }} from {{ user.agency }}
</p>
</template>