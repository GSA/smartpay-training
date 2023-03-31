<script setup>
  const props = defineEmits(['start'])
</script>
<template>
  <section class="usa-prose margin-y-4">
    <p>
      Now that you’ve reviewed the course material, you are ready to take the quiz. You must score at least a 75% to pass. Once you’ve successfully passed the quiz, your certificate of completion will be sent to you via the email that you provided when you registered for the quiz. You may print the certificate or save it as a PDF.
    </p>
    <p>
      <b>Note:</b> Your quiz progress will not be saved if you navigate away.
    </p>
    <button class="usa-button" @click="$emit('start')">Start quiz</button>
  </section>

</template>