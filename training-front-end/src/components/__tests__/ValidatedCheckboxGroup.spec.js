import { mount } from '@vue/test-utils';
import ValidatedCheckboxGroup from '../form-components/ValidatedCheckboxGroup.vue';
import { describe, it, expect } from 'vitest';

describe('ValidatedCheckboxGroup.vue', () => {
  it('renders options correctly', () => {
    const wrapper = mount(ValidatedCheckboxGroup, {
      props: {
        legend: 'Test Legend',
        modelValue: [],
        options: [
          { value: 'option1', label: 'Option 1' },
          { value: 'option2', label: 'Option 2' },
        ],
        required: false,
        validator: { $error: false, $errors: [] },
      },
    });

    // Check legend text
    expect(wrapper.find('legend').text()).toBe('Test Legend (optional)');

    // Check the number of checkboxes rendered
    const checkboxes = wrapper.findAll('input[type="checkbox"]');
    expect(checkboxes.length).toBe(2);

    // Check if labels are rendered correctly
    expect(wrapper.find('label[for="option1"]').text()).toBe('Option 1');
    expect(wrapper.find('label[for="option2"]').text()).toBe('Option 2');
  });

  it('emits update when checkbox is clicked', async () => {
    const wrapper = mount(ValidatedCheckboxGroup, {
      props: {
        legend: 'Test Legend',
        modelValue: [],
        options: [
          { value: 'option1', label: 'Option 1' },
          { value: 'option2', label: 'Option 2' },
        ],
        required: false,
        validator: { $error: false, $errors: [] },
      },
    });

    const option1Checkbox = wrapper.find('input[value="option1"]');
    const option2Checkbox = wrapper.find('input[value="option2"]');

    // Check the emitted value after selecting the first checkbox
    await option1Checkbox.setChecked(true);
    expect(wrapper.emitted()['update:modelValue'][0]).toEqual([['option1']]);

    // Check the emitted value after selecting the second checkbox
    await option2Checkbox.setChecked(true);
    expect(wrapper.emitted()['update:modelValue'][1]).toEqual([['option1', 'option2']]);
    
    // Check the emitted value after unchecking the first checkbox
    await option1Checkbox.setChecked(false);
    expect(wrapper.emitted()['update:modelValue'][2]).toEqual([['option2']]);

    // Check the emitted value after unchecking all checkboxes
    await option2Checkbox.setChecked(false);
    expect(wrapper.emitted()['update:modelValue'][3]).toEqual([[]]);
  });

  it('displays validation errors', () => {
    const wrapper = mount(ValidatedCheckboxGroup, {
      props: {
        legend: 'Test Legend',
        modelValue: [],
        options: [
          { value: 'option1', label: 'Option 1' },
          { value: 'option2', label: 'Option 2' },
        ],
        required: false,
        validator: {
          $error: true,
          $errors: [{ $property: 'modelValue', $message: 'Required field' }],
        },
      },
    });

    // Check that the error message is displayed
    const errorMessage = wrapper.find('.usa-error-message');
    expect(errorMessage.exists()).toBe(true);
    expect(errorMessage.text()).toBe('Required field');
  });
});