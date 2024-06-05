import { describe, it, expect, afterEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { cleanStores } from 'nanostores'
import { profile } from '../../stores/user.js'

import AdminReportIndex from '../AdminReportIndex.vue'


describe("AdminReportIndex", async () => {
  afterEach(() => {
    vi.restoreAllMocks()
    cleanStores()
    profile.set({})
  })

  it('Shows download screen', async () => {
    profile.set({name:"Amelia Sedley", jwt:"some-token-value", roles:["Admin"]})
    const wrapper = await mount(AdminReportIndex)
    expect(wrapper.text()).toContain('Download GSPC Report')
  })

  it('shows error when user is know but does not have correct roles', async () => {
    profile.set({name:"Amelia Sedley", jwt:"some-token-value", roles:["SomeOtherRole"]})
    const wrapper = await mount(AdminReportIndex)
    expect(wrapper.text()).toContain('You are not authorized')
  })

})