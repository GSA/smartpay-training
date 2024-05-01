import { describe, it, expect, vi} from 'vitest'
import { shallowMount, mount } from '@vue/test-utils'
import GspcQuestions from '../GspcQuestions.vue'

async function startForm(wrapper) {
  await wrapper.find('#start-button').trigger('click')
}

async function selectAnswer(wrapper, index) {
  await wrapper.find(`input[value="${index}"]`).setChecked()  
}

describe('GspcQuestions', () => {
  const questions = [
    {"id": 0, 
      "text": "Question 1", 
      "type": "MultipleChoiceSingleSelect",  
      "choices": [{"id": 0, "text": "Yes", "correct": true}, {"id": 1, "text": "No", "correct": false}]}, 
    {"id": 1, 
      "text": "Question 2", 
      "type": "MultipleChoiceSingleSelect", 
      "choices": [{"id": 0, "text": "Yes", "correct": true}, {"id": 1, "text": "No", "correct": false}]},
  ]

  it('shows intro section initially and hides it on "Continue" button click', async () => {
    const wrapper = shallowMount(GspcQuestions, {
      props: { questions }
    })

    expect(wrapper.find('.usa-prose').exists()).toBe(true)
    expect(wrapper.find('#start-button').exists()).toBe(true)

    await wrapper.find('#start-button').trigger('click')

    expect(wrapper.find('#start-button').exists()).toBe(false)
  })

  it('Nest button should be disabled when no answer has been selected', async () => {
    const wrapper = await shallowMount(GspcQuestions, {
      props: { questions }
    })

    await startForm(wrapper)

    const button = wrapper.find('#next-button')
    expect(button.element.disabled).toBe(true)
  })

  it('Nest button should not be disabled when an answer has been selected', async () => {
    const wrapper = mount(GspcQuestions, {
      props: { questions }
    })

    await startForm(wrapper)
    await selectAnswer(wrapper, 0)

    const button = wrapper.find('#next-button')
    expect(button.element.disabled).toBe(false)
  })

  it('Previous button does not show on first question', async () => {
    const wrapper = shallowMount(GspcQuestions, {
      props: { questions }
    })

    await startForm(wrapper)

    // Assert that the previous button does not exist
    const previousButton = wrapper.find('#previous-button');
    expect(previousButton.exists()).toBe(false);
  })

  it('navigates to the next question and back', async () => {
    const wrapper = mount(GspcQuestions, {
      props: { questions }
    })

    await startForm(wrapper)
    await selectAnswer(wrapper, 0)
    
    await wrapper.find('#next-button').trigger('click') 
    
    expect(wrapper.text()).toContain("Question 2")

    await wrapper.find('#previous-button').trigger('click') // Move to previous question

    expect(wrapper.text()).toContain("Question 1")
  })

  it('submits the quiz', async () => {
    const wrapper = mount(GspcQuestions, {
      props: { questions }
    })

    await startForm(wrapper)

    await selectAnswer(wrapper, 0) 
    await wrapper.find('#next-button').trigger('click') 
    
    await selectAnswer(wrapper, 0)
    await wrapper.find('.usa-button').trigger('click') // Submit quiz

    expect(wrapper.emitted('submitGspcRegistration')).toBeTruthy()
    expect(wrapper.vm.has_submitted).toBe(true)
  })

  it('shows "Submit" button when on the last question', async () => {
    const wrapper = mount(GspcQuestions, {
      props: { questions }
    })

    await startForm(wrapper)

    await selectAnswer(wrapper, 0) 
    await wrapper.find('#next-button').trigger('click') 

    const submitButton = wrapper.find('#submit-button');
    expect(submitButton.exists()).toBe(true);
  })

  it('should add window listeners on mount', async () => {
    const addEventListenerMock = vi.spyOn(global, 'addEventListener').mockImplementation(() => {})
    await mount(GspcQuestions, {
      props: { questions }
    })

    expect(addEventListenerMock).toBeCalled(1)
    expect(addEventListenerMock).toHaveBeenNthCalledWith(1, 'beforeunload', expect.any(Function))
  })

  it('should remove window listeners on mount', async () => {
    const wrapper = mount(GspcQuestions, {
      props: { questions }
    })
    const removeEventListenerMock = vi.spyOn(global, 'removeEventListener').mockImplementation(() => {})

    wrapper.unmount()
    expect(removeEventListenerMock).toBeCalled(1)
    expect(removeEventListenerMock).toHaveBeenNthCalledWith(1, 'beforeunload', expect.any(Function))
  })
})