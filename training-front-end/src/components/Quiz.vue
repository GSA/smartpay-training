<script setup>
  import { profile } from '../stores/user'
  import { useStore } from '@nanostores/vue'

  const props = defineProps(['title'])
  const user = useStore(profile)
 
</script>
<template>
    <h2> A Quiz goes here</h2>
    <h3> {{ title }}</h3>
    <p class="usa-prose">
    Welome {{ user.name }}
</p>
</template>