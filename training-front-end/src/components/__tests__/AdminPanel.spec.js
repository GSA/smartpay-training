import {beforeEach, describe, expect, it} from "vitest";
import {profile} from "../../stores/user.js";
import {mount} from "@vue/test-utils";
import AdminPanel from "../AdminPanel.vue";

describe('AdminPanel', async () => {
    
    it('displays admin card links', async () => {
        // Set the profile mock with Admin role
        profile.set({ name: 'Amelia Sedley', jwt: 'some-token-value', roles: ['Admin'] });

        const wrapper = await mount(AdminPanel, {
            global: {
                stubs: {
                    // Stub child components that are not essential for the test
                    USWDSAlert: true,
                },
            },
        });
        
        const userMaintenanceLink = wrapper.find('div[id="user-maintenance-card"]')
        const gspcLink = wrapper.find('div[id="gspc-card"]')
        const systemReportsLink = wrapper.find('div[id="system-reports-card"]')
        expect(userMaintenanceLink.exists()).toBe(true)
        expect(gspcLink.exists()).toBe(true)
        expect(systemReportsLink.exists()).toBe(true)
    })

    it('displays an error message when the user is not authorized', async () => {
        // Change the profile to non-admin
        profile.set({ name: 'Amelia Sedley', jwt: 'some-token-value', roles: [] });

        const wrapper = await mount(AdminPanel, {
            global: {
                stubs: {
                    // Stub child components that are not essential for the test
                    USWDSAlert: true,
                },
            },
        });

        expect(wrapper.html()).toContain('You are not authorized to access.');
    });
})