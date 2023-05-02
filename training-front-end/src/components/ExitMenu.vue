<script setup>
  import { useStore } from '@nanostores/vue'
  import { hasActiveSession} from '../stores/user'
  import FileDownload from './icons/FileDownload.vue'
  
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
      class="smartpay-sign-out"
      @click="exit"
    >
      Exit
    </button>
  </li>
</template>