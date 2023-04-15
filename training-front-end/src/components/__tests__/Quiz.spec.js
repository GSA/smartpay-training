import { describe, it, expect, afterEach, beforeEach, vi} from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import quiz  from './fixtures/sample_quiz'
import Quiz from '../Quiz.vue'


describe('Quiz', () => {
  let wrapper 
  let addEventListenerMock
  let removeEventListenerMock
  
  beforeEach(async () => {
    addEventListenerMock = vi.spyOn(global, 'addEventListener').mockImplementation(() => {})
    removeEventListenerMock = vi.spyOn(global, 'removeEventListener').mockImplementation(() => {})
    wrapper = await mount(Quiz, { 
      props: {"quiz":quiz, "title": "Astro Quiz!"}
    })
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders initial view of first question', async () => {
    const heading = wrapper.find('h3')
    expect(heading.text()).toBe(quiz.content.questions[0].text)
  })

  it('renders radiobuttons for each choice', async () => {
    const inputs = wrapper.findAll('input[type="radio"]')
    expect(inputs.length).toBe(2)
  })

  it('renders labels with text for each choice', async () => {
    const labels = wrapper.findAll('label')
    expect(labels.length).toBe(2)
    expect(labels[0].text()).toBe(quiz.content.questions[0].choices[0].text)
    expect(labels[1].text()).toBe(quiz.content.questions[0].choices[1].text)
  })

  it('shows current question and total questions', async () => {
    const counter = wrapper.find('[data-test="quiz-counter"]')
    expect(counter.text()).toBe("Question 1 of 2 Questions")
  })

  it('submit button should be disabled when no answer has been selected', async () => {
    const button = wrapper.find('button')
    expect(button.element.disabled).toBe(true)
  })

  it('submit button should not be disabled when an answer has been selected', async () => {
    const radioButtons = wrapper.findAll('input[type="radio"]')
    await radioButtons[0].setChecked()    
    const button = wrapper.find('button')
    expect(button.element.disabled).toBe(false)
  })

  it('should move to the next question when next-button is clicked', async () => {
    const radioButtons = wrapper.findAll('input[type="radio"]')
    await radioButtons[0].setChecked()
    
    const button = wrapper.find('button')
    button.trigger('click')
    await flushPromises()

    const heading = wrapper.find('h3')
    expect(heading.text()).toBe(quiz.content.questions[1].text)

    const labels = wrapper.findAll('label')
    expect(labels.length).toBe(4)
  })

  it('should display acknowledgement box with disabled submit after all questions have been answered', async () => {
    const selects = [1, 2]
    for (const i of selects) {
      const radioButtons = wrapper.findAll('input[type="radio"]')
      await radioButtons[i].setChecked()
      const button = wrapper.find('button')
      button.trigger('click')
      await flushPromises()
    }
    expect(wrapper.text()).toContain('ACKNOWLEDGMENT STATEMENT')
    const button = wrapper.find('button')
    expect(button.element.disabled).toBe(true)
  })

  it('should emit answers after quiz is submitted', async () => {
    const selects = [1, 3]
    for (const i of selects) {
      const radioButtons = wrapper.findAll('input[type="radio"]')
      await radioButtons[i].setChecked()
      const button = wrapper.find('button')
      button.trigger('click')
      await flushPromises()
    }
    const checkbox = wrapper.find('input[type="checkbox"]')
    await checkbox.setChecked()
    const button = wrapper.find('button')
    expect(button.element.disabled).toBe(false)

    button.trigger('click')
    expect(wrapper.emitted().submitQuiz[0][0]).toEqual(
      [
        { question_id: 0, response_ids: [ selects[0] ] },
        { question_id: 1, response_ids: [ selects[1] ] }
      ]
    )
  })

  it('should push window history state when submitting question', async () => {
    const pushStateMock = vi.spyOn(global.history, 'pushState').mockImplementation(() => {})
    const radioButtons = wrapper.findAll('input[type="radio"]')
    await radioButtons[0].setChecked()
    
    const button = wrapper.find('button')
    button.trigger('click')
    await flushPromises()
    expect(pushStateMock).toBeCalledWith({ page: 1 }, '', '')
  })

  it('should push window history state when going back to previous question', async () => {
    const pushStateMock = vi.spyOn(global.history, 'pushState').mockImplementation(() => {})
    const radioButtons = wrapper.findAll('input[type="radio"]')
    await radioButtons[0].setChecked()
    
    const button = wrapper.find('button')
    button.trigger('click')
    await flushPromises()
    const buttons = wrapper.findAll('button')
    buttons[1].trigger('click')
    await flushPromises()

    expect(pushStateMock).toBeCalledTimes(2)
    // back to first page
    expect(pushStateMock).toHaveBeenNthCalledWith(2,{ page: 0 }, '', '')
  })

  it('should not push window history state when going back from first question', async () => {
    const pushStateMock = vi.spyOn(global.history, 'pushState').mockImplementation(() => {})
    const radioButtons = wrapper.findAll('input[type="radio"]')
    await radioButtons[0].setChecked()
    
    const button = wrapper.find('button')
    button.trigger('click')
    await flushPromises()
    const buttons = wrapper.findAll('button')
    buttons[1].trigger('click')
    buttons[1].trigger('click')
    await flushPromises()

    expect(pushStateMock).toBeCalledTimes(2)
  })

  it('should add window listeners on mount', async () => {
    expect(addEventListenerMock).toBeCalled(2)
    expect(addEventListenerMock).toHaveBeenNthCalledWith(1, 'beforeunload', expect.any(Function))
    expect(addEventListenerMock).toHaveBeenNthCalledWith(2, 'popstate', expect.any(Function))
  })

  it('should remove window listeners on mount', async () => {
    wrapper.unmount()
    expect(removeEventListenerMock).toBeCalled(2)
    expect(removeEventListenerMock).toHaveBeenNthCalledWith(1, 'popstate', expect.any(Function))
    expect(removeEventListenerMock).toHaveBeenNthCalledWith(2, 'beforeunload', expect.any(Function))
  })
})
