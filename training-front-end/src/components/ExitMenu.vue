<script setup>
  import LogoutIcon from './icons/LogoutIcon.vue'
  defineEmits(['exit'])
</script>
<template>
  <li 
    class="margin-left-auto"
  >
    <button
      data-test="exit-button"
      class="cursor-pointer exit"
      @click="$emit('exit')"
    >
      <LogoutIcon /> Exit
    </button>
  </li>
 
</template>
