import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import ValidatedTextArea from "../ValidatedTextArea.vue";

describe('ValidatedTextArea', () => {
  it('renders properly', () => {
    const wrapper = mount(ValidatedTextArea, {
      props: {
        modelValue: 'initial value',
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
    expect(wrapper.find('textarea').exists()).toBe(true)
  })

  it('displays errors when validator has errors', async () => {
    const wrapper = mount(ValidatedTextArea, {
      props: {
        modelValue: 'initial value',
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
    const wrapper = mount(ValidatedTextArea, {
      props: {
        modelValue: 'initial value',
        validator: {
          $error: false,
          $errors: []
        },
        name: 'testName',
        label: 'Test Label'
      }
    })

    const textarea = wrapper.find('textarea')
    await textarea.setValue('new value')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['new value'])
  })
})