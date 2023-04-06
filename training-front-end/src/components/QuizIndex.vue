<script setup>
  import { ref, onErrorCaptured, computed } from 'vue';
  import Alert from './Alert.vue';
  import Quiz from './Quiz.vue';
  import Loginless from './Loginless.vue';
  import QuizIntro from './QuizIntro.vue';
  import QuizResults from './QuizResults.vue';

  const props = defineProps(['quiz_id', 'page_id', 'title', 'header', 'subhead', 'hero_image'])

	const error = ref()
  const isStarted = ref(false)
  const isSubmitted = ref(false)
  const quizResults = ref()
  const quizSubmission = ref()
  
  const hero_text = computed(() => isStarted.value ? `${props.header} Quiz` : props.header)
  function startQuiz() {
    /* Fired by the Start Quiz button on the first page */
    isStarted.value = true
  }
  
  function submitQuiz(e) {
    isStarted.value = false
    isSubmitted.value = true
    quizResults.value = e
  }

  function startLoading() {
    error.value = undefined
  }

  onErrorCaptured((err) => {
    console.log("got error in parent", err)
    setError(err)
  })

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
            <Quiz v-if="isStarted" :title="title" :quiz_id="quiz_id" @submitQuiz=submitQuiz class="grid-col-8"/>
            <div v-else>
              <QuizResults v-if="isSubmitted"  :quizResults="quizResults"  :quizSubmission="quizSubmission"/>
              <QuizIntro v-else @start="startQuiz" />
            </div>
          </Loginless>
        </Suspense>
      </div>
    </div>
  </div>
  </div>
</template>