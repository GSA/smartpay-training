<script setup>
    const props = defineProps({
        'linkHome': {
            type: Boolean,
            default: true,
        },
    })
</script>
<template>
    <header class="usa-header usa-header--extended  border-bottom-1px border-base-light" role="banner">
        <div class="usa-navbar">
            <div v-if="linkHome" class="usa-logo" id="header-logo">
                <router-link to="/">
                    <img class="usa-logo-img" src="@/assets/images/gsa-smartpay-training-logo.svg" alt="GSA SmartPay Logo" title="U.S. General Services Administration">
                </router-link>
            </div>
            <div v-else class="usa-logo" id="header-logo">
                <img class="usa-logo-img" src="@/assets/images/gsa-smartpay-training-logo.svg" alt="GSA SmartPay Logo" title="U.S. General Services Administration">
            </div>
        </div>
    </header>
 </template>