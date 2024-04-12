import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import GspcRegistration from '../GspcRegistration.vue'


import { cleanStores } from 'nanostores'
import { profile } from '../../stores/user.js'

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
    expect(wrapper.text()).toContain("GSPC Registration")
    expect(wrapper.text()).toContain("Enter your email address to login. You'll receive an email with an access link.")
  })

  it('shows start registration form once user is known', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false, status:404, json: () => Promise.resolve([]) })
    })
    profile.set({name:"John Smith", jwt:"some-token-value"})
    const wrapper = await mount(GspcRegistration)
    await flushPromises()
    expect(wrapper.text()).toContain("GSPC Placeholder")
  })
})