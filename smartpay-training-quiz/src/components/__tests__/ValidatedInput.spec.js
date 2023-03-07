import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import ValidatedInput from '../loginless/ValidatedInput.vue'


describe('ValidatedInput', () => {
    it('renders properly', () => {
      const wrapper = mount(ValidatedInput, { 
        props: { 
          'modelValue': "Ringo",
          'isInvalid': false,
          'name': 'first_name',
          'label': 'First name',
          'error_message': 'Please enter your first name'
        }
      })
      expect(wrapper.text()).toContain('First name')
    })
})

describe('ValidatedInput', () => {
  it('does not render error when valid', () => {
    const wrapper = mount(ValidatedInput, { 
      props: { 
        'modelValue': "Ringo",
        'isInvalid': false,
        'name': 'first_name',
        'label': 'First name',
        'error_message': 'Please enter your first name'
      }
    })
    const element = wrapper.find('[id="first_name-input-error-message"]')
    expect(element.exists()).toBe(false)
  })
})

describe('ValidatedInput', () => {
  it('does render error when invalid', () => {
    const wrapper = mount(ValidatedInput, { 
      props: { 
        'modelValue': "Ringo",
        'isInvalid': true,
        'name': 'first_name',
        'label': 'First name',
        'error_message': 'Please enter your first name'
      }
    })
    const element = wrapper.find('[id="first_name-input-error-message"]')
    expect(element.exists()).toBe(true)
    expect(element.text()).toBe('Please enter your first name')
  })
})
 
