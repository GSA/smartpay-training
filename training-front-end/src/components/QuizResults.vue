<script setup>
    import {computed, onMounted } from 'vue';
    import Cancel from './icons/Cancel.vue';

    const props = defineProps(['quiz', 'quizResults']);
    const emits = defineEmits(['reset_quiz'])

    const passed = props.quizResults.passed
    const quiz_questions = props.quiz.content.questions

    const result_string = computed(() => `${props.quizResults.correct_count} correct out of ${props.quizResults.question_count}`)
    const percentage = computed(() => (props.quizResults.percentage * 100).toFixed(0))
    const questions_incorrect = computed(() => quiz_questions.filter((q, i) => !props.quizResults.questions[i].correct))

    function exit_warning(event) {
      event.preventDefault()
      return event.returnValue = "Are you sure you want to exit?";
    }
    
    function windowStateListener(event) {
      window.location = import.meta.env.BASE_URL
    }

    onMounted(() => {
      // send to API
      window.addEventListener("beforeunload", exit_warning)
      window.addEventListener("popstate", windowStateListener)
    })

</script>

<template>
  <div class="usa-prose">
    <h3>Quiz Results</h3>
    <div v-if="passed">
      <h3>🎉 You passed 🎉</h3>
      <p>
        You answered {{ result_string }} for a score of {{ percentage }}%
      </p>
      <p>Download a PDF of your training certificate [link: coming soon]</p>
    </div>
    <div v-else>
      <h3>😥 You did not pass 😥</h3>
      <p>
        You correctly answered {{ result_string }} for a score of {{ percentage }}% 
      </p>
      <h3>You answered these questions incorrectly</h3>
      <ul  class="usa-icon-list">
        <li v-for="question in questions_incorrect" class="usa-icon-list__item">
          <div class="usa-icon-list__icon text-red">
            <Cancel />
          </div>
          <div class="usa-icon-list__content">{{ question.text }}</div>
        </li>
      </ul>
      <button class="usa-button margin-y-4" @click="$emit('reset_quiz')">Try again</button>
    </div>
    

  </div>
</template>