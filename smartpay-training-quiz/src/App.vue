<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Banner from "./components/Banner.vue";
import PrototypeAlert from "./components/PrototypeAlert.vue";
import GSAFooter from "./components/GSAFooter.vue"
import USAIdentifier from "./components/USAIdentifier.vue";
import GSAHeader from "./components/GSAHeader.vue"


</script>

<template>
    <Banner />
    <PrototypeAlert />
    <div  class="background flex-fill">
        <GSAHeader :linkHome="false" />
        <div id="main-container" class="wide-layout">
            <main>
                <div class="grid-container">
                    <RouterView />
                </div>
            </main>
        </div>

    </div>
    <footer class="flex-shrink-0">
        <GSAFooter />
        <USAIdentifier />
    </footer>
</template>

<style scoped>
 
</style>
