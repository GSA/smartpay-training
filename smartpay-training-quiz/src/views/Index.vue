<script setup>
  import hero_image from '@/assets/images/Training_TravelAH_Hero.jpg'
  import Hero from '@/components/smartpay/Hero.vue'

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
      <ul class="usa-card-group">
        <li class="usa-card tablet:grid-col-4">
          <div class="usa-card__container">
            <div class="usa-card__header">
             
              <h4 class="usa-card__heading ">
                <span>
                  <img
                  src="../assets/images/travelc.svg"
                  alt="a blue circle represent blue travel card"
                  class="circle-icon" />
                Travel training</span></h4>
            </div>
            <div class="usa-card__body">
              <p>
                Learn about the basics about your role and responsibility as a card / account holder, the Federal Travel Regulations (FTR), and other government travel policies.
              </p>
            </div>
            
            <div class="usa-card__footer">
              <router-link :to="{ name: 'getstarted'}">
              <button type="button" class="usa-button">Take the travel training</button>
              </router-link>
            </div>
          </div>
        </li>
        <li class="usa-card tablet:grid-col-4">
          <div class="usa-card__container">
            <div class="usa-card__header">
              
              <h4 class="usa-card__heading"><span>
                  <img
                  src="../assets/images/purchasec.svg"
                  alt="a blue circle represent blue travel card"
                  class="circle-icon" />
                  Purchase training</span>
                </h4>
            </div>
            <!--
            <div class="usa-card__media">
              
              <div class="usa-card__img">
                <img
                  src="../assets/images/red-card.png"
                  alt="A placeholder image"
                />
              </div>
            
            </div>
          -->
            <div class="usa-card__body">
              <p>
                Learn about the basics about your role and responsibility as a card / account holder, the Federal Travel Regulations (FTR), and other government travel policies.
              </p>
            </div>
            <div class="usa-card__footer">
              <button type="button" class="usa-button">Take the purchase training</button>
            </div>
          </div>
        </li>
      </ul>

      <h3>
        TRAINING FOR PROGRAM COORDINATORS
      </h3>
      <ul class="usa-card-group">
        <li class="usa-card tablet:grid-col-4">
          <div class="usa-card__container">
            <div class="usa-card__header">
             
              <h4 class="usa-card__heading ">
                <span>
                  <img
                  src="../assets/images/travelc.svg"
                  alt="a blue circle represent blue travel card"
                  class="circle-icon" />
                Travel training</span></h4>
            </div>
            <div class="usa-card__body">
              <p>
                Learn about the basics about your role and responsibility as a card / account holder, the Federal Travel Regulations (FTR), and other government travel policies.
              </p>
            </div>
            
            <div class="usa-card__footer">
              <router-link :to="{ name: 'getstarted'}">
              <button type="button" class="usa-button">Take the travel training</button>
              </router-link>
            </div>
          </div>
        </li>
        <li class="usa-card tablet:grid-col-4">
          <div class="usa-card__container">
            <div class="usa-card__header">
              <h4 class="usa-card__heading"><span>
                  <img
                  src="../assets/images/purchasec.svg"
                  alt="a blue circle represent blue travel card"
                  class="circle-icon" />
                  Purchase training</span>
                </h4>
            </div>
            
            <div class="usa-card__body">
              <p>
                Learn about the basics about your role and responsibility as a card / account holder, the Federal Travel Regulations (FTR), and other government travel policies.
              </p>
            </div>
            <div class="usa-card__footer">
              <button type="button" class="usa-button">Take the purchase training</button>
            </div>
          </div>
        </li>
        <li class="usa-card tablet:grid-col-4">
          <div class="usa-card__container">
            <div class="usa-card__header">
              <h4 class="usa-card__heading"><span>
                  <img
                  src="../assets/images/fleetc.svg"
                  alt="a blue circle represent blue travel card"
                  class="circle-icon" />
                  Fleet training</span>
                </h4>
            </div>
           
            <div class="usa-card__body">
              <p>
                Learn about the basics about your role and responsibility as a card / account holder, the Federal Travel Regulations (FTR), and other government travel policies.
              </p>
            </div>
            <div class="usa-card__footer">
              <button type="button" class="usa-button">Take the fleet training</button>
            </div>
          </div>
        </li>
      </ul>

    </div>
</template>

<style scoped>
 .circle-icon {
    vertical-align: middle;
    width: 15%;
  }
</style>