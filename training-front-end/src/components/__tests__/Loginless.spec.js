import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount, shallowMount, flushPromises } from '@vue/test-utils'
import { cleanStores, keepMount } from 'nanostores'
import Loginless from '../Loginless.vue'
import { profile } from '../../stores/user.js'

function submitEmail(wrapper, email) {
  wrapper.get('[data-test="email-submit-form"] [name="email"]').setValue(email)
  wrapper.get('form').trigger('submit.prevent')
}

const fetchData = {
  token: "http://www.example.com/?test-token"
}


describe('Loginless', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    cleanStores(profile)
  })

  it('renders initial view but not response view', async () => {
    const wrapper = await shallowMount(Loginless, { 
      props: {"page_id": "training"}
    })
    expect(wrapper.text()).toContain('Enter your email address to get access to the quiz')
    const initial_div = wrapper.find('[data-test="pre-submit"]') 
    const confirmation_div = wrapper.find('[data-test="post-submit"]')
    expect(initial_div.exists()).toBe(true)
    expect(confirmation_div.exists()).toBe(false)
  })

  it('initially only asks for an email', async () => {
    const wrapper = await shallowMount(Loginless, { 
      props: {"page_id": "training"}
    })
    const email_only_form = wrapper.find('[data-test="email-submit-form"]') 
    const complete_form = wrapper.find('[data-test="name-submit-form"]')
    expect(email_only_form.exists()).toBe(true)
    expect(complete_form.exists()).toBe(false)
  })

  it('asks for more info after unknown email is submitted', async () => {
    const wrapper = await mount(Loginless, { 
      props: {"page_id": "training"}
    })
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(fetchData) })
    })
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    const email_only_form = wrapper.find('[data-test="email-submit-form"]') 
    const complete_form = wrapper.find('[data-test="name-submit-form"]')
    expect(email_only_form.exists()).toBe(false)
    expect(complete_form.exists()).toBe(true)
  })

  it('After succesfully submitting form, it shows confirmation', async () => {
    const wrapper = await mount(Loginless, { 
      props: {"page_id": "training"}
    })
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:201, json: () => Promise.resolve(fetchData) })
    })
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    const initial_div = wrapper.find('[data-test="pre-submit"]') 
    const confirmation_div = wrapper.find('[data-test="post-submit"]')
    expect(initial_div.exists()).toBe(false)
    expect(confirmation_div.exists()).toBe(true)
  })

  it('It confirms the user email on the confirmation page', async () => {
    const wrapper = await mount(Loginless, { 
      props: {"page_id": "training"}
    })
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:201, json: () => Promise.resolve(fetchData) })
    })
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    const confirmation_div = wrapper.find('[data-test="post-submit"]')
    expect(confirmation_div.text()).toContain('test@example.com')
  })

  it('It uses the token in the url to confirm the user and show child component', async () => {
    vi.spyOn(URLSearchParams.prototype, 'get').mockImplementation(() => '7348244d-76c7-4535-94f7-5929e039af97')

    const wrapper = await mount(Loginless, { 
      props: {"page_id": "training"}
    })
    const token_response = {
      user: {},
      jwt: 'abcd'
    }
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, json: () => Promise.resolve(token_response) })
    })
    await flushPromises()
    
    const initial_div = wrapper.find('[data-test="pre-submit"]') 
    const confirmation_div = wrapper.find('[data-test="post-submit"]')
    const content_div = wrapper.find('[data-test="child-component"]')

    expect(initial_div.exists()).toBe(false)
    expect(confirmation_div.exists()).toBe(false)
    expect(content_div.exists()).toBe(true)
  })

  it('It gets the user from api using token and sets in store', async () => {
    vi.spyOn(URLSearchParams.prototype, 'get').mockImplementation(key => '7348244d-76c7-4535-94f7-5929e039af97')
    keepMount(profile)

    const token_response = {
      user: {name: "Molly Bloom"},
      jwt: 'abcd'
    }
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, json: () => Promise.resolve(token_response) })
    })
    const wrapper = await mount(Loginless, { 
      props: {"page_id": "training"}
    }) 
    await flushPromises()
    expect(profile.get()).toEqual({jwt: "abcd", name: 'Molly Bloom' })
  })

  it("It emits error when api can't find the token", async () => {
    vi.spyOn(URLSearchParams.prototype, 'get').mockImplementation(() => '7348244d-76c7-4535-94f7-5929e039af97')
    
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false })
    })
    const wrapper = await mount(Loginless, { 
      props: {"page_id": "training"}
    }) 
    await flushPromises()
    expect(wrapper.emitted().error[0][0].name).toBe('Invalid Link')
  })

  it("It should show the form when the link is invalid", async () => {
    vi.spyOn(URLSearchParams.prototype, 'get').mockImplementation(() => '7348244d-76c7-4535-94f7-5929e039af97')

    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false })
    })
    const wrapper = await mount(Loginless, { 
      props: {"page_id": "training"}
    }) 
    await flushPromises()
    const initial_div = wrapper.find('[data-test="pre-submit"]') 
    const confirmation_div = wrapper.find('[data-test="post-submit"]')
    const content_div = wrapper.find('[data-test="child-component"]')

    expect(initial_div.exists()).toBe(true)
    expect(confirmation_div.exists()).toBe(false)
    expect(content_div.exists()).toBe(false)
  })
})