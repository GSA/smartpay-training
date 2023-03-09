<script setup>
  import hero_image from '@/assets/images/Training_TravelAH_Hero.jpg'
  import Hero from '@/components/smartpay/Hero.vue'

</script>
<template>
    <Hero :hero_image="hero_image">
    <template #default>
        GSA SmartPay Training
    </template>
  </Hero>
    <div class="grid-container" data-test="pre-submit">
      
      <p>
        GSA offers free Government-wide GSA SmartPay training to all agency account holders (cardholders)/ approving officials and program coordinators. All training courses meet the OMB Circular A-123, Appendix B training requirement. Each training course takes approximately 45 minutes to complete and is worth 1 CLP.  To receive credit and your certificate, you must  login and pass your quiz with a score of 75% or higher.    
      </p>
      <h2>
       Start Training
      </h2>
      <p>
      <router-link :to="{ name: 'getstarted'}">
        Get a link to training
      </router-link>
        </p>
    </div>
</template>