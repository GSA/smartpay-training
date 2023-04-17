import { describe, it, expect, afterEach, vi} from 'vitest'
import { defineComponent } from 'vue'
import { mount, shallowMount, flushPromises } from '@vue/test-utils'
import { cleanStores, keepMount } from 'nanostores'
import Loginless from '../Loginless.vue'
import { profile } from '../../stores/user.js'

function submitEmail(wrapper, email) {
  wrapper.get('[data-test="email-submit-form"] [name="email"]').setValue(email)
  wrapper.get('form').trigger('submit.prevent')
}

const agency_api = [
  {
    "name": "Central Intelligence Agency",
    "id": '13'
  },
  {
    "name": "General Services Administration",
    "id": '22'
  }
]

function makeAsyncComponent() {
  return defineComponent({
    components: { Loginless },
    template: `
      <Suspense>
        <Loginless 
          page_id="page-id"
          header="Some header"
         />
      </Suspense>`
  })
}

const fetchData = {
  token: "http://www.example.com/?test-token"
}

describe('Loginless', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    cleanStores(profile)
  })

  it('renders initial view, but not the response view', async () => {
    const wrapper = await shallowMount(Loginless, { 
      props: {"page_id": "training"}
    })
    expect(wrapper.text()).toContain('Enter your email address to get access to the quiz')
    const initial_div = wrapper.find('[data-test="pre-submit"]') 
    const confirmation_div = wrapper.find('[data-test="post-submit"]')
    expect(initial_div.exists()).toBe(true)
    expect(confirmation_div.exists()).toBe(false)
  })

  it('initially only asks for an email address', async () => {
    const wrapper = await shallowMount(Loginless, { 
      props: {"page_id": "training"}
    })
    const email_only_form = wrapper.find('[data-test="email-submit-form"]') 
    const complete_form = wrapper.find('[data-test="name-submit-form"]')
    expect(email_only_form.exists()).toBe(true)
    expect(complete_form.exists()).toBe(false)
  })

  it('asks for more information after an unknown email is submitted', async () => {
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

  it("does not call the api if the form is invalid", async () => {
    const wrapper = await mount(Loginless, { 
      props: {"page_id": "training"}
    })
    const fetchMock = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(fetchData) })
    })
    await submitEmail(wrapper, 'bademail@') 
    await flushPromises()

    expect(fetchMock).not.toBeCalled()
  })

  it('after succesfully submitting the form, it shows confirmation', async () => {
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

  it('throws error on non-2xx reponse code', async () => {
    /* this error should be handled by parent component */
    const error_handler =  vi.fn()
    const wrapper = await mount(Loginless, { 
      props: {"page_id": "training"},
      global: {
        config: {
          errorHandler: error_handler
        }
      }
    })
    
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false, status:404, json: () => Promise.resolve(fetchData) })
    })
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    expect(error_handler).toBeCalledTimes(1)
  })


  it('confirms the user email on the confirmation page', async () => {
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

  it('uses the token in the url to confirm the user and show the child component', async () => {
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

  it('gets the user from the api using the token from the url and sets it in the store', async () => {
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

  it('resets history on a successful mount', async () => {
    vi.spyOn(URLSearchParams.prototype, 'get').mockImplementation(key => '7348244d-76c7-4535-94f7-5929e039af97')

    const token_response = {
      user: {name: "Molly Bloom"},
      jwt: 'abcd'
    }
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, json: () => Promise.resolve(token_response) })
    })
    const historymock = vi.spyOn(global.history, 'replaceState').mockImplementation(() => {})
    const wrapper = await mount(Loginless, { 
      props: {"page_id": "training"}
    }) 
    await flushPromises()
    expect(historymock).toBeCalledWith({}, '', expect.any(URL))
  })

  it("emits error when api can't find the token", async () => {
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

  it("shows the form when the link is invalid", async () => {
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

  it('submits form to api with complete information', async () => {
    const fetchspy = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(agency_api) })
    })
    // first fill out the email only form...
    const wrapper = await mount(makeAsyncComponent())
    await flushPromises()
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    // ...then the second form
    const second_form = wrapper.get('form')
    await wrapper.get('[name="email"]').setValue("test@example.com")
    await wrapper.get('[name="name"]').setValue("Molly")
    
    const select = second_form.find('select')
    await select.setValue('22')
    select.trigger('input')
    second_form.trigger('submit.prevent')
    await flushPromises()

    expect(fetchspy).toBeCalledTimes(3)
    expect(fetchspy).nthCalledWith(3, expect.any(URL), {
      body: '{"user":{"name":"Molly","email":"test@example.com","agency_id":"22"},"dest":{"page_id":"page-id"}}',
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
    })
  })
})