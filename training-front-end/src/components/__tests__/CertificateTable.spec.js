import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import CertificateTable from '../CertificateTable.vue'

const API_RESPONSE = [
  {
    "id": 2,
    "user_id": 1,
    "user_name": "Becky Sharp",
    "quiz_id": 5,
    "quiz_name": "Travel Training for Card/Account Holders and Approving Officials",
    "completion_date": "2023-04-17T15:02:02.814004"
  },
  {
    "id": 68,
    "user_id": 1,
    "user_name": "Becky Sharp",
    "quiz_id": 8,
    "quiz_name": "Travel Training for Agency/Organization Program Coordinators",
    "completion_date": "2023-04-25T18:03:45.134752"
  }
]


describe('CertificateTable', async () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('shows training names in table', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(API_RESPONSE) })
    })
    const wrapper = await mount(CertificateTable)
    await flushPromises()
    const rows = wrapper.findAll('tr') 
    expect(rows.length).toBe(3)

    const rowOne = rows[1].findAll('td')
    expect(rowOne[0].text()).toBe('Travel Training for Card/Account Holders and Approving Officials')

    const rowTwo = rows[2].findAll('td')
    expect(rowTwo[0].text()).toBe('Travel Training for Agency/Organization Program Coordinators')
  })

  it('displays formatted dates', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(API_RESPONSE) })
    })
    const wrapper = await mount(CertificateTable)
    await flushPromises()
    const rows = wrapper.findAll('tr') 
    expect(rows.length).toBe(3)

    const rowOne = rows[1].findAll('td')
    expect(rowOne[1].text()).toBe('April 17, 2023')

    const rowTwo = rows[2].findAll('td')
    expect(rowTwo[1].text()).toBe('April 25, 2023')
  })

  it('has links to certificate', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(API_RESPONSE) })
    })
    const wrapper = await mount(CertificateTable)
    await flushPromises()
    const rows = wrapper.findAll('tr') 
    expect(rows.length).toBe(3)

    const anchorOne = rows[1].find('form')
    expect(anchorOne.attributes('action')).toBe("http://localhost:8000/api/v1/certificate/2")

    const anchorTwo = rows[2].find('form')
    expect(anchorTwo.attributes('action')).toBe("http://localhost:8000/api/v1/certificate/68")
  })

  it('show correct message when the user has not taken a quiz', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve([]) })
    })
    const wrapper = await mount(CertificateTable)
    await flushPromises()

    const table = wrapper.find('table') 
    expect(table.exists()).toBe(false)

    expect(wrapper.text()).toContain('You have not earned any certificates yet. Take a training to earn a certificate.')
  })
})