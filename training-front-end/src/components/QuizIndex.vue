<script setup>
  import { ref, onErrorCaptured, onBeforeMount } from 'vue';
  import Alert from './Alert.vue';
  import Quiz from './Quiz.vue';
  import Loginless from './Loginless.vue';
  import QuizIntro from './QuizIntro.vue';
  import QuizResults from './QuizResults.vue';

  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const quiz = ref()
  const props = defineProps(['quiz_id', 'page_id', 'title', 'header', 'subhead', 'hero_image'])

  onBeforeMount(async () => {
    // import quiz_temp_json from '../dev_data/travel_a_opc.json'
    // quiz.value = quiz_temp_json
    const res = await fetch(`${base_url}/api/v1/quizzes/${props.quiz_id}`)
    if (!res.ok) {
      // TODO: give the user something better than this
      throw new Error("Sorry, a server error was encountered.")
    }
    quiz.value = await res.json();
  })

  onErrorCaptured((err) => {
    console.log("Error from child component", err)
    setError(err)
  })

	const error = ref()
  const isStarted = ref(false)
  const isSubmitted = ref(false)
  const quizResults = ref()
  const quizSubmission = ref()

  function startQuiz() {
    /* Fired by the Start Quiz button on the first page */
    isStarted.value = true
  }
  
  function resetQuiz() {
    /* Fired when user wants to retake quiz after unsuccesful attemtp */
    isSubmitted.value = false
    quizSubmission.value = undefined
    quizResults.value = undefined
  }

  async function submitQuiz(user_answers) {
    const url = `${base_url}/api/v1/quizzes/${props.quiz_id}/submission`
    
    let res
    
    try {
      res = await fetch(url, { 
        method: "POST", 
        headers: { 'Content-Type': 'application/json'},
        body:  JSON.stringify( {'responses': user_answers}) 
      })
    } catch(e) {
      // server error
      console.log("error connecting to api", e)
      throw e
    }
    if (!res.ok){
      // non 2xx response from server
      // TODO: this could happen with an expired jwt
      // should offer solution for user in that case.
      const e = new Error("There was a problem connecting with the server")
      e.name = "Server Error"
      setError(e)
    }
    quizResults.value = await res.json()
    isStarted.value = false
    isSubmitted.value = true
  }

  function startLoading() {
    error.value = undefined
  }

	function setError(event){
    error.value = event
	}
</script>

<template>
  <div class="bg-base-lightest padding-top-4 padding-bottom-4">
  <div  class="grid-container" data-test="post-submit">
    <div class="grid-row">
      <div class="tablet:grid-col-12">
        <Alert v-if="error" class="tablet:grid-col-8" status="warning" :heading="error.name">
          {{ error.message }}
        </Alert>
        <Suspense>
          <template #fallback>
            …Loading
          </template>
          <Loginless @startLoading="startLoading"  @error="setError" :page_id="page_id" :title="title" :header="header">
            <Quiz v-if="isStarted" :quiz="quiz" :title="title" :quiz_id="quiz_id" @submitQuiz=submitQuiz class="grid-col-8"/>
            <div v-else>
              <QuizResults v-if="isSubmitted"  @reset_quiz="resetQuiz" :quizResults="quizResults" :quiz="quiz"/>
              <QuizIntro v-else @start="startQuiz" />
            </div>
          </Loginless>
        </Suspense>
      </div>
    </div>
  </div>
  </div>
</template>