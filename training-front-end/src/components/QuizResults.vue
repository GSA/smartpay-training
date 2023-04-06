<script setup>
    import {computed, onMounted } from 'vue';
    const props = defineProps(['quizSubmission', 'quizResults']);
    const passed = computed(() => props.quizResults.passed)
    const result_string = computed(() => `${props.quizResults.correct_count} correct out of ${props.quizResults.question_count}`)
    const percentage = computed(() => (props.quizResults.percentage * 100).toFixed(0))

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
      🎉 You passed 🎉
      <p>
        You answered {{ result_string }} for a score of {{ percentage }}%
      </p>
    </div>
    <div v-else>
      😥 You did not pass 😥
      <p>
        You answered {{ result_string }} for a score of {{ percentage }}% 
      </p>
    </div>
    
    <p>
      <b>Dev only:</b> <br />
      quiz results from server:
    </p>
  </div>
  <code>
  {{ quizResults }}
  </code>
</template>