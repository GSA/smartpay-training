<script setup>
import StartInput from '../components/StartInput.vue'
import GSAHeader from "../components/GSAHeader.vue"
</script>

<template>
    <div  class="background flex-fill">
    
    <GSAHeader :linkHome="false" />
        <div id="main-container" class="wide-layout">
            <main>
                <div class="grid-container">
                    <StartInput msg="GSA SmartPay Quiz" />
                </div>
            </main>
        </div>
    </div>
</template>

<style scoped>
</style>