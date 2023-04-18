import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { defineComponent } from 'vue'
import { mount, flushPromises } from '@vue/test-utils'
import ValidatedSelect from '../ValidatedSelect.vue'


const agency_api = [
  {
    "name": "Central Intelligence Agency",
    "id": 13
  },
  {
    "name": "General Services Administration",
    "id": 22
  }
]
/* 
 * This component makes an async call to get agencies from the API
 * which requires special handling in tests see:
 * https://test-utils.vuejs.org/guide/advanced/async-suspense.html#testing-asynchronous-setup
 */
function makeAsyncComponent() {
  return defineComponent({
    components: { ValidatedSelect },
    props: {isInvalid: Boolean},
    template: `
      <Suspense>
        <ValidatedSelect 
          modelValue="SomeModel"
          :isInvalid="isInvalid"
          name="agency"
          label="Agency / organization (*Required)"
          errorMessage="Please enter your agency"
         />
      </Suspense>`
  })
}

let fetchMock
describe('ValidatedInput', () => {
  beforeEach(async () => {
    fetchMock = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({
        ok: true, status:200, 
        json: () => Promise.resolve(agency_api)
      })
    })
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders properly', async () => {
    const wrapper = mount(makeAsyncComponent(), {props: {isInvalid: false}})

    await flushPromises()
    expect(wrapper.text()).toContain('Agency')
  })

  it('does not render error when valid', async () => {
    const wrapper = mount(makeAsyncComponent(),  {props: {isInvalid: false}})
    await flushPromises()

    const element = wrapper.find('[id="agency-input-error-message"]')
    expect(element.exists()).toBe(false)
  })

  it('does render error when invalid', async () => {
    const wrapper = mount(makeAsyncComponent(), {props: {isInvalid: true}})
    await flushPromises()

    const element = wrapper.find('[id="agency-input-error-message"]')
    expect(element.exists()).toBe(true)
    expect(element.text()).toBe('Please enter your agency')
  })

  it('label should be "for" input', async () => {
    const wrapper = mount(makeAsyncComponent(), {props: {isInvalid: true}})
    await flushPromises()

    const label = wrapper.find('label')
    const input = wrapper.find('select')

    expect(label.attributes('for')).toBe(input.attributes('name'))
  })

  it('get choices from the api', async () => {
    const wrapper = mount(makeAsyncComponent(), {props: {isInvalid: true}})
    await flushPromises()

    const options = wrapper.findAll('option')

    expect(options.length).toBe(3)  
    expect(options[1].text()).toBe('Central Intelligence Agency')
    expect(options[1].element.value).toBe('13')
    expect(options[2].text()).toBe('General Services Administration')
    expect(options[2].element.value).toBe('22')

    expect(fetchMock).toBeCalled()
  })

  it('displays error with invalid data', async () => {
    const wrapper = mount(makeAsyncComponent(), {props: {isInvalid: true}})
    await flushPromises()

    const error_span = wrapper.find('span[class="usa-error-message"]')
    expect(error_span.text()).toBe('Please enter your agency')
  })

  it('emits value on input', async () => {
    const wrapper = mount(makeAsyncComponent(), {props: {isInvalid: false}})
    await flushPromises()

    const select = wrapper.find('select')
    const component = wrapper.findComponent(ValidatedSelect)
    await select.setValue('22')
    await select.trigger('input')
    await flushPromises()

    expect(component.emitted()).toMatchObject({'update:modelValue': [ [ '22' ] ]})
  })
})
