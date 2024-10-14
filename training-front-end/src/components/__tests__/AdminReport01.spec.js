import { describe, it, expect, beforeEach } from 'vitest';
import { mount, flushPromises  } from '@vue/test-utils'
import { vi } from 'vitest';
import AdminReport01 from '../AdminReport01.vue';
import AdminRepository from '../AdminRepository.vue';
import { profile } from '../../stores/user';

describe('AdminReport01.vue', () => {
  let wrapper;

  beforeEach(async () => {
    // Set the profile mock with Admin role
    profile.set({ name: 'Amelia Sedley', jwt: 'some-token-value', roles: ['Admin'] });

    wrapper = await mount(AdminReport01, {
      global: {
        stubs: {
          // Stub child components that are not essential for the test
          USWDSAlert: true,
          ValidatedSelect: true,
          ValidatedDateRangePicker: true,
          ValidatedCheckboxGroup: true,
          SpinnerGraphic: true,
        },
      },
    });
  });

  it('renders the form when the user is an Admin', () => {
    expect(wrapper.html()).toContain('Lorem ipsum dolor sit amet, consectetur adipiscing elit');
    expect(wrapper.find('form').exists()).toBe(true);
  });

  it('displays an error message when the user is not authorized', async () => {
    // Change the profile to non-admin
    profile.set({ name: 'Amelia Sedley', jwt: 'some-token-value', roles: [] });

    await wrapper.vm.$nextTick();

    expect(wrapper.html()).toContain('You are not authorized to receive reports.');
    expect(wrapper.find('form').exists()).toBe(false);
  });

  it('submits the form and calls downloadReport01', async () => {
    // Mocking the report download response
    AdminRepository.downloadReport01 = vi.fn(() =>
      Promise.resolve({
        blob: () => new Blob(['mock-csv-content'], { type: 'text/csv' }),
      })
    );

    // Update reactive `user_input` properties using Vue reactivity
    wrapper.vm.user_input.agency_id = '123';
    wrapper.vm.user_input.bureau_id = '456';
    wrapper.vm.user_input.quiz_names = ['Fleet Training For Program Coordinators'];
    wrapper.vm.user_input.completion_date_range = ['2024-01-01', '2024-01-31'];

    // Simulate form submission
    await wrapper.find('form').trigger('submit.prevent');

    expect(AdminRepository.downloadReport01).toHaveBeenCalledWith({
      agency_id: '123',
      bureau_id: '456',
      quiz_names: ['Fleet Training For Program Coordinators'],
      completion_date_start: '2024-01-01',
      completion_date_end: '2024-01-31',
    });
  });

  it('handles errors during report download', async () => {
    AdminRepository.downloadReport01 = vi.fn(() => Promise.reject(new Error('Failed to download')));

    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.vm.error.message).toBe('Failed to download');
  });

  it('shows a success message after a successful report download', async () => {
    AdminRepository.downloadReport01 = vi.fn(() =>
      Promise.resolve({
        blob: () => new Blob(['mock-csv-content'], { type: 'text/csv' }),
      })
    );
  
    // Trigger the form submission
    await wrapper.find('form').trigger('submit.prevent');
  
    // Wait for all pending promises and Vue updates to complete
    await flushPromises();
  
    // Assert that the success message is shown
    expect(wrapper.vm.showSuccessMessage).toBe(true);
  });

  it('displays a spinner while the report is loading', async () => {
    const downloadPromise = new Promise(() => {}); // Mock a pending download
    AdminRepository.downloadReport01 = vi.fn(() => downloadPromise);

    await wrapper.find('form').trigger('submit.prevent');

    expect(wrapper.vm.showSpinner).toBe(true);
  });
});