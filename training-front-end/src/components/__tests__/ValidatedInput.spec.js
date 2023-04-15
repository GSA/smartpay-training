import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import ValidatedInput from '../ValidatedInput.vue'


const valid_input = { 
  'modelValue': "Ringo",
  'isInvalid': false,
  'name': 'first_name',
  'label': 'First name',
  'error_message': 'Please enter your first name'
}

const invalid_input = {...valid_input, 'isInvalid': true}


describe('ValidatedInput', () => {
  it('renders properly', () => {
    const wrapper = mount(ValidatedInput, { 
      props: valid_input
    })
    expect(wrapper.text()).toContain('First name')
  })

  it('does not render error when valid', () => {
    const wrapper = mount(ValidatedInput, { 
      props: valid_input
  })
    const element = wrapper.find('[id="first_name-input-error-message"]')
    expect(element.exists()).toBe(false)
  })

  it('does render error when invalid', () => {
    const wrapper = mount(ValidatedInput, { 
      props: invalid_input
    })
    const element = wrapper.find('[id="first_name-input-error-message"]')
    expect(element.exists()).toBe(true)
    expect(element.text()).toBe('Please enter your first name')
  })

  it('label should be "for" input', () => {
    const wrapper = mount(ValidatedInput, { 
      props: valid_input
    })
    const label = wrapper.find('label')
    const input = wrapper.find('input')

    expect(label.attributes('for')).toBe(input.attributes('name'))
  })
})
