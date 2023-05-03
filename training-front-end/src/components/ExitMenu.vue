<script setup>
  import { useStore } from '@nanostores/vue'
  import { hasActiveSession} from '../stores/user'
  import LogoutIcon from './icons/LogoutIcon.vue'
  
  const isActive = useStore(hasActiveSession)

  const exit = () => {
    window.location.replace(`${import.meta.env.BASE_URL}exit`)
  }
</script>
<template>
  <li 
    v-if="isActive"
    class="margin-left-auto"
  >
    <button
      data-test="exit-button"
      class="cursor-pointer exit"
      @click="exit"
    >
      <LogoutIcon /> Exit
    </button>
  </li>
</template>
