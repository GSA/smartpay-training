<script setup>
  /**
   * This compoenent is responsible for displaying alert messages on the front page.
   * Because this project is built around static pages built with Astro, there is
   * no global state for the applications. This makes sending messages between pages
   * challenging. This component depends on the message_manager and session_manager
   * to set a message in session storage. When the component mounts it reads and 
   * clears this messages and displays it in the USWDS alert.
   * 
   * See stores/message_manager for more details. 
   */
  import { onMounted, ref } from 'vue'
  import { useStore } from '@nanostores/vue'
  import { message, clearMessage } from '../stores/message_manager.js'
  import USWDSAlert from './USWDSAlert.vue'

  const message_text = useStore(message)
  const display_text = ref()
  const display_level = ref()
  
  function consumeMessage() {
    if (message_text.value) {
      [display_text.value, display_level.value] = message_text.value
      clearMessage(message)
    }
  }
  
  onMounted(() => {
    consumeMessage()
  })
</script>
<template>
  <USWDSAlert 
    v-if="display_text"
    :status="display_level"
    class="usa-alert--slim margin-y-4"
    :has-heading="false"
  >
    {{ display_text }}
  </USWDSAlert>
</template>