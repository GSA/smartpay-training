<script setup>

</script>

<template>
  <div class="usa-prose">
    <h3>
      Edit User Profile
    </h3>
  </div>
  <div class="grid-row grid-gap">
    <div class="tablet:grid-col">
      <label
          for="input-full-name"
          class="usa-label"
      >
        Full Name
      </label>
      <input
          id="input-full-name"
          class="usa-input bg-base-lightest"
          name="input-full-name"
      >
    </div>
    <div class="tablet:grid-col">
      <label
          for="input-email"
          class="usa-label"
      >
        Email
      </label>
      <input
          id="input-email"
          class="usa-input bg-base-lightest"
          name="input-email"
      >
    </div>
  </div>
  <div class="grid-row grid-gap">
    <div class="tablet:grid-col">
      <label
          for="input-agency"
          class="usa-label"
      >
        Agency / Organization
      </label>
      <input
          id="input-agency"
          class="usa-input bg-base-lightest"
          name="input-agency"
      >
    </div>
    <div class="tablet:grid-col">
      <label
          class="usa-label"
          for="input-bureau"
      >
        Sub-Agency, Organization, or Bureau
      </label>
      <input
          id="input-bureau"
          class="usa-input bg-base-lightest"
          name="input-bureau"
      >
    </div>
  </div>
  <div class="grid-row grid-gap">
    <div class="tablet:grid-col">
      <button type="button" class="usa-button">Default</button>
    </div>
  </div>
</template>
