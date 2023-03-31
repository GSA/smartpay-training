<script setup>
  import { ref } from 'vue'
  import Alert from './Alert.vue'
  import Quiz from './Quiz.vue'
  import Loginless from './Loginless.vue';
  import QuizIntro from './QuizIntro.vue'

  const props = defineProps(['page_id', 'title'])

	const error = ref()
  const isStarted = ref(false)

  function startLoading() {
    error.value = undefined
  }
	function setError(event){
    error.value = event
	}

  function startQuiz() {
    isStarted.value = true
  }
</script>

<template>
  <div class="bg-base-lightest padding-top-1 padding-bottom-4">
  <div  class="grid-container" data-test="post-submit">
    <div class="grid-row">
      <div class="tablet:grid-col-7">
        <Alert v-if="error" class="tablet:grid-col-8" status="warning" :heading="error.name">
          {{ error.message }}
        </Alert>
        <Loginless @startLoading="startLoading"  @error="setError" :page_id="page_id" :title="title">
          <Quiz v-if="isStarted" :title="title" />
          <QuizIntro v-else @start="startQuiz" />
        </Loginless>
      </div>
    </div>
  </div>
  </div>
</template>