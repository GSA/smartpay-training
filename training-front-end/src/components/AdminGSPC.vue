<script setup>
  import USWDSAlert from './USWDSAlert.vue'
</script>

<template>
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <USWDSAlert
      v-if="error"
      status="error"
      :heading="error.name"
    >
      {{ error.message }}
    </USWDSAlert>
  </div>
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <h2>GSPC Send Email Notifications</h2>
    <p>
      Content here duis vulputate pellentesque commodo. Nullam congue nibh a diam porta, at tincidunt mi pellentesque. Curabitur at mollis erat. Pellentesque ultricies libero sem, sed ornare nisl faucibus sit amet. In vel dictum tortor. Nullam iaculis efficitur ipsum. Quisque pharetra euismod augue et placerat.
    </p>
    <p>
      Duis congue, eros eu volutpat suscipit, odio dui varius nisi, id bibendum ipsum nisi at libero. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer felis velit, sollicitudin a leo sagittis, iaculis efficitur turpis. Vivamus id mi sed sapien facilisis consequat pulvinar sed orci. Morbi tellus quam, consectetur in aliquet eu, auctor id urna.
    </p>
    <form 
      class="usa-search"
      role="search"
      @submit.prevent="search"
    >
      <label 
        class="usa-label" 
        for="email-addresses-textarea"
      >
        Email Addresses of GSA SmartPay Forum Attendees 
        <span class="text-secondary-dark">(*Required)</span>
      </label>
      <span v-if="validator.$error">
        <span
          v-for="error in validator.$errors"
          :id="error_id"
          :key="error.$property"
          class="usa-error-message"
          role="alert"
        >
          {{ error.$message }}
        </span>
      </span>
      <textarea
        id="email-addresses-textarea"
        class="usa-textarea usa-input tablet:grid-col-8"
        name="email-addresses-textarea"
      />
      <button 
        class="usa-button"
        type="submit"
      >
        <span class="usa-search__submit-text">
          Search
        </span>
      </button>
    </form>
  </div>
</template>