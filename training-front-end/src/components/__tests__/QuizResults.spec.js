import { describe, it, expect, vi, afterEach } from "vitest";
import { mount } from "@vue/test-utils";
import QuizResults from "../QuizResults.vue";
import QuizResult from "../QuizResult.vue";
import CheckCircleIcon from "../icons/CheckCircleIcon.vue";
import ErrorIcon from "../icons/ErrorIcon.vue";
import quiz from './fixtures/sample_quiz'
import {passing_result, failing_result} from './fixtures/sample_quiz_response'

const userSelections = [
  {question_id: 0, response_ids: [0]},
  {question_id: 1, response_ids: [0]}
]

describe("QuizResults", () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('displays passing result', async () => {
    const wrapper = mount(QuizResults, {props: {quiz, quizResults: passing_result, userSelections}})
    expect(wrapper.text()).toContain('You passed the quiz!')
    expect(wrapper.text()).toContain('You got 2 of 2 questions correct, for a total score of 100%, which meets the 75% or higher requirement to pass.')
  })

  it('displays checkmark on passing result', async () => {
    const wrapper = mount(QuizResults, {props: {quiz, quizResults: passing_result, userSelections}})
    const checkIcon = wrapper.findComponent(CheckCircleIcon)
    expect(checkIcon.exists()).toBe(true)
  })

  it('displays failing result', async () => {
    const wrapper = mount(QuizResults, {props: {quiz: quiz, quizResults: failing_result, userSelections}})
    expect(wrapper.text()).toContain('You did not pass')
    expect(wrapper.text()).toContain('You got 1 of 2 questions correct, for a total score of 50%, which does not meet the 75% or higher requirement to pass.')
  })

  it('displays error icon on passing result', async () => {
    const wrapper = mount(QuizResults, {props: {quiz, quizResults: failing_result, userSelections}})
    const errorIcon = wrapper.findComponent(ErrorIcon)
    expect(errorIcon.exists()).toBe(true)
  })

  it('displays a result for each question', async () => {
    const wrapper = mount(QuizResults, {props: {quiz, quizResults: failing_result, userSelections}})
    const results = wrapper.findAllComponents(QuizResult)
    expect(results.length).toBe(2)
  })

  it('loads base url on popstate', async() => {
    const setMock = vi.fn();
    await mount(QuizResults, {props: {quiz: quiz, quizResults: passing_result, userSelections}})
    vi.spyOn(global.window, 'location', 'set').mockImplementation(setMock)

    const popEvent = new Event('popstate');
    window.dispatchEvent(popEvent)

    expect(setMock).toHaveBeenCalledWith(import.meta.env.BASE_URL)
  })

  it('retry button emits reset_quiz event', async() => {
    const wrapper = await mount(QuizResults, {props: {quiz: quiz, quizResults: failing_result, userSelections}})
    const button = wrapper.find('button')
    await button.trigger('click')

    expect(wrapper.emitted()).toHaveProperty('reset_quiz')
  })
})