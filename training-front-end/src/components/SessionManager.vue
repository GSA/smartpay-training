<script setup>
  import { useStore } from '@nanostores/vue'
  import { hasActiveSession} from '../stores/user'
  import { willTimeOut, continueSession } from '../stores/session_manager'
  import ExitModal from './ExitModal.vue'
  import ExitMenu from './ExitMenu.vue'

  const isModalDisplayed = useStore(willTimeOut)
  const isActive = useStore(hasActiveSession)

  const exit = () => {
    window.location.replace(`${import.meta.env.BASE_URL}exit`)
  }
  
</script>
<template>
  <Teleport to="#header_main_menu">
    <ExitMenu
    v-if="isActive"
    @exit="exit" 
  />
  </Teleport>
  <ExitModal 
    v-if="isActive && isModalDisplayed"
    @exit="exit" 
    @continueSession="continueSession"
  />
</template>
