<script setup>
    const props = defineProps({
        /**
         * Total number of pages to show
         */
        'linkHome': {
            type: Boolean,
            default: true,
        },
    })
</script>
<template>
    <header class="usa-header usa-header--extended " role="banner">
        <div class="usa-navbar border-bottom-1px">
            <div v-if="linkHome" class="usa-logo" id="header-logo">
                <router-link to="/">
                    <img class="usa-logo-img" src="@/assets/images/gsa-smartpay-logo.svg" alt="GSA SmartPay Logo" title="U.S. General Services Administration">
                </router-link>
                <router-link to="/">
                    <em class="usa-logo__text">GSA SmartPay Training</em>
                </router-link>
            </div>
            <div v-else class="usa-logo" id="header-logo">
                <img class="usa-logo-img" src="@/assets/images/gsa-smartpay-logo.svg" alt="GSA SmartPay Logo" title="U.S. General Services Administration">
                <em class="usa-logo__text" >GSA SmartPay Training</em>
            </div>
        </div>
    </header>
 </template>