import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import CertificateTable from '../CertificateTable.vue'

const API_RESPONSE = [
  {
    "id": 2,
    "user_id": 1,
    "user_name": "Becky Sharp",
    "cert_title": "Travel Training for Card/Account Holders and Approving Officials",
    "quiz_name": "Travel Training for Card/Account Holders and Approving Officials",
    "completion_date": "2023-04-17T15:02:02.814004",
    "certificate_type": 1
  },
  {
    "id": 68,
    "user_id": 1,
    "user_name": "Becky Sharp",
    "cert_title": "Travel Training for Agency/Organization Program Coordinators",
    "quiz_name": "Travel Training for Agency/Organization Program Coordinators",
    "completion_date": "2023-04-25T18:03:45.134752",
    "certificate_type": 1
  },
  {
    "id": 99,
    "user_id": 1,
    "user_name": "Becky Sharp",
    "cert_title": "GSPC",
    "quiz_name": "GSPC",
    "completion_date": "2023-07-25T18:03:45.134752",
    "certificate_type": 2
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
    expect(rows.length).toBe(API_RESPONSE.length + 1)

    const rowOne = rows[1].findAll('td')
    API_RESPONSE[0].cert_title
    expect(rowOne[0].text()).toBe(API_RESPONSE[0].cert_title)

    const rowTwo = rows[2].findAll('td')
    expect(rowTwo[0].text()).toBe(API_RESPONSE[1].cert_title)

    const rowThree = rows[3].findAll('td')
    expect(rowThree[0].text()).toBe(API_RESPONSE[2].cert_title)
  })

  it('displays formatted dates', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(API_RESPONSE) })
    })
    const wrapper = await mount(CertificateTable)
    await flushPromises()
    const rows = wrapper.findAll('tr') 

    const rowOne = rows[1].findAll('td')
    expect(rowOne[1].text()).toBe('April 17, 2023')

    const rowTwo = rows[2].findAll('td')
    expect(rowTwo[1].text()).toBe('April 25, 2023')
  })

  it('has links to certificate with cert type and id', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(API_RESPONSE) })
    })
    const wrapper = await mount(CertificateTable)
    await flushPromises()
    const rows = wrapper.findAll('tr') 

    const anchorOne = rows[1].find('form')
    expect(anchorOne.attributes('action')).toBe("http://localhost:8000/api/v1/certificate/1/2")

    const anchorTwo = rows[2].find('form')
    expect(anchorTwo.attributes('action')).toBe("http://localhost:8000/api/v1/certificate/1/68")

    const anchorThree = rows[3].find('form')
    expect(anchorThree.attributes('action')).toBe("http://localhost:8000/api/v1/certificate/2/99")
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