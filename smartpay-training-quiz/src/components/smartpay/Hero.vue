<script setup>
  const props = defineProps({
    'hero_image': String
  })
</script>

<template>
  <section class="usa-hero padding-y-4" :style="{backgroundImage: `url(${hero_image}`}">
    <div class="grid-container">
      <div class="grid-row">
        <h1 class="usa-hero__heading tablet:grid-col-6">
          <span class="usa-hero__heading--alt">
            <slot></slot>
          </span>
        </h1>
      </div>
      <div class="grid-row">
        <p v-if="$slots.subheader" class="margin-bottom-0">
            <slot name="subheader"></slot>
        </p>
      </div>
    </div>
  </section>
</template>