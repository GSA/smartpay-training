<script setup>
  import { onMounted, ref } from 'vue'
  import { useStore } from '@nanostores/vue'
  import { message, clearMessage } from '../stores/message_manager.js'
  import USWDSAlert from './USWDSAlert.vue'

  const message_text = useStore(message)
  const display_text = ref()
  
  function consumeMessage() {
    if (message_text.value) {
      display_text.value = message_text.value
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
    status="warning"
    class="usa-alert--slim margin-y-4"
    :has-heading="false"
  >
    {{ display_text }}
  </USWDSAlert>
</template>