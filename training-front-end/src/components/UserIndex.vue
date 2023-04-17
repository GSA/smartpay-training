<script setup>
  /**
   * This component governs the display of the user's main profile page
   * When mounted, it will look for a token in the url query string:
   * http://example.com/home?t=some-token-value
   * 
	 * It will pass this token to the store to generate fetch a JWT
	 * from the backend.
	 * 
	 * Once a jwt is present in the store it will mount the user home component
   */

  import { onMounted, ref } from 'vue'
  import { profile, getUserFromToken } from '../stores/user'
  import { useStore } from '@nanostores/vue'
  import Alert from './USWDSAlert.vue'
  import UserHome from '../components/UserHome.vue'
  import Loginless from '../components/Loginless.vue';

  const user = useStore(profile)
  const base_url = import.meta.env.PUBLIC_API_BASE_URL

  const loaded = ref(false)

	const error = ref()

  onMounted(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('t')

    if (token) {
      try {
        await getUserFromToken(base_url, token)
      } catch(e) {
          error.value = e
      }
    } 
    loaded.value = true
  })

  function endLoading() {
    error.value = undefined
  }
	function setError(event){
		console.log(event)
	}

</script>

<template>
  <div  class="grid-container" data-test="post-submit">
    <div v-if="loaded" class="grid-container">
      <UserHome  v-if="user.jwt"/>
      <div v-else>
          <Alert v-if="error" class="tablet:grid-col-8" status="warning" :heading="error.name">
            {{ error.message }}
          </Alert>
          <Loginless @endLoading="endLoading" @error="setError"/>
      </div>
    </div>
  </div>
</template>