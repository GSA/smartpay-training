<script setup>
  import hero_image from '@/assets/images/Training_TravelAH_Hero.jpg'
  import Hero from '@/components/smartpay/Hero.vue'
  import accounts_data from '@/data/trainingaccounts.json'
  import TrainingAccounts from '@/components/smartpay/TrainingAccounts.vue'

    const cardholders = {
      "listItems":[],
    };
    const coordinators = {
      "listItems":[],
    };
    cardholders.listItems = accounts_data.card_holders
    coordinators.listItems = accounts_data.coordinators

</script>
<template>
    <Hero :hero_image="hero_image">
    <template #default>
      Complete your SmartPay training
    </template>
    <template #subheader>
        We offer SmartPay training to all agency card / account holders, approving officials, and program coordinators. 
    </template>
    
  </Hero>
    <div class="grid-container" data-test="pre-submit">
      <h2>Select your training course</h2>
      <p>
        Each training course takes approximately 45 minutes to complete and is worth 1 CLP. To receive credit and your certificate, you must pass your quiz with a score of 75% or higher.
      </p>
      <h3>
        TRAINING FOR CARD / ACCOUNT HOLDERS AND APPROVING OFFICIALS
      </h3>
      <TrainingAccounts :items ="cardholders.listItems"></TrainingAccounts>

      <h3>
        TRAINING FOR PROGRAM COORDINATORS
      </h3>
      <TrainingAccounts :items ="coordinators.listItems"></TrainingAccounts>
    </div>
</template>
