import { mount } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import ValidatedDateRangePicker from '../form-components/ValidatedDateRangePicker.vue'
import FormLabel from '../form-components/FormLabel.vue'

describe('ValidatedDateRangePicker.vue', () => {
  let wrapper;

  const mockValidator = {
    startDate: 'Invalid start date',
    endDate: 'Invalid end date',
  }

  beforeEach(() => {
    // Reset mock calls and implementations before each test
    vi.resetAllMocks()
    wrapper = mount(ValidatedDateRangePicker, {
      global: {
        components: { FormLabel }
      },
      props: {
        label: 'Event Date',
        name: 'event-date',
        validator: mockValidator,
        modelValue: []
      }
    })
  })

  it('renders with the correct label and hint text', () => {
    expect(wrapper.find('label[for="event-date-start"]').text()).toBe('Event Date start (optional)')
    expect(wrapper.find('label[for="event-date-end"]').text()).toBe('Event Date end (optional)')
    expect(wrapper.find('#event-date-start-hint').text()).toBe('mm/dd/yyyy')
    expect(wrapper.find('#event-date-end-hint').text()).toBe('mm/dd/yyyy')
  })

  it('emits update:modelValueStart on start date input', async () => {
    const startInput = wrapper.find('input[name="event-date-start"]')
    await startInput.setValue('2024-01-31')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0][0]).toEqual(["2024-01-31", ""])
  })

  it('emits update:modelValueEnd on end date input', async () => {
    const endInput = wrapper.find('input[name="event-date-end"]')
    await endInput.setValue('2024-01-31')

    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')?.[0][0]).toEqual(['', '2024-01-31'])
  })
})
