import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import GspcRegistration from '../GspcRegistration.vue'


import { cleanStores } from 'nanostores'
import { profile } from '../../stores/user.js'

async function setUserCredentials(){
  vi.spyOn(global, 'fetch').mockImplementation(() => {
    return Promise.resolve({ok: false, status:404, json: () => Promise.resolve([]) })
  })
  profile.set({name:"John Smith", jwt:"some-token-value"})
}

describe('GspcRegistration', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    cleanStores(profile)
    profile.set({})
  })

  it('loads initial view with unknown user', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false, status:404, json: () => Promise.resolve([]) })
    })
    const wrapper = await mount(GspcRegistration)
    await flushPromises()
    expect(wrapper.text()).toContain("Verify GSPC coursework and experience")
    expect(wrapper.text()).toContain("Enter your email address")
  })

  it('shows start registration form once user is known', async () => {
    setUserCredentials()
    const wrapper = await mount(GspcRegistration)
    await flushPromises()
    expect(wrapper.text()).toContain("GSA SmartPay® Program Certification (GSPC) Requirements")
  })

  it('renders USWDSAlert when error is present', async () => {
    // Mock the error
    const error = { name: 'Mock Error', message: 'This is a mock error message' };

    // Mount the component with error prop
    const wrapper = mount(GspcRegistration, {
      props: {
        error: error
      }
    });

    // Find the USWDSAlert component
    const uswdsAlert = wrapper.findComponent({ name: 'USWDSAlert' });
    expect(uswdsAlert.exists()).toBe(true);

    // Assert the props passed to USWDSAlert
    expect(uswdsAlert.props('status')).toBe('error');
    expect(uswdsAlert.props('heading')).toBe(error.name);
    expect(wrapper.text()).toContain(error.message)
  });


  it('should submit registration successfully', async () => {
    setUserCredentials()
    const wrapper = mount(GspcRegistration, {});

    const mockedResponse = { passed: true };
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockedResponse)
    });

    await wrapper.vm.submitGspcRegistration([]);

    expect(wrapper.vm.certPassed).toBe(true);
    expect(wrapper.vm.certFailed).toBe(false);
    expect(wrapper.vm.error).toBe(null);
    expect(wrapper.text()).toContain("Congratulations")
  });

  it('should submit failed registration successfully', async () => {
    setUserCredentials()
    const wrapper = mount(GspcRegistration, {});

    const mockedResponse = { passed: false };
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockedResponse)
    });

    await wrapper.vm.submitGspcRegistration([]);

    expect(wrapper.vm.certPassed).toBe(false);
    expect(wrapper.vm.certFailed).toBe(true);
    expect(wrapper.vm.error).toBe(null);
    expect(wrapper.text()).toContain("You Don't Meet the Requirements")
  });

  it('should handle server error', async () => {
    setUserCredentials()
    const wrapper = mount(GspcRegistration, {});

    const errorMessage = 'There was a problem connecting with the server';
    global.fetch = vi.fn().mockRejectedValueOnce(new Error(errorMessage));

    await wrapper.vm.submitGspcRegistration([]);

    expect(wrapper.vm.certPassed).toBe(false);
    expect(wrapper.vm.certFailed).toBe(false);
    expect(wrapper.vm.error.message).toBe(errorMessage);
    expect(wrapper.text()).toContain(errorMessage)
  });
})