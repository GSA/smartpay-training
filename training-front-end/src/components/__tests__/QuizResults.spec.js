import { describe, it, expect, vi, afterEach } from "vitest";
import { mount } from "@vue/test-utils";
import QuizResults from "../QuizResults.vue";
import quiz from './fixtures/sample_quiz'
import {passing_result, failing_result} from './fixtures/sample_quiz_response'


describe("QuizResults", () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('displays passing result', async () => {
    const wrapper = mount(QuizResults, {props: {quiz: quiz, quizResults: passing_result}})
    expect(wrapper.text()).toContain('You passed')
    expect(wrapper.text()).toContain('You answered 2 correct out of 2 for a score of 100%')
  })

  it('displays failing result', async () => {
    const wrapper = mount(QuizResults, {props: {quiz: quiz, quizResults: failing_result}})
    expect(wrapper.text()).toContain('You did not pass')
    expect(wrapper.text()).toContain('You correctly answered 1 correct out of 2 for a score of 50%')
  })

  it('loads base url on popstate', async() => {
    const setMock = vi.fn();
    const wrapper = await mount(QuizResults, {props: {quiz: quiz, quizResults: passing_result}})
    vi.spyOn(global.window, 'location', 'set').mockImplementation(setMock)

    const popEvent = new Event('popstate');
    window.dispatchEvent(popEvent)

    expect(setMock).toHaveBeenCalledWith(import.meta.env.BASE_URL)
  })

  it('retry button emits reset_quiz event', async() => {
    const wrapper = await mount(QuizResults, {props: {quiz: quiz, quizResults: failing_result}})
    const button = wrapper.find('button')
    button.trigger('click')

    expect(wrapper.emitted()).toHaveProperty('reset_quiz')
  })
})