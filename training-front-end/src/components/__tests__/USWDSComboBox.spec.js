import { describe, it, expect } from "vitest";
import { mount } from '@vue/test-utils';
import USWDSComboBox from "../form-components/USWDSComboBox.vue";

describe('USWDSComboBox', () => {
    it('renders properly when required', () => {
        const wrapper = mount(USWDSComboBox, {
            props: {
                modelValue: '',
                validator: {
                    $error: false,
                    $errors: []
                },
                name: 'testAgency',
                label: 'Test Agency',
                items: [
                    { id: 1, name: 'Option 1' },
                    { id: 2, name: 'Option 2' },
                    { id: 3, name: 'Option 3' }
                ],
                required: true
            }
        })

        expect(wrapper.find('.usa-form-group').exists()).toBe(true)
        expect(wrapper.find('.usa-label').text()).toBe('Test Agency (*Required)')
        expect(wrapper.findAll('option').length).toBe(3)
    })

    it('renders properly when optional', () => {
        const wrapper = mount(USWDSComboBox, {
            props: {
                modelValue: '',
                validator: {
                    $error: false,
                    $errors: []
                },
                name: 'testAgency',
                label: 'Test Agency',
                items: [
                    { id: 1, name: 'Option 1' },
                    { id: 2, name: 'Option 2' },
                    { id: 3, name: 'Option 3' }
                ],
                required: false
            }
        })

        expect(wrapper.find('.usa-form-group').exists()).toBe(true)
        expect(wrapper.find('.usa-label').text()).toBe('Test Agency (optional)')
        expect(wrapper.findAll('option').length).toBe(3)
    })

    it('displays errors when validator has errors', async () => {
        const wrapper = mount(USWDSComboBox, {
            props: {
                modelValue: '',
                validator: {
                    $error: true,
                    $errors: [{ $property: 'agency', $message: 'Agency is required' }]
                },
                name: 'testAgency',
                label: 'Test Agency',
                items: [
                    { id: 1, name: 'Option 1' },
                    { id: 2, name: 'Option 2' },
                    { id: 3, name: 'Option 3' }
                ]
            }
        })

        expect(wrapper.find('.usa-form-group--error').exists()).toBe(true)
        expect(wrapper.find('.usa-error-message').text()).toBe('Agency is required')
    })

    it('emits update:modelValue event on select', async () => {
        const wrapper = mount(USWDSComboBox, {
            props: {
                modelValue: '',
                validator: {
                    $error: false,
                    $errors: []
                },
                name: 'testAgency',
                label: 'Test Agency',
                items: [
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