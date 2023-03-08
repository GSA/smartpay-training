import { describe, it, expect, vi, afterEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'

import Loginless from '../loginless/Loginless.vue'

function submitForm(wrapper, userData) {
  wrapper.get('[name="first_name"]').setValue(userData.first_name)
  wrapper.get('[name="last_name"]').setValue(userData.last_name)
  wrapper.get('[name="email"]').setValue(userData.email)
  wrapper.get('[name="agency"]').setValue(userData.agency)
  wrapper.get('form').trigger('submit.prevent')
}

const userData = {
  first_name: 'Stephen',
  last_name: 'Dedalus',
  email: 'stephen@liffy.org',
  agency: 'GSA'
}

const fetchData = {
  token: "test-token"
}

  
describe('ValidatedInput', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders initial view but not response view', () => {
    const wrapper = mount(Loginless)
    expect(wrapper.text()).toContain('Getting access to training')
    const initial_div = wrapper.find('[data-test="pre-submit"]') 
    const result_div = wrapper.find('[data-test="post-submit"]')
    expect(initial_div.exists()).toBe(true)
    expect(result_div.exists()).toBe(false)
  })

  it('renders response view after user submits and hides original', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, json: () => Promise.resolve(fetchData) })
    })

    const wrapper = mount(Loginless)
    submitForm(wrapper, userData)
    await flushPromises()

    const initial_div = wrapper.find('[data-test="pre-submit"]') 
    const result_div = wrapper.find('[data-test="post-submit"]')
    expect(initial_div.exists()).toBe(false)
    expect(result_div.exists()).toBe(true)
  })

  it('does not fetch data with invalid form' , async () => {
    const fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, json: () => Promise.resolve(fetchData) })
    })
    const wrapper = mount(Loginless)
    const badData = {...userData, email: "abc@"}
    submitForm(wrapper, badData)
    await flushPromises()

    const result_div = wrapper.find('[data-test="post-submit"]')
    expect(result_div.exists()).toBe(false)
    expect(fetchSpy).not.toHaveBeenCalled()
  })

  it('does not change views invalid form' , async () => {
    const fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, json: () => Promise.resolve(fetchData) })
    })
    const wrapper = mount(Loginless)
    const badData = {...userData, email: "1928"}
    submitForm(wrapper, badData)
    await flushPromises()
    
    const initial_div = wrapper.find('[data-test="pre-submit"]') 
    const result_div = wrapper.find('[data-test="post-submit"]')
    expect(initial_div.exists()).toBe(true)
    expect(result_div.exists()).toBe(false)
  })

})
