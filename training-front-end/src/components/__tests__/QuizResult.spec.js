import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import QuizResult from "../QuizResult.vue";
import CheckCircleIcon from "../icons/CheckCircleIcon.vue";
import CancelIcon from "../icons/CancelIcon.vue";
import {passing_result, failing_result} from './fixtures/sample_quiz_response'
import quiz from './fixtures/sample_quiz'

const passingProps_correct = {
  index: 1,
  question: quiz.content.questions[0], 
  result: passing_result.questions[0],
  didPass: true
}

const passingProps_incorrect = {
  index: 1,
  question: quiz.content.questions[1], 
  result: passing_result.questions[3],
  didPass: true
}

const failingProps_incorrect = {
  index: 1,
  question: quiz.content.questions[1], 
  result: failing_result.questions[1],
  didPass: false
}

const failingProps_correct = {
  index: 1,
  question: quiz.content.questions[0], 
  result: failing_result.questions[0],
  didPass: false
}

describe("QuizResult", () => {
  it('displays question text with number', async () => {
    const wrapper = mount(QuizResult, {props: passingProps_correct})
    const heading = wrapper.find('h4')
    expect(heading.text()).toBe('2. '+passingProps_correct.question.text)
  })

  it('displays check mark when answer is correct', async () => {
    const wrapper = mount(QuizResult, {props: passingProps_correct})
    const icon = wrapper.findComponent(CheckCircleIcon)
    expect(icon.exists()).toBe(true)
  })

  it('displays cancel mark when answer is incorrect', async () => {
    const wrapper = mount(QuizResult, {props: passingProps_incorrect})
    const icon = wrapper.findComponent(CancelIcon)
    expect(icon.exists()).toBe(true)
  })

  it('shows selected next to incorrect selection', async () => {
    const wrapper = mount(QuizResult, {props: failingProps_incorrect})
    const answer = wrapper.findAll('[data-test="answers"]')
    const label = answer[1].find('div')
    expect(label.text()).toBe('You Selected:')
  })
})

describe("QuizResult Failed", async () => {
  it('does not show correct answer when user did not select it', async () => {
    const wrapper = mount(QuizResult, {props: failingProps_incorrect})
    const answer = wrapper.findAll('[data-test="answers"]')
    const label = answer[0].find('div')
    expect(label.text()).toBe('')
  })

  it('indicates correct answer when used selected it', async () => {
    const wrapper = mount(QuizResult, {props: failingProps_correct})
    const answer = wrapper.findAll('[data-test="answers"]')
    const label = answer[1].find('div')
    expect(label.text()).toBe('Correct:')
  })

  it('highlights correct answer on failed tests when used selected it', async () => {
    const wrapper = mount(QuizResult, {props: failingProps_correct})
    const answer = wrapper.findAll('[data-test="answers"]')
    expect(answer[1].classes()).toContain('bg-base-lightest')
  })

  it('does not highlight answer on failed tests when used selected it', async () => {
    const wrapper = mount(QuizResult, {props: failingProps_correct})
    const answer = wrapper.findAll('[data-test="answers"]')
    expect(answer[0].classes()).not.toContain('bg-base-lightest')
  })
})

describe("QuizResult Passed", async () => {
  it('does shows the correct answer when user did not select it', async () => {
    const wrapper = mount(QuizResult, {props: passingProps_incorrect})
    const answer = wrapper.findAll('[data-test="answers"]')
    const label = answer[0].find('div')
    expect(label.text()).toBe('Correct:')
  })

  it('indicates correct answer when used selected it', async () => {
    const wrapper = mount(QuizResult, {props: passingProps_correct})
    const answer = wrapper.findAll('[data-test="answers"]')
    const label = answer[1].find('div')
    expect(label.text()).toBe('Correct:')
  })

  it('highlights correct answer tests when used selected it', async () => {
    const wrapper = mount(QuizResult, {props: passingProps_correct})
    const answer = wrapper.findAll('[data-test="answers"]')
    expect(answer[1].classes()).toContain('bg-base-lightest')
  })

  it('does highlight answer on failed tests when used selected it', async () => {
    const wrapper = mount(QuizResult, {props: passingProps_incorrect})
    const answer = wrapper.findAll('[data-test="answers"]')
    expect(answer[0].classes()).toContain('bg-base-lightest')
  })
})
