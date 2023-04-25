<script setup>
    import {computed, onMounted } from 'vue';
    import CheckCircleIcon from './icons/CheckCircleIcon.vue';
    import ErrorIcon from './icons/ErrorIcon.vue';
    import QuizResult from './QuizResult.vue';
    import USWDS from "@uswds/uswds/js";
    const { accordion } = USWDS;

    const props = defineProps({
      'quiz':{
        type: Object,
        required: true
      },
      'quizResults': {
        type: Object,
        required: true
      }
    });

    defineEmits(['reset_quiz'])

    const result_string = computed(() => `${props.quizResults.correct_count} of ${props.quizResults.question_count}`)
    const percentage = computed(() => (props.quizResults.percentage * 100).toFixed(0))

    function windowStateListener() {
      window.location = import.meta.env.BASE_URL
    }

    onMounted(() => {
      window.addEventListener("popstate", windowStateListener)
      accordion.init()
    })
</script>

<template>
  <div class="usa-prose">
    <div v-if="quizResults.passed">
      <div class="usa-prose">
        <h2 class="usa-alert__heading">
          <span class="text-green font-body-2xl">
            <CheckCircleIcon />
          </span>
          You passed the quiz!
        </h2>
      </div>
      <p>
        You got <b>{{ result_string }}</b> questions correct, for a total score of <b>{{ percentage }}%</b>, which meets the 75% or higher requirement to pass.
      </p>
      <button
        class="usa-button usa-button--outline margin-bottom-3"
      >
        Download your certificate of completion
      </button>
    </div>
    <div v-else>
      <div class="usa-prose">
        <h2 class="usa-alert__heading">
          <span class="text-secondary-dark font-body-2xl">
            <ErrorIcon />
          </span>
          You did not pass
        </h2>
      </div>
      <p>
        You got <b>{{ result_string }}</b> questions correct, for a total score of <b>{{ percentage }}%</b>, which does <b>not</b> meet the 75% or higher requirement to pass.
      </p>
      <button
        class="usa-button margin-bottom-2"
        @click="$emit('reset_quiz')"
      >
        Retake the quiz
      </button>
    </div>
    <div class="tablet:grid-col-8">
      <div class="usa-accordion usa-accordion--bordered">
        <QuizResult 
          v-for="(question, index) in quiz.content.questions" 
          :key="question.id"
          :question="question"
          :result="quizResults.questions[index]"
          :index="index"
        />
      </div>
    </div>
  </div>
</template>