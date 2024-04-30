import { describe, it, expect} from 'vitest'
import { shallowMount } from '@vue/test-utils'
import GspcQuestion from '@/components/GspcQuestion.vue'

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
  const userAnswer = 0 // Assuming the user selected the first choice

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
    expect(wrapper.emitted('select_answer')[0]).toEqual([0])
  })

  it('correctly highlights selected choice', async () => {
    const wrapper = shallowMount(GspcQuestion, {
      props: { question, selection: userAnswer }
    })
    const selectedChoice = wrapper.find(`input[value="${userAnswer}"]`)
    expect(selectedChoice.element.checked).toBe(true)
  })
})