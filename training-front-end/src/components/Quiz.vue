<script setup>
  import { ref, onMounted, computed, reactive, onBeforeMount} from "vue"
  import { profile } from '../stores/user'
  import { useStore } from '@nanostores/vue'
  import QuizQuestion from "./QuizQuestion.vue"
  import QuizCounter from "./QuizCounter.vue"
  import NavigateNext from "./icons/NavigateNext.vue"
  import NavigateBack from "./icons/NavigateBack.vue"
  import quiz from '../dev_data/travel_a_opc.json'

  const props = defineProps(['title'])
  const user = useStore(profile)
  
  const question_index = ref(0)
  const user_answers = reactive([])
  const number_of_questions = quiz['questions'].length
  const quiz_complete = computed(() => user_answers.length === quiz.questions.length)
  const current_question = computed(() => quiz['questions'][question_index.value])
  const current_unaswered = computed(() => user_answers[question_index.value] == null )
  const question_complete = computed(() => quiz_complete.value && (question_index.value >= quiz.questions.length))
  const acknowledge = ref(false)

  function exit_warning(event) {
    event.returnValue = ''
    event.preventDefault()
  }
  

  onMounted(() => {
    window.addEventListener("beforeunload", exit_warning)
    const state = { page: 0 };
    history.replaceState(state, "", "");

    window.onpopstate = event => {
      if (event.state) {
        question_index.value = event.state.page
      }
    }
  })

  function next_question(){
    question_index.value += 1
    const state = { page: question_index.value }
    const url = ""
    history.pushState(state, "", url)
  }

  function previous_question(e){
    e.preventDefault()
    question_index.value -= 1
    const state = { page: question_index.value }
    const url = ""
    history.pushState(state, "", url)
  }

  function select_answer(event) {
    user_answers[question_index.value] = parseInt(event)
  }

</script>
<template >
    <section v-if="question_complete" class="margin-y-4">
        <div class="usa-checkbox padding-4">
          <input
            class="usa-checkbox__input"
            id="check-historical-truth"
            type="checkbox"
            name="historical-figures"
            value="sojourner-truth"
            v-model="acknowledge"
          />
          <label class="usa-checkbox__label" for="check-historical-truth"
          >ACKNOWLEDGMENT STATEMENT<br/>“I acknowledge that I’ve read and understand the policies and regulations that govern the use of the GSA SmartPay® travel account, as well as understand my role and responsibilities as an A/OPC as outlined in this training course.” </label>
        </div>
      <div class="grid-row">
        <button class="usa-button margin-y-3"  :disabled="!acknowledge">Submit Quiz</button>
      </div>
    </section>
    <div v-else>
      <QuizCounter :current="question_index + 1" :total="number_of_questions" />
      <section class="usa-prose margin-y-4 bg-white padding-4 ">
        <QuizQuestion 
          :question="current_question" 
          :selection="user_answers[question_index]" 
          @select_answer="select_answer"
          :key="question_index" />
      </section>
      <button class="usa-button margin-bottom-2" :disabled="current_unaswered" @click="next_question">
        <span class="usa-pagination__link-text">Next</span
        ><NavigateNext />
      </button><br />
      <button v-if="question_index" type="" @click="previous_question" class="usa-button usa-button--unstyled">
        <NavigateBack />
        <span class="usa-pagination__link-text">Back</span>
      </button>
    </div>
</template>