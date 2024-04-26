<script setup>
  import { ref, onMounted, onBeforeUnmount, computed, reactive} from "vue"
  import { exit_warning } from '../stores/session_manager'
  import QuizQuestion from "./QuizQuestion.vue"
  import QuizCounter from "./QuizCounter.vue"
  import NavigateNext from "./icons/NavigateNext.vue"
  import NavigateBack from "./icons/NavigateBack.vue"
  import SpinnerGraphic from './SpinnerGraphic.vue'

  const emit = defineEmits(['submitGspcRegistration'])

  const questions = 
    [{"id": 0, 
        "text": "I have met the coursework requirement during the GSA SmartPay Training Forum by attending at least two GSA Qualifying classes and at least five Bank/Brand Qualifying classes, as outlined in Smart Bulletin No. 022.", 
        "type": "MultipleChoiceSingleSelect",  
        "choices": [{"id": 0, "text": "Yes", "correct": true}, {"id": 1, "text": "No", "correct": false}]}, 
      {"id": 1, 
        "text": "I have met the experience requirement by having a minimum of six months of continuous, hands-on experience working in an agency/organization's GSA SmartPay Program prior to receiving the GSPC.", 
        "type": "MultipleChoiceSingleSelect", 
        "choices": [{"id": 0, "text": "Yes", "correct": true}, {"id": 1, "text": "No", "correct": false}]},
      ]

      //GSPC
      //Id UserId JSON(List QuestionId QuestionSting AnswerId AnswerString Correct(bool)) CreatedOn 

  const question_index = ref(0)
  const user_answers = reactive([])
  const has_submitted = ref(false)
  let show_intro = ref(true)

  const number_of_questions = computed(() => questions.length)
  const current_question = computed(() => questions[question_index.value])
  const is_current_unanswered = computed(() => user_answers[question_index.value] === undefined )
  const last_question = computed(() => question_index.value == (questions.length -1))
  const can_submit = computed(() => !is_current_unanswered.value && !has_submitted.value)

  function start() {
    show_intro.value = false
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
    has_submitted.value = true
    emit('submitGspcRegistration', user_answers)
  }

</script>

<template>
  <section 
    v-if="show_intro"
    class="usa-prose margin-y-1 usa-prose"
  >
    <p>
      Now that you’ve completed the training portion of the GSA SmartPay® {{ title }}, you are ready to take the quiz.
    </p>
    <p>
      Once you’ve successfully passed the quiz, your certificate will be displayed. You can print the certificate or save it as a PDF.
    </p>
    <p>
      <b>Note:</b> Your quiz progress will not be saved if you navigate away.
    </p>
    <button
      class="usa-button"
      @click="start"
    >
      Continue to verify coursework and experience
    </button>
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
    <div v-if="last_question">
      <button
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
      type=""
      class="usa-button usa-button--unstyled"
      @click="previous_question"
    >
      <NavigateBack />
      <span class="usa-pagination__link-text">Back</span>
    </button>
  </div>
</template>