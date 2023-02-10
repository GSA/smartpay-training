<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Banner from "./components/Banner.vue";
import PrototypeAlert from "./components/PrototypeAlert.vue";
import GSAFooter from "./components/GSAFooter.vue"
import USAIdentifier from "./components/USAIdentifier.vue";


</script>

<template>
    <Banner />
    <PrototypeAlert />
     <RouterView />
     <footer class="flex-shrink-0">
        <GSAFooter />
        <USAIdentifier />
    </footer>
</template>

<style scoped>
 
</style>
