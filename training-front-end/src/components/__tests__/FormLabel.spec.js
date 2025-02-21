import { describe, it, expect } from "vitest";
import { mount } from '@vue/test-utils';
import FormLabel from '../form-components/FormLabel.vue';

describe('FormLabel', () => {
  it('renders properly', () => {
    const wrapper = mount(FormLabel, {
      props: {
        for: '',
        id: '',
        required: true,
        value: 'Test Label',
      }
    })

    expect(wrapper.find('.usa-label').text()).toBe('Test Label (*Required)')
  })

  it('shows as optional when not required', () => {
    const wrapper = mount(FormLabel, {
      props: {
        for: '',
        id: 'test-label',
        required: false,
        value: 'Test Label',
      }
    })

    expect(wrapper.find('.usa-label').text()).toBe('Test Label (optional)')
  })

  it('sets id field', () => {
    const wrapper = mount(FormLabel, {
      props: {
        for: '',
        id: 'test-label',
        required: false,
        value: 'Test Label',
      }
    })

    expect(wrapper.find('#test-label').text())
  })

  it('sets for field', () => {
    const wrapper = mount(FormLabel, {
      props: {
        for: 'test-input',
        id: 'test-label',
        required: false,
        value: 'Test Label',
      }
    })

    const label = wrapper.find('.usa-label');
  
    // Check that the 'for' attribute is set correctly
    expect(label.attributes('for')).toBe('test-input');
  })
})