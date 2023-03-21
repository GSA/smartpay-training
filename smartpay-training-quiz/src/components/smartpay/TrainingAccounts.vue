
<script setup>
  const props = defineProps({
    'items': Array
  })
</script>

<template>
      <ul class="usa-card-group">
        <li class="usa-card tablet:grid-col-4" v-for="item in items" :key="item">
          <div class="usa-card__container">
            <div class="usa-card__header">
              <h4 class="usa-card__heading">
                <span>
                  <img v-if= "item.img_type ==='T'"
                  src="@/assets/images/travelc.svg"
                  class="circle-icon"
                  aria-hidden="true"
                  />
                  <img v-if= "item.img_type ==='P'"
                  src="@/assets/images/purchasec.svg"
                  class="circle-icon"
                  aria-hidden="true"
                  />
                  <img v-if = "item.img_type ==='F'"
                  src="@/assets/images/fleetc.svg"
                  class="circle-icon"
                  aria-hidden="true"
                  />
                {{item.header}}</span></h4>
            </div>
            <div class="usa-card__body">
              <p>
                {{ item.text }}
              </p>
            </div>
            
            <div class="usa-card__footer">
              <router-link :to="{ name: item.link_name}">
              {{item.link_text}}
              </router-link>
            </div>
          </div>
        </li>
      </ul>
  
</template>

<style scoped>
 .circle-icon {
    vertical-align: middle;
    width: 15%;
  }
</style>