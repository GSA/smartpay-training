<script setup>
    import { ref, onMounted } from 'vue';
    const props = defineProps(['quizSubmission']);
    
    const gradedResults = ref();

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

      gradedResults.value = "You scored x out of x"
    })

</script>

<template>
  <div class="usa-prose">
    <h3>Quiz Results</h3>
    🎉 {{ gradedResults }} 🎉
    
    <p>
      <b>Dev only:</b> <br />
      results sent to server for grading:
    </p>
  </div>
  <code>
  {{ quizSubmission }}
  </code>
</template>