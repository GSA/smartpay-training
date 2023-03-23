<script setup>
  /**
   * This component is the wrapping element for a quiz.
   * When mounted, it will look for a token in the url query string:
   * http://example.com/quiz/some_quiz/?t=some-token-value
   * 
   * It will pass this token to the store to generate fetch a JWT
   * from the backend. The store will save it in local storage
   * 
   * Once a jwt is present in the store it will mount quiz components to 
   * actually take the quiz
   */

  import { onMounted, ref } from 'vue'
  import { profile, getUserFromToken } from '../stores/user'
  import { useStore } from '@nanostores/vue'
  import Alert from './Alert.vue'
  import Verify from './Verify.vue'
  import Quiz from './Quiz.vue'
  import Loginless from '../components/Loginless.vue';

  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const user = useStore(profile)

  const props = defineProps(['page_id', 'title'])

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

  function startLoading() {
    error.value = undefined
  }
	function setError(event){
    error.value = event
	}

</script>

<template>
  <div  class="grid-container" data-test="post-submit">
    <div v-if="loaded" class="grid-container">
      <Quiz :title="title" v-if="user.jwt"/>
      <div v-else>
          <Alert v-if="error" class="tablet:grid-col-8" status="warning" :heading="error.name">
            {{ error.message }}
          </Alert>
          <Loginless @startLoading="startLoading"  @error="setError" :page_id="page_id"/>
      </div>
    </div>
  </div>
</template>