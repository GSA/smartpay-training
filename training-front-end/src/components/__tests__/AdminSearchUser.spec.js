import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import AdminSearchUserVue from '../AdminSearchUser.vue'
import AdminEditReporting  from  '../AdminEditReporting.vue'
import USWDSPagination from "../USWDSPagination.vue";

import users from './fixtures/sample_users'
import agencies from './fixtures/sample_agency_response'

describe('AdminAgencySelect', async () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })
  it('displays a search input', async () => {
    let wrapper = await mount(AdminSearchUserVue)
    const searchInput = wrapper.find('input[id="search-field"]')
    expect(searchInput.exists()).toBe(true)
  })

  it('displays a search results', async () => {
    const fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve({'total_count': 2, 'users':users}) })
    })
    let wrapper = await mount(AdminSearchUserVue)
    const searchInput = wrapper.find('input[id="search-field"]')

    await searchInput.setValue("Joelle Van Dyne")
    await wrapper.get('form').trigger('submit.prevent')
    await flushPromises()

    expect(fetchSpy).toHaveBeenCalledOnce()

    const rows = wrapper.findAll('tr')
    expect(rows.length).toBe(3)
    expect(rows[1].text()).toContain('Hugh Steeply')
    expect(rows[2].text()).toContain('Rémy Marathe')
  })

  it('updates with API when child component emits data', async () => {
    let fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve({'total_count': 2, 'users':users}) })
    })
    let wrapper = await mount(AdminSearchUserVue)
    const searchInput = wrapper.find('input[id="search-field"]')

    await searchInput.setValue("Steeply")
    await wrapper.get('form').trigger('submit.prevent')
    await flushPromises()

    expect(fetchSpy).toHaveBeenCalledOnce()

    fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(agencies)})
    })
    const row = wrapper.findAll('tr')[1]
    const nameLink = row.find('button')
    await nameLink.trigger('click')
    const adminReporting = wrapper.findComponent(AdminEditReporting)

    const updateFetchSpy = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(users[0])})
    })
    await adminReporting.vm.$emit('save', "1", [{id: 10}])

    expect(updateFetchSpy).nthCalledWith(1, expect.any(URL), {
      body: '[10]',
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
    })
  })

  it('allows user to cancel update', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve({'total_count': 2, 'users':users}) })
    })
    let wrapper = await mount(AdminSearchUserVue)
    const searchInput = wrapper.find('input[id="search-field"]')

    await searchInput.setValue("Steeply")
    await wrapper.get('form').trigger('submit.prevent')
    await flushPromises()

    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(agencies)})
    })
    const row = wrapper.findAll('tr')[1]
    const nameLink = row.find('button')
    await nameLink.trigger('click')
    const adminReporting = wrapper.findComponent(AdminEditReporting)
  
    const cancel_button = adminReporting.find('button[id="cancel"')
    await cancel_button.trigger('click')

    expect(wrapper.findComponent(AdminEditReporting).exists()).toBe(false)
  })

  it('updates page when pagination emits', async () => {
    let fetchSpy = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve({'total_count': 26, 'users':users}) })
    })
    let wrapper = await mount(AdminSearchUserVue)
    const searchInput = wrapper.find('input[id="search-field"]')

    await searchInput.setValue("Steeply")
    await wrapper.get('form').trigger('submit.prevent')
    await flushPromises()

    const pagination = wrapper.findComponent(USWDSPagination)
    const linkElements = pagination.findAll('[data-test="page-link"]')
    linkElements[1].trigger('click')

    expect(fetchSpy).toBeCalledTimes(2)
    expect(fetchSpy.mock.lastCall[0].search).toBe('?page_number=2')
  })

  it('displays no results message', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve({'total_count': 0, 'users':[]}) })
    })
    let wrapper = await mount(AdminSearchUserVue)
    const searchInput = wrapper.find('input[id="search-field"]')

    await searchInput.setValue("Steeply")
    await wrapper.get('form').trigger('submit.prevent')
    await flushPromises()

    const adminReporting = wrapper.findComponent(AdminEditReporting)
    expect(adminReporting.exists()).toBe(false)
    expect(wrapper.text()).toContain("zero results")
  })
})
