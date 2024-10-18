import { describe, it, expect } from "vitest";
import { mount } from '@vue/test-utils';
import ValidatedSelect from '../form-components/ValidatedSelect.vue';

describe('ValidatedSelect', () => {
  it('renders properly', () => {
    const wrapper = mount(ValidatedSelect, {
      props: {
        modelValue: '',
        validator: {
          $error: false,
          $errors: []
        },
        name: 'testName',
        label: 'Test Label',
        options: [
          { id: 1, name: 'Option 1' },
          { id: 2, name: 'Option 2' },
          { id: 3, name: 'Option 3' }
        ],
        required: true
      }
    })

    expect(wrapper.find('.usa-form-group').exists()).toBe(true)
    expect(wrapper.find('.usa-label').text()).toBe('Test Label (*Required)')
    expect(wrapper.findAll('option').length).toBe(4) // 3 options + default option
  })

  it('displays errors when validator has errors', async () => {
    const wrapper = mount(ValidatedSelect, {
      props: {
        modelValue: '',
        validator: {
          $error: true,
          $errors: [{ $property: 'name', $message: 'Name is required' }]
        },
        name: 'testName',
        label: 'Test Label',
        options: [
          { id: 1, name: 'Option 1' },
          { id: 2, name: 'Option 2' },
          { id: 3, name: 'Option 3' }
        ]
      }
    })

    expect(wrapper.find('.usa-form-group--error').exists()).toBe(true)
    expect(wrapper.find('.usa-error-message').text()).toBe('Name is required')
  })

  it('emits update:modelValue event on input', async () => {
    const wrapper = mount(ValidatedSelect, {
      props: {
        modelValue: '',
        validator: {
          $error: false,
          $errors: []
        },
        name: 'testName',
        label: 'Test Label',
        options: [
          { id: 1, name: 'Option 1' },
          { id: 2, name: 'Option 2' },
          { id: 3, name: 'Option 3' }
        ]
      }
    })

    const select = wrapper.find('select')
    await select.setValue('1')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['1'])
  })
})