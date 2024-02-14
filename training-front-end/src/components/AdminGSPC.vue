<script setup>
  import USWDSAlert from './USWDSAlert.vue'
  import ValidatedTextArea from './ValidatedTextArea.vue';

  const props = defineProps({
    'emailAddresses': {
      type: String,
      required: true
    },
    'emailInvitationExpirationDate': {
      type: String,
      required: true
    },
    'certificationExpirationDate': {
      type: String,
      required: true
    },
  })
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
      <ValidatedTextArea
        v-model="user_input.name"
        client:load
        :validator="v_all_info$.name"
        label="Full Name"
        name="name"
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