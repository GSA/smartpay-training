import { describe, it, expect } from "vitest";
import { mount } from '@vue/test-utils';
import ValidatedInput from '../ValidatedInput.vue';

describe('ValidatedInput', () => {
  it('renders properly', () => {
    const wrapper = mount(ValidatedInput, {
      props: {
        modelValue: '',
        validator: {
          $error: false,
          $errors: []
        },
        name: 'testName',
        label: 'Test Label'
      }
    })

    expect(wrapper.find('.usa-form-group').exists()).toBe(true)
    expect(wrapper.find('.usa-label').text()).toBe('Test Label (*Required)')
    expect(wrapper.find('input').exists()).toBe(true)
  })

  it('displays errors when validator has errors', async () => {
    const wrapper = mount(ValidatedInput, {
      props: {
        modelValue: '',
        validator: {
          $error: true,
          $errors: [{ $property: 'name', $message: 'Name is required' }]
        },
        name: 'testName',
        label: 'Test Label'
      }
    })

    expect(wrapper.find('.usa-input--error').exists()).toBe(true)
    expect(wrapper.find('.usa-error-message').text()).toBe('Name is required')
  })

  it('emits update:modelValue event on input', async () => {
    const wrapper = mount(ValidatedInput, {
      props: {
        modelValue: '',
        validator: {
          $error: false,
          $errors: []
        },
        name: 'testName',
        label: 'Test Label'
      }
    })

    const textarea = wrapper.find('input')
    await textarea.setValue('new value')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['new value'])
  })
})