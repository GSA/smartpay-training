import { describe, it, expect } from "vitest";
import { mount } from '@vue/test-utils';
import ValidatedDatepicker from '../ValidatedDatepicker.vue';

describe('ValidatedDatepicker', () => {
  it('renders properly', async () => {
    const wrapper = mount(ValidatedDatepicker, {
      props: {
        modelValue: '',
        validator: {
          $error: false,
          $errors: []
        },
        name: 'testName',
        label: 'Test Label'
      }
    });
    
    expect(wrapper.html()).toContain('Month');
    expect(wrapper.html()).toContain('Day');
    expect(wrapper.html()).toContain('Year');
  });

  it('displays errors when validator has errors', async () => {
    const wrapper = mount(ValidatedDatepicker, {
      props: {
        modelValue: '',
        validator: {
          $error: true,
          $errors: [{ $property: 'name', $message: 'Name is required' }]
        },
        name: 'testName',
        label: 'Test Label'
      }
    });

    expect(wrapper.find('.usa-error-message').text()).toBe('Name is required');
  });

  it('emits update:modelValue event on input', async () => {
    const wrapper = mount(ValidatedDatepicker, {
      props: {
        modelValue: '',
        validator: {
          $error: false,
          $errors: []
        },
        name: 'testName',
        label: 'Test Label'
      }
    });

    const monthInput = wrapper.get('#testName-month');
    const dayInput = wrapper.get('#testName-day');
    const yearInput = wrapper.get('#testName-year');

    await monthInput.setValue('1'); //zero index 1 = february 
    await dayInput.setValue('15');
    await yearInput.setValue('2023');

    expect(wrapper.emitted()).toHaveProperty('update:modelValue');
    expect(wrapper.emitted()['update:modelValue'][0]).toEqual([new Date('2023-02-15')]);
  });

  it('updates user_input when modelValue changes', async () => {
    const wrapper = mount(ValidatedDatepicker, {
      props: {
        modelValue: '',
        validator: {
          $error: false,
          $errors: []
        },
        name: 'testName',
        label: 'Test Label'
      }
    });

    await wrapper.vm.$nextTick();
 
    // Simulate user input
    const monthInput = wrapper.get('#testName-month');
    const dayInput = wrapper.get('#testName-day');
    const yearInput = wrapper.get('#testName-year');

    // Simulate modelValue change
    await wrapper.setProps({
      modelValue: new Date('2024-02-20')
    });

    await wrapper.vm.$nextTick();

    // Ensure user_input is updated
    expect(monthInput.element.value).toBe('1');
    expect(dayInput.element.value).toBe('20');
    expect(yearInput.element.value).toBe('2024');

    // Simulate modelValue change to undefined
    await wrapper.setProps({
      modelValue: undefined
    });

    await wrapper.vm.$nextTick();

    // Ensure user_input is cleared
    expect(monthInput.element.value).toBe('');
    expect(dayInput.element.value).toBe('');
    expect(yearInput.element.value).toBe('');
  });
});