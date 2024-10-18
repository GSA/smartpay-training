<script setup>
  import { ref, onErrorCaptured, onBeforeMount } from 'vue';
  import { useStore } from '@nanostores/vue'
  import { profile} from '../stores/user'
  import USWDSAlert from './USWDSAlert.vue'
  import Quiz from './QuizMain.vue';
  import Loginless from './LoginlessFlow.vue';
  import QuizIntro from './QuizIntro.vue';
  import QuizResults from './QuizResults.vue';

  const user = useStore(profile)
  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const quiz = ref()
  const userSelections = ref([])

  const props = defineProps({
    'topic': {
      type: String,
      required: true,
    },
    'audience': {
      type: String,
      required: true,
    }, 
    'pageId': {
      type: String,
      required: true,
    }, 
    'title': {
      type: String,
      required: true,
    },
    'header': {
      type: String,
      required: true,
    },
    'subhead': {
      type: String,
      required: true,
    }
  })

  onBeforeMount(async () => {
    // import quiz_temp_json from '../dev_data/travel_a_opc.json'
    // quiz.value = quiz_temp_json
    const url = `${base_url}/api/v1/quizzes/?topic=${props.topic}&audience=${props.audience}&active=true`
    let res
    try {
      res = await fetch(url, {
        method: 'GET', 
        headers: {'Authorization': `Bearer ${user.value.jwt}`}
      })
    } catch(e) {
      const err = new Error("Sorry, a server error was encountered.")
      err.name = "Server Error!"
      setError(err)
      return
    }

    if (!res.ok) {
      const err = new Error("Sorry, a server error was encountered.")
      err.name = "Server Error!"
      setError(err)
      return
    }
    const filtered_quizzes =  await res.json();
    quiz.value = filtered_quizzes[0]
  })

  onErrorCaptured((err) => {
    setError(err)
    return false
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
    /* Fired when user wants to retake quiz after unsuccessful attempt */
    isSubmitted.value = false
    quizSubmission.value = undefined
    quizResults.value = undefined
  }

  async function submitQuiz(user_answers) {
    userSelections.value = user_answers
    const url = `${base_url}/api/v1/quizzes/${quiz.value.id}/submission`
    
    let res
    
    try {
      res = await fetch(url, { 
        method: "POST", 
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.value.jwt}`
        },
        body:  JSON.stringify( {'responses': user_answers}) 
      })
    } catch(e) {
      const err = new Error("There was a problem connecting with the server")
      err.name = "Server Error"
      setError(err)
      return 
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
  <div 
    class="padding-top-4 padding-bottom-4" 
    :class="{'bg-base-lightest': isStarted && !isSubmitted}"
  >
    <div
      class="grid-container"
      data-test="post-submit"
    >
      <div class="grid-row">
        <div class="tablet:grid-col-12">
          <USWDSAlert
            v-if="error"
            class="tablet:grid-col-12"
            status="error"
            :heading="error.name"
          >
            {{ error.message }}
          </USWDSAlert>
          <Suspense>
            <template #fallback>
              …Loading
            </template>
            <Loginless
              :page-id="pageId"
              :title="title"
              :header="header"
              link-destination-text="the training quiz"
              @start-loading="startLoading"
              @error="setError"
            >
              <template #initial-greeting>
                <h2>Take the GSA SmartPay {{ header }} Quiz</h2>
                <p>Enter your email address to get access to the quiz. You'll receive an email with an access link.</p>
              </template>
              
              <template #more-info>
                <h2>Welcome!</h2>
                <p>Before you can take a quiz, you'll need to create and complete your profile.</p>
              </template>

              <Quiz
                v-if="isStarted"
                :quiz="quiz"
                :title="title"
                :topic="topic"
                :audience="audience"
                class="desktop:grid-col-8"
                @submit-quiz="submitQuiz"
              />
              <div v-else>
                <QuizResults
                  v-if="isSubmitted"
                  :quiz-results="quizResults"
                  :quiz="quiz"
                  @reset_quiz="resetQuiz"
                />
                <QuizIntro
                  v-else
                  :title="title"
                  @start="startQuiz"
                />
              </div>
            </Loginless>
          </Suspense>
        </div>
      </div>
    </div>
  </div>
</template>