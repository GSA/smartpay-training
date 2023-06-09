import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { cleanStores } from 'nanostores'
import { profile } from '../../stores/user.js'

import TrainingReportIndex from '../TrainingReportIndex.vue'
import * as agencyList from '../../stores/helpers/getAgencies.js'

vi.spyOn(agencyList, 'fetchAgencyList').mockImplementation(() => Promise.resolve([]))

describe("TrainingReportIndex", async () => {
  afterEach(() => {
    vi.restoreAllMocks()
    cleanStores()
    profile.set({})
  })
  it('displays text and email input with unknown user', async () => {
    const wrapper = await mount(TrainingReportIndex)
    expect(wrapper.text()).toContain('Confirm your email to gain report access')
  })

  it('Shows download screen', async () => {
    profile.set({name:"Amelia Sedley", jwt:"some-token-value", roles:[{'name': "Report"}]})
    const wrapper = await mount(TrainingReportIndex)
    expect(wrapper.text()).toContain('Download Your Report')
  })

  it('shows error when user is know but does not have correct roles', async () => {
    profile.set({name:"Amelia Sedley", jwt:"some-token-value", roles:[{'name': "SomeOtherRole"}]})
    const wrapper = await mount(TrainingReportIndex)
    expect(wrapper.text()).toContain('You are not authorized')
  })

  it('shows error when api reports a 401', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false, status:401 })
    })
    const wrapper = await mount(TrainingReportIndex)
    await wrapper.get('[name="email"]').setValue("test@example.com")
    const form = wrapper.get('form')
    await form.trigger('submit.prevent')
    await flushPromises()
    expect(wrapper.text()).toContain('You are not authorized')
  })
})