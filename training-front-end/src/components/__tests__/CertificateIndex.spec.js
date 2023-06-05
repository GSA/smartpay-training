import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import CertificateIndex from '../CertificateIndex.vue'
import CertificateTable from '../CertificateTable.vue'

import { cleanStores } from 'nanostores'
import { profile } from '../../stores/user.js'
import * as agencyList from '../../stores/helpers/getAgencies.js'


const API_RESPONSE = [
  {
    "id": 2,
    "user_id": 1,
    "user_name": "Becky Sharp",
    "quiz_id": 5,
    "quiz_name": "Travel Training for Card/Account Holders and Approving Officials",
    "completion_date": "2023-04-17T15:02:02.814004"
  },
]

vi.spyOn(agencyList, 'fetchAgencyList').mockImplementation(() => Promise.resolve([]))

describe('CertificateIndex', async () => {
  afterEach(() => {
    vi.restoreAllMocks()
    cleanStores()
    profile.set({})
  })

  it('shows email input when user is unknown', async () => {
    const wrapper = await mount(CertificateIndex)
    expect(wrapper.text()).toContain('Enter your email address to get access to your previously earned certificates')
  })

  it('welcomes user when they are known', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(API_RESPONSE) })
    })
    profile.set({name:"Amelia Sedley", jwt:"some-token-value"})
    const wrapper = await mount(CertificateIndex)
    expect(wrapper.text()).toContain('Welcome Amelia Sedley!')
  })

  it('shows certificate table when user is known', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(API_RESPONSE) })
    })
    profile.set({name:"Amelia Sedley", jwt:"some-token-value"})
    const wrapper = await mount(CertificateIndex)
    const table = wrapper.findComponent(CertificateTable)
    expect(table.exists()).toBe(true)
  })

  it('displays an error message on a server error', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.reject(new Error("Whoops! Server Error"))
    })
    const wrapper = await mount(CertificateIndex)
    await wrapper.get('[name="email"]').setValue("test@example.com")
    const form = wrapper.get('form')
    await form.trigger('submit.prevent')
    await flushPromises()

    const alert = wrapper.find("[data-test='alert-container']")
    expect(alert.exists()).toBe(true)
    expect(alert.text()).toContain('Server Error')
  })
})