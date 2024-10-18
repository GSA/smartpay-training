import { describe, it, expect } from "vitest";
import { mount } from '@vue/test-utils';
import FormLegend from '../form-components/FormLegend.vue';

describe('FormLegend', () => {
  it('renders properly', () => {
    const wrapper = mount(FormLegend, {
      props: {
        required: true,
        value: 'Test Legend',
      }
    })

    expect(wrapper.find('.usa-legend').text()).toBe('Test Legend (*Required)')
  })

  it('shows as optional when not required', () => {
    const wrapper = mount(FormLegend, {
      props: {
        required: false,
        value: 'Test Legend',
      }
    })

    expect(wrapper.find('.usa-legend').text()).toBe('Test Legend (optional)')
  })
})