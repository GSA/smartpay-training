<script setup>
  import { ref, onMounted, onBeforeUnmount, computed, reactive} from "vue"
  import QuizQuestion from "./QuizQuestion.vue"
  import QuizCounter from "./QuizCounter.vue"
  import NavigateNext from "./icons/NavigateNext.vue"
  import NavigateBack from "./icons/NavigateBack.vue"
  

  const emit = defineEmits(['submitQuiz'])
  const props = defineProps({
    'quiz':{
      type: Object,
      required: true
    },
    'title': {
      type: String,
      required: true
    },
    'topic': {
      type: String,
      required: true
    },
    'audience': {
      type: String,
      required: true
    }
  })

  const question_index = ref(0)
  const user_answers = reactive([])
  const acknowledge = ref(false)

  const number_of_questions = computed(() => props.quiz['content']['questions'].length)
  const is_quiz_complete = computed(() => user_answers.length === number_of_questions.value)
  const current_question = computed(() => props.quiz['content']['questions'][question_index.value])
  const is_current_unanswered = computed(() => user_answers[question_index.value] === undefined )
  const show_acknowledge = computed(() => is_quiz_complete.value && (question_index.value >= number_of_questions.value))

  const user_string_lookup = {
    "AccountHoldersApprovingOfficials": "a card/account holder or approving official",
    "ProgramCoordinators": "an agency/organization program coordinator (A/OPC)"
  }
 
  function exit_warning(event) {
    event.preventDefault()
    return event.returnValue = "Are you sure you want to exit?";
  }
  
  function windowStateListener(event) {
    if (event.state) {
        question_index.value = event.state.page
      }
  }

  onMounted(async () => {
    window.addEventListener("beforeunload", exit_warning)
    const state = { page: 0 };
    history.replaceState(state, "", "");
    window.addEventListener("popstate", windowStateListener)
  })

  onBeforeUnmount(() => {
    window.removeEventListener('popstate', windowStateListener)
    window.removeEventListener('beforeunload', exit_warning)
  })

  function next_question(){
    question_index.value += 1
    const state = { page: question_index.value }
    const url = ""
    history.pushState(state, "", url)
  }

  function previous_question(){
    if (question_index.value <= 0) {
      return
    }
    question_index.value -= 1
    const state = { page: question_index.value }
    const url = ""
    history.pushState(state, "", url)
  }

  function select_answer(event) {
    user_answers[question_index.value] = event
  }

  async function submit_quiz() {
    emit('submitQuiz', user_answers)
  }

</script>
<template>
  <section
    v-if="show_acknowledge"
    class="margin-y-1"
  >
    <div class="usa-checkbox padding-4">
      <input
        id="acknowledge"
        v-model="acknowledge"
        class="usa-checkbox__input"
        type="checkbox"
        name="acknowledge"
        value="sojourner-truth"
      >
      <label
        class="usa-checkbox__label"
        for="acknowledge"
      >
        ACKNOWLEDGMENT STATEMENT<br>“I acknowledge that I’ve read and understand the policies and regulations that govern the use of the GSA SmartPay® {{ topic.toLowerCase() }} card/account, as well as understand my role and responsibilities as {{ user_string_lookup[audience] }} as outlined in this training course.” 
      </label>
    </div>
    <div class="grid-row">
      <button
        class="usa-button margin-y-3"
        :disabled="!acknowledge"
        @click="submit_quiz"
      >
        Submit quiz
      </button>
    </div>
  </section>

  <div v-else>
    <QuizCounter
      :current="question_index + 1"
      :total="number_of_questions"
    />

    <section class="usa-prose margin-y-4 bg-white padding-4 border-1px border-base-lighter radius-md">
      <QuizQuestion 
        :key="question_index" 
        :question="current_question" 
        :selection="user_answers[question_index]"
        @select_answer="select_answer"
      />
    </section>

    <button
      class="usa-button margin-bottom-2"
      :disabled="is_current_unanswered"
      @click="next_question"
    >
      <span class="usa-pagination__link-text">Next</span>
      <NavigateNext />
    </button>
    <br>
    <button
      v-if="question_index"
      type=""
      class="usa-button usa-button--unstyled"
      @click="previous_question"
    >
      <NavigateBack />
      <span class="usa-pagination__link-text">Back</span>
    </button>
  </div>
</template>