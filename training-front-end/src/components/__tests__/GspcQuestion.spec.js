import { describe, it, expect} from 'vitest'
import { shallowMount } from '@vue/test-utils'
import GspcQuestion from '../GspcQuestion.vue'

describe('GspcQuestion', () => {
  // Sample question data for testing
  const question = {
    id: 0,
    text: 'Sample question text',
    type: 'MultipleChoiceSingleSelect',
    choices: [
      { id: 0, text: 'Option 1', correct: true },
      { id: 1, text: 'Option 2', correct: false }
    ]
  }

  // Sample user answer for testing
  const userAnswer = 0

  it('renders question text correctly', () => {
    const wrapper = shallowMount(GspcQuestion, {
      props: { question, selection: null }
    })
    expect(wrapper.text()).toContain(question.text)
  })

  it('renders choices correctly', () => {
    const wrapper = shallowMount(GspcQuestion, {
      props: { question, selection: null }
    })
    const choices = wrapper.findAll('input[type="radio"]')
    expect(choices.length).toBe(question.choices.length)
    question.choices.forEach((choice, index) => {
      expect(choices[index].element.value).toBe(choice.id.toString())
      expect(wrapper.text()).toContain(choice.text)
    })
  })

  it('emits select_answer event with correct choice', async () => {
    const wrapper = shallowMount(GspcQuestion, {
      props: { question, selection: null }
    })
    await wrapper.find('input[value="0"]').setChecked()
    const emittedEvent = wrapper.emitted('select_answer')[0][0]
    expect(emittedEvent).toEqual({
      correct: true,
      question: question.text,
      question_id: question.id,
      response: question.choices[0].text,
      response_id: question.choices[0].id
    })
  })

  it('emits select_answer event with incorrect choice', async () => {
    const wrapper = shallowMount(GspcQuestion, {
      props: { question, selection: null }
    })
  
    // Assuming the user selects the incorrect choice (index 1)
    await wrapper.find('input[value="1"]').setChecked()
  
    // Verify that the emitted event contains the expected data for an incorrect choice
    const emittedEvent = wrapper.emitted('select_answer')[0][0]
    expect(emittedEvent).toEqual({
      correct: false,  // Expecting the choice to be incorrect
      question: question.text,
      question_id: question.id,
      response: question.choices[1].text,  // Expecting the text of the incorrect choice
      response_id: question.choices[1].id   // Expecting the id of the incorrect choice
    })
  })

  it('correctly highlights selected choice', async () => {
    const wrapper = shallowMount(GspcQuestion, {
      props: { question, selection: {response_id: userAnswer} }
    })
    const selectedChoice = wrapper.find(`input[value="${userAnswer}"]`)
    expect(selectedChoice.element.checked).toBe(true)
  })
})