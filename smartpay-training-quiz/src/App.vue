<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Banner from "@/components/uswds/Banner.vue";
import PrototypeAlert from "@/components/uswds/PrototypeAlert.vue";
import GSAFooter from "@/components/uswds/GSAFooter.vue"
import USAIdentifier from "@/components/uswds/USAIdentifier.vue";
import GSAHeader from "@/components/uswds/GSAHeader.vue"


</script>

<template>
    <Banner />
    <div  class="background flex-fill">
        <GSAHeader :linkHome="false" />
        <div id="main-container" class="wide-layout">
            <main>
                <RouterView />
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
