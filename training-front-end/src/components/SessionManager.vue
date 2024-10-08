<script setup>
  import { useStore } from '@nanostores/vue'
  import { hasActiveSession } from '../stores/user'
  import { willTimeOut, continueSession, exit } from '../stores/session_manager'
  import { setMessage } from '../stores/message_manager'

  import ExitModal from './ExitModal.vue'
  import ExitMenu from './ExitMenu.vue'

  const isModalDisplayed = useStore(willTimeOut)
  const isActive = useStore(hasActiveSession)

  const exit_redirect = () => {
    setMessage(
      'You have successfully exited.',
      'success'
    )
    window.location.replace(`${import.meta.env.BASE_URL}exit/`)
  }
</script>
<template>
  <Teleport to="#header_main_menu">
    <ExitMenu
      v-if="isActive"
      @exit="exit_redirect" 
    />
  </Teleport>
  
  <Teleport to="body">
    <ExitModal 
      v-if="isActive && isModalDisplayed"
      @exit="exit" 
      @continue-session="continueSession"
    />
  </Teleport>
</template>
