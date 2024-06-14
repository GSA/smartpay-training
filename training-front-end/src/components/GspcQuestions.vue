<script setup>
  import { ref, onMounted, onBeforeUnmount, computed, reactive} from "vue"
  import { exit_warning } from '../stores/session_manager'
  import GspcQuestion from "./GspcQuestion.vue"
  import QuizCounter from "./QuizCounter.vue"
  import NavigateNext from "./icons/NavigateNext.vue"
  import NavigateBack from "./icons/NavigateBack.vue"
  import SpinnerGraphic from './SpinnerGraphic.vue'

  const emit = defineEmits(['submitGspcRegistration', 'startQuiz'])
  
  
  const props = defineProps({
    'questions': {
      type: Array,
      required: true
    },
  })

  const question_index = ref(0)
  const user_answers = reactive([])
  const has_submitted = ref(false)
  let show_intro = ref(true)

  const number_of_questions = computed(() => props.questions.length)
  const current_question = computed(() => props.questions[question_index.value])
  const is_current_unanswered = computed(() => user_answers[question_index.value] === undefined )
  const last_question = computed(() => question_index.value == (props.questions.length -1))
  const can_submit = computed(() => !is_current_unanswered.value && !has_submitted.value)

  function start() {
    show_intro.value = false
    emit('startQuiz')
  }

  onMounted(async () => {
    window.addEventListener("beforeunload", exit_warning)
    const state = { page: 0 };
    history.replaceState(state, "", "");
  })

  onBeforeUnmount(() => {
    window.removeEventListener('beforeunload', exit_warning)
  })

  function next_question(){
    question_index.value += 1
    const state = { page: question_index.value }
    const url = "" 
    history.pushState(state, "", url)
  }

  function previous_question(){
    question_index.value -= 1
    const state = { page: question_index.value }
    const url = ""
    history.pushState(state, "", url)
  }

  function select_answer(event) {
    user_answers[question_index.value] = event
  }

  async function submit_quiz() {
    has_submitted.value = true
    emit('submitGspcRegistration', user_answers)
  }

</script>

<template>
  <section 
    v-if="show_intro"
    class="usa-prose margin-y-1 usa-prose"
  >
    <h2>GSA SmartPay Program Certification (GSPC) Requirements</h2>
    <p>
      To earn your GSA SmartPay Program Certification you will need to:

      <ul>
        <li>Complete a minimum of seven classes, including two GSA-qualifying classes and five Bank/brand-qualifying classes, during the annual GSA SmartPay Training Forum.</li>
        <li>Have a minimum of six months of continuous, hands-on experience working with the GSA SmartPay program.</li>
      </ul> 

      You can complete the verification steps to receive your GSA SmartPay Program Certification if you meet these requirements.
    </p>
    <button
      id="start-button"
      class="usa-button"
      @click="start"
    >
      Continue to verify coursework and experience
    </button>
  </section>
  <div 
    v-else
  >
    <QuizCounter
      :current="question_index + 1"
      :total="number_of_questions"
    />

    <section class="usa-prose margin-y-4 bg-white padding-4 border-1px border-base-lighter radius-md">
      <GspcQuestion 
        :key="question_index" 
        :question="current_question" 
        :selection="user_answers[question_index]"
        @select_answer="select_answer"
      />
    </section>
    <div v-if="last_question">
      <button
        id="submit-button"
        class="usa-button margin-bottom-2"
        :disabled="!can_submit"
        @click="submit_quiz"
      >
        Submit quiz
      </button>
      <!--display spinner along with submit button in one row for desktop-->
      <div
        v-if="has_submitted"
        class="display-none tablet:display-block tablet:grid-col-1 tablet:padding-top-3 tablet:margin-left-neg-1"
      >
        <SpinnerGraphic />
      </div>
      <!--display spinner under submit button for mobile view-->
      <div
        v-if="has_submitted"
        class="tablet:display-none margin-top-1 text-center"
      >
        <SpinnerGraphic />
      </div>
    </div>
    <div v-else>
      <button
        id="next-button"
        class="usa-button margin-bottom-2"
        :disabled="is_current_unanswered"
        @click="next_question"
      >
        <span class="usa-pagination__link-text">Next</span>
        <NavigateNext />
      </button>
    </div>
    <br>
    <button
      v-if="question_index"
      id="previous-button"
      type=""
      class="usa-button--outline"
      @click="previous_question"
    >
      <NavigateBack />
      <span class="usa-pagination__link-text">Back</span>
    </button>
  </div>
</template>