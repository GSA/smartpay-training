<script setup>
  import { useStore } from '@nanostores/vue'
  import { hasActiveSession} from '../stores/user'

  const isActice = useStore(hasActiveSession)
 
  const exit = () => {
    window.location.href  = "/exit"
  }
</script>
<template>
  <li 
    v-if="isActice"
    class="usa-nav__primary-item"
  >
    <button
      class="usa-nav-link cursor-pointer"
      @click="exit"
    >
      exit
    </button>
  </li>
</template>