import { describe, it, expect, afterEach, beforeEach, vi} from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import sample_quiz from './fixtures/sample_quiz'
import {passing_result} from './fixtures/sample_quiz_response'
import QuizIndex from '../QuizIndex.vue'
import Quiz from '../Quiz.vue'
import { cleanStores } from 'nanostores'
import { profile } from '../../stores/user.js'

const page_props = {
  header: "Fancy Pants",
  subhead: "for everyone",
  audience: "audience",
  page_id: "training_travel",
  topic: "tennis",
  title: "Eschaton Training"
}

describe('QuizIndex', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    cleanStores(profile)
  })

  it('loads initial view with unknown user', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(sample_quiz) })
    })
    const wrapper = await mount(QuizIndex, {props: page_props})
    expect(wrapper.text()).toContain("Take the GSA SmartPay Fancy Pants Quiz")
    expect(wrapper.text()).toContain("Enter your email address to get access to the quiz. You'll receive an email with an access link")
  })

  it('handles API errors', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.reject(new Error("Whoops, Server Error"))
    })
    const wrapper = await mount(QuizIndex, {props: page_props})
    await flushPromises()
    const alert = wrapper.find('[data-test="alert-container"]')
    expect(alert.text()).toContain("Server Error")
  })

  it('handles non-2xx responses from API', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false, status:404, json: () => Promise.resolve([sample_quiz]) })
    })
    const wrapper = await mount(QuizIndex, {props: page_props})
    await flushPromises()
    const alert = wrapper.find('[data-test="alert-container"]')
    expect(alert.text()).toContain("Server Error")
  })

  it('shows start quiz once user is known', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve([sample_quiz]) })
    })
    profile.set({name:"Hal Incandenza", jwt:"some-token-value"})
    const wrapper = await mount(QuizIndex, {props: page_props})
    await flushPromises()
    expect(wrapper.text()).toContain("Now that you’ve reviewed the course material, you are ready to take the quiz.")
  })

  it('starts quiz when user clicks button', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve([sample_quiz]) })
    })
    profile.set({name:"Hal Incandenza", jwt:"some-token-value"})
    const wrapper = await mount(QuizIndex, {props: page_props})
    
    await flushPromises()
    const button = wrapper.find('button')
    button.trigger('click')
    await flushPromises()

   expect(wrapper.text()).toContain(sample_quiz.content.questions[0].text)
  })

  it('it sends results to api when quiz emits submit', async () => {
    const fetchspy = vi.spyOn(global, 'fetch')
    // gets quiz
    fetchspy.mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve([sample_quiz]) })
    })
    profile.set({name:"Hal Incandenza", jwt:"some-token-value"})
    const wrapper = await mount(QuizIndex, {props: page_props})
    await flushPromises()

    const button = wrapper.find('button')
    button.trigger('click')
    await flushPromises()

    // submits quiz
    fetchspy.mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(passing_result) })
    })
    const quiz = wrapper.getComponent(Quiz)
    await quiz.vm.$emit('submitQuiz', [[0], [2]])
    await wrapper.vm.$nextTick()
    expect(fetchspy).nthCalledWith(2, 
      expect.stringMatching('api/v1/quizzes/2/submission'), 
      {
        body: '{"responses":[[0],[2]]}',
        headers: {
          'Authorization': 'Bearer some-token-value',
          'Content-Type': 'application/json',
        },
        method: 'POST'
      }
    )
  })

  it('it displays error when child component throws error', async () => {
    const fetchspy = vi.spyOn(global, 'fetch')
    // gets quiz
    fetchspy.mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve([sample_quiz]) })
    })
    profile.set({name:"Hal Incandenza", jwt:"some-token-value"})
    const wrapper = await mount(QuizIndex, {props: page_props})
    await flushPromises()

    const button = wrapper.find('button')
    button.trigger('click')
    await flushPromises()

    // get API error from  back end
    fetchspy.mockImplementation(() => {
      return Promise.reject(new Error("Whoops server error"))
    })
    const quiz = wrapper.getComponent(Quiz)
    await quiz.vm.$emit('submitQuiz', [[0], [2]])
    await wrapper.vm.$nextTick()
    await flushPromises()
    let alert = wrapper.find('[data-test="alert-container"]')
    expect(alert.text()).toContain('There was a problem connecting with the server')
  })
})