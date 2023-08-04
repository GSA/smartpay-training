import { describe, it, expect, afterEach, vi} from 'vitest'
import { defineComponent } from 'vue'
import { mount, shallowMount, flushPromises } from '@vue/test-utils'
import { cleanStores, keepMount, allTasks } from 'nanostores'
import Loginless from '../LoginlessFlow.vue'
import { profile } from '../../stores/user.js'

import * as agencyList from '../../stores/helpers/getAgencies'

function submitEmail(wrapper, email) {
  wrapper.get('[data-test="email-submit-form"] [name="email"]').setValue(email)
  wrapper.get('form').trigger('submit.prevent')
}

const props = {"pageId": "training", "header":"Some header", "title":"Training Title", 'linkDestinationText': "the training quiz"}
const slots = {
  'initial-greeting': "Enter your email address to get access to the quiz"
}
const agency_api = [
  { 'id': 1, 'name': 'General Services Administration', 'bureaus': []},
  { 'id': 2, 
    'name': 'Department of the Treasury', 
    'bureaus': [
      {'id': 3, 'name': 'United States Mint'},
      {'id': 4, 'name': 'Financial Crimes Enforcement'}
    ]
  },
  { 'id': 5, 'name': 'Department of the Interior', 'bureaus': []}
]

function makeAsyncComponent() {
  return defineComponent({
    components: { Loginless },
    template: `
        <Loginless 
          pageId="page-id"
          header="Some header"
          title="Training Title"
          link-destination-text="the training quiz"
         />`
  })
}

const fetchData = {
  token: "http://www.example.com/?test-token"
}

vi.spyOn(agencyList, 'fetchAgencyList').mockImplementation(() => Promise.resolve(agency_api))

describe('Loginless', () => {

  afterEach(() => {
    vi.restoreAllMocks()
    cleanStores(profile)
    profile.set({})
  })

  it('renders initial view, but not the response view', async () => {
    const wrapper = await shallowMount(Loginless, {props, slots})
    expect(wrapper.text()).toContain('Enter your email address to get access to the quiz')
    const initial_div = wrapper.find('[data-test="pre-submit"]') 
    const confirmation_div = wrapper.find('[data-test="post-submit"]')
    expect(initial_div.exists()).toBe(true)
    expect(confirmation_div.exists()).toBe(false)
  })
 
  it('initially only asks for an email address', async () => {
    const wrapper = await shallowMount(Loginless, {props})
    const email_only_form = wrapper.find('[data-test="email-submit-form"]') 
    const complete_form = wrapper.find('[data-test="name-submit-form"]')
    expect(email_only_form.exists()).toBe(true)
    expect(complete_form.exists()).toBe(false)
  })

  it('shows warning alert regarding authorized users at the start of the flow ', async () => {
    const wrapper = await mount(Loginless, {props})
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(fetchData) })
    })
    let alert = wrapper.find('[data-test="alert-container"]')
    expect(alert.exists()).toBe(true)
    expect(alert.text()).toContain('FOR OFFICIAL USE ONLY')
    
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    alert = wrapper.find('[data-test="alert-container"]')
    expect(alert.exists()).toBe(false)
  })

  it('asks for more information after an unknown email is submitted', async () => {
    const wrapper = await mount(Loginless, {props})
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

  it('does not ask for more information after an unknown email is submitted when allowRegistration is false', async () => {
    const wrapper = await mount(Loginless, {props: {...props, allowRegistration:false}})
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(fetchData) })
    })
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    const email_only_form = wrapper.find('[data-test="email-submit-form"]') 
    const complete_form = wrapper.find('[data-test="name-submit-form"]')
    expect(email_only_form.exists()).toBe(true)
    expect(complete_form.exists()).toBe(false)
  })

  it("does not call the api if the form is invalid", async () => {
    const wrapper = await mount(Loginless, {props})
    const fetchMock = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(fetchData) })
    })
    await submitEmail(wrapper, 'bademail@') 
    await flushPromises()

    expect(fetchMock).not.toBeCalled()
  })

  it("shows message when email form is invalid", async () => {
    const wrapper = await mount(Loginless, {props})
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(fetchData) })
    })
    await submitEmail(wrapper, 'bademail@') 
    await flushPromises()
    const element = wrapper.find('[id="email-input-error-message"]')
    expect(element.exists()).toBe(true)
    expect(element.text()).toBe('Please enter a valid email address')
  })

  it('after succesfully submitting the form, it shows confirmation', async () => {
    const wrapper = await mount(Loginless, {props})
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

  it('throws error on non-2xx response code', async () => {
    /* this error should be handled by parent component */
    const error_handler =  vi.fn()
    const wrapper = await mount(Loginless, { 
      props,
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

  it('throws specific error on 401 response code', async () => {
    /* this error should be handled by parent component */
    const error_handler =  vi.fn()
    const wrapper = await mount(Loginless, { 
      props,
      global: {
        config: {
          errorHandler: error_handler
        }
      }
    })
    
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false, status:401, json: () => Promise.resolve(fetchData) })
    })
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    expect(error_handler).toBeCalledTimes(1)
    expect(error_handler.mock.calls[0][0]).toEqual(Error("Unauthorized"))
  })

  it('confirms the user email on the confirmation page', async () => {
    const wrapper = await mount(Loginless, {props})
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

    const wrapper = await mount(Loginless, {props})
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
    vi.spyOn(URLSearchParams.prototype, 'get').mockImplementation(() => '7348244d-76c7-4535-94f7-5929e039af97')

    keepMount(profile)

    const token_response = {
      user: {name: "Molly Bloom"},
      jwt: 'abcd'
    }

    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, json: () => Promise.resolve(token_response) })
    })
    await mount(Loginless, {props}) 
    await flushPromises()
    expect(profile.get()).toEqual({jwt: "abcd", name: 'Molly Bloom' })
  })

  it('resets history on a successful mount', async () => {
    vi.spyOn(URLSearchParams.prototype, 'get').mockImplementation(() => '7348244d-76c7-4535-94f7-5929e039af97')

    const token_response = {
      user: {name: "Molly Bloom"},
      jwt: 'abcd'
    }
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, json: () => Promise.resolve(token_response) })
    })
    const historymock = vi.spyOn(global.history, 'replaceState').mockImplementation(() => {})
    await mount(Loginless, {props}) 
    await flushPromises()
    expect(historymock).toBeCalledWith({}, '', expect.any(URL))
  })

  it("emits error when api can't find the token", async () => {
    vi.spyOn(URLSearchParams.prototype, 'get').mockImplementation(() => '7348244d-76c7-4535-94f7-5929e039af97')

    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false })
    })
    const wrapper = await mount(Loginless, {props}) 
    await flushPromises()
    expect(wrapper.emitted().error[0][0].name).toBe('Invalid Link')
  })

  it("shows the form when the link is invalid", async () => {
    vi.spyOn(URLSearchParams.prototype, 'get').mockImplementation(() => '7348244d-76c7-4535-94f7-5929e039af97')

    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false })
    })
    const wrapper = await mount(Loginless, {props}) 
    await flushPromises()
    const initial_div = wrapper.find('[data-test="pre-submit"]') 
    const confirmation_div = wrapper.find('[data-test="post-submit"]')
    const content_div = wrapper.find('[data-test="child-component"]')

    expect(initial_div.exists()).toBe(true)
    expect(confirmation_div.exists()).toBe(false)
    expect(content_div.exists()).toBe(false)
  })

  it('loads agencies in select element', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(agency_api) })
    })
    //  first fill out the email only form...
    const wrapper = await mount(makeAsyncComponent())
    await flushPromises()
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    const options = wrapper.findAll('option')

    expect(options.length).toBe(4)  
    expect(options[1].text()).toBe('General Services Administration')
    expect(options[1].element.value).toBe('1')
    expect(options[2].text()).toBe('Department of the Treasury')
    expect(options[2].element.value).toBe('2')
  })

  it('does not show bureau select when agency has none', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => Promise.resolve({ok: true, status:200 }))
    //  first fill out the email only form...
    const wrapper = await mount(makeAsyncComponent())
    await flushPromises()
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    const agency_select = await wrapper.get('[name="agency"]')
    agency_select.setValue(1)
    await agency_select.trigger('input')
    const bureau_select = wrapper.find('[name="bureau"]')
    expect(bureau_select.exists()).toBe(false)
  })

  it('loads bureaus in select element', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => Promise.resolve({ok: true, status:200 }))
    //  first fill out the email only form...
    const wrapper = await mount(makeAsyncComponent())
    await flushPromises()
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    const agency_select = await wrapper.get('[name="agency"]')
    agency_select.setValue(2)
    await agency_select.trigger('input')

    const bureau_select = await wrapper.get('[name="bureau"]')
    const options = bureau_select.findAll('option')

    expect(options.length).toBe(3)  
    expect(options[1].text()).toBe('United States Mint')
    expect(options[1].element.value).toBe('3')
    expect(options[2].text()).toBe('Financial Crimes Enforcement')
    expect(options[2].element.value).toBe('4')
  })

  it('sets uses the bureau when selected', async () => {
    const fetchspy = vi.spyOn(global, 'fetch').mockImplementation(() => Promise.resolve({ok: true, status:200 }))
    //  first fill out the email only form...
    const wrapper = await mount(makeAsyncComponent())
    await flushPromises()
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    await wrapper.get('[name="email"]').setValue("test@example.com")
    await wrapper.get('[name="name"]').setValue("Molly")

    const agency_select = await wrapper.get('[name="agency"]')
    agency_select.setValue(2)
    await agency_select.trigger('input')

    const bureau_select = await wrapper.get('[name="bureau"]')
    bureau_select.setValue(3)
    await bureau_select.trigger('input')
    const second_form = wrapper.get('form')

    await second_form.trigger('submit.prevent')
    await flushPromises()
    expect(fetchspy).nthCalledWith(2, expect.any(URL), {
      body: '{"user":{"name":"Molly","email":"test@example.com","agency_id":"3"},"dest":{"page_id":"page-id","title":"Training Title"}}',
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
    })

  })

  it('submits form to api with complete information', async () => {
    const fetchspy = vi.spyOn(global, 'fetch').mockImplementation(() => Promise.resolve({ok: true, status:200 }))
    
    // first fill out the email only form...
    const wrapper = await mount(makeAsyncComponent())
    await allTasks()
    await flushPromises()
    await submitEmail(wrapper, 'test@example.com') 
    await flushPromises()

    // ...then the second form
    const second_form = wrapper.get('form')
    await wrapper.get('[name="email"]').setValue("test@example.com")
    await wrapper.get('[name="name"]').setValue("Molly")
    
    const select = second_form.find('select')
    await select.setValue('1')
    await select.trigger('input')
    await second_form.trigger('submit.prevent')
    await flushPromises()

    expect(fetchspy).toBeCalledTimes(2)
    expect(fetchspy).nthCalledWith(2, expect.any(URL), {
      body: '{"user":{"name":"Molly","email":"test@example.com","agency_id":"1"},"dest":{"page_id":"page-id","title":"Training Title"}}',
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
    })
  })
})