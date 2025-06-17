import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import AdminSearchUserVue from '../AdminSearchUser.vue'
import AdminEditReporting  from  '../AdminEditReporting.vue'
import USWDSPagination from "../USWDSPagination.vue";
import { cleanStores } from 'nanostores'
import { profile } from '../../stores/user.js'
import users from './fixtures/sample_users'
import agencies from './fixtures/sample_agency_response'

describe('AdminAgencySelect', async () => {
  afterEach(() => {
    vi.restoreAllMocks()
    cleanStores()
    profile.set({})
  })
  
  it('displays a search input', async () => {
    profile.set({name:"Amelia Sedley", jwt:"some-token-value", roles:["Admin"]})
    let wrapper = await mount(AdminSearchUserVue)
    const searchInput = wrapper.find('input[id="search-field"]')
    expect(searchInput.exists()).toBe(true)
  })

  it('displays a search results', async () => {
    profile.set({name:"Amelia Sedley", jwt:"some-token-value", roles:["Admin"]})
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
    profile.set({name:"Ortho Stice", jwt:"some-token-value", roles:["Admin"]})
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
    await adminReporting.vm.$emit('updateReportingAccess', "1", [{id: 10}])

    expect(updateFetchSpy).nthCalledWith(1, expect.any(URL), {
      body: '[10]',
      method: 'PATCH',
      headers: {
        'Authorization': 'Bearer some-token-value',
        'Content-Type': 'application/json'
      },
    })
    //Ensure it stayed on User Profile
    expect(wrapper.text()).toContain('User Profile');
  })

  it('allows user to cancel update', async () => {
    profile.set({name:"Amelia Sedley", jwt:"some-token-value", roles:["Admin"]})
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
    profile.set({name:"Amelia Sedley", jwt:"some-token-value", roles:["Admin"]})
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
    expect(fetchSpy.mock.lastCall[0].search).toBe('?searchText=Steeply&page_number=2')
  })

  it('displays no results message', async () => {
    profile.set({name:"Amelia Sedley", jwt:"some-token-value", roles:["Admin"]})
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

  it('displays error with server message on non-2xx response', async () => {
    profile.set({name:"Amelia Sedley", jwt:"some-token-value", roles:["Admin"]})
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false, status:403, text: () => Promise.resolve('Forbidden') })
    })
    let wrapper = await mount(AdminSearchUserVue)
    const searchInput = wrapper.find('input[id="search-field"]')

    await searchInput.setValue("Steeply")
    await wrapper.get('form').trigger('submit.prevent')
    await flushPromises()
    const alert = wrapper.find('[data-test="alert-container"]')
    expect(alert.exists()).toBe(true)
    expect(alert.text()).toContain('Forbidden')
  })

  it('displays error on server error', async () => {
    profile.set({name:"Amelia Sedley", jwt:"some-token-value", roles:["Admin"]})
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.reject(new Error('T00 many m0nkey$'))
    })
    let wrapper = await mount(AdminSearchUserVue)
    const searchInput = wrapper.find('input[id="search-field"]')

    await searchInput.setValue("Steeply")
    await wrapper.get('form').trigger('submit.prevent')
    await flushPromises()
    const alert = wrapper.find('[data-test="alert-container"]')
    expect(alert.exists()).toBe(true)
    expect(alert.text()).toContain('T00 many m0nkey$')
  })

  it('displays error on server failure during update', async () => {
    profile.set({name:"Ortho Stice", jwt:"some-token-value", roles:["Admin"]})

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

    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false, status:403, text: () => Promise.resolve('Office of Unspecified Services is not a real agency')})
    })
    await adminReporting.vm.$emit('updateReportingAccess', "1", [{id: 10}])

    await flushPromises()
    const alert = await wrapper.find('[data-test="alert-container"]')
    expect(alert.text()).toContain('Office of Unspecified Services is not a real agency')
  })

})
