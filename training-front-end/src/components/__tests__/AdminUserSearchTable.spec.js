import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import AdminUserSearchTableVue from '../AdminUserSearchTable.vue'
import DocumentIconVue from '../icons/DocumentIcon.vue'


const USERS = [
  {
    "email": "helen.steeply@ous.gov",
    "name": "Hugh Steeply",
    "id": 1,
    "agency_id": 27,
    "agency": {
      "name": "Office of Unspecified Services",
      "bureau": null,
      "id": 27
    },
    "roles": [
      {
        "name": "Report",
        "id": 2
      }
    ],
    "report_agencies": [
      {
        "name": "Office of Unspecified Services",
        "bureau": null,
        "id": 27
      }
    ]
  },
  {
    "email": "remy@afr.gov",
    "name": "Rémy Marathe",
    "id": 2,
    "agency_id": 60,
    "agency": {
      "name": "Office of Unspecified Services",
      "bureau": "Les Assassins des Fauteuils Rollents",
      "id": 60
    },
    "roles": [],
    "report_agencies": []
  }
]


describe('AdminUserSearchTable', async () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })
  it('displays a header with categories', async () => {
    const props = {searchResults: USERS, numberOfResults: 2}
    const wrapper = await mount(AdminUserSearchTableVue, {props})
    const header_row = wrapper.find('tr')
    const headers = header_row.text().split(/\s+/)
    expect(headers).toEqual(['Name', 'Email', 'Agency', 'Bureau', 'Access'])
  })

  it('displays a header row for each user', async () => {
    const props = {searchResults: USERS, numberOfResults: 2}
    const wrapper = await mount(AdminUserSearchTableVue, {props})
    expect(wrapper.findAll('tr').length).toBe(3)
  })

  it('displays report access and when the user has report agencies', async () => {
    const props = {searchResults: USERS, numberOfResults: 2}
    const wrapper = await mount(AdminUserSearchTableVue, {props})
    const rows = wrapper.findAll('tr')
    const first_user_columns = rows[1].findAll('td')
    expect(first_user_columns[4].text()).toBe('Reporting')
  })

  it('displays icon and when the user has report agencies', async () => {
    const props = {searchResults: USERS, numberOfResults: 2}
    const wrapper = await mount(AdminUserSearchTableVue, {props})
    const rows = wrapper.findAll('tr')
    const first_user_columns = rows[1].findAll('td')
    const document_icon = first_user_columns[4].findComponent(DocumentIconVue)
    expect(document_icon.exists())
  })

  it('does not displays report access and when the user has no report agencies', async () => {
    const props = {searchResults: USERS, numberOfResults: 2}
    const wrapper = await mount(AdminUserSearchTableVue, {props})
    const rows = wrapper.findAll('tr')
    const second_user_columns = rows[2].findAll('td')
    expect(second_user_columns[4].text()).toBeFalsy()
  })

  it('displays does not display an icon and when the user has report agencies', async () => {
    const props = {searchResults: USERS, numberOfResults: 2}
    const wrapper = await mount(AdminUserSearchTableVue, {props})
    const rows = wrapper.findAll('tr')
    const second_user_columns = rows[2].findAll('td')
    const document_icon = second_user_columns[4].findComponent(DocumentIconVue)
    expect(document_icon.exists()).toBe(false)
  })

  it('emits selected user when name is clicked', async () => {
    const props = {searchResults: USERS, numberOfResults: 2}
    const wrapper = await mount(AdminUserSearchTableVue, {props})
    const rows = wrapper.findAll('tr')
    const second_user_columns = rows[2].findAll('td')
    const user_button = second_user_columns[0].find('button')
    await user_button.trigger('click')
    expect(wrapper.emitted()['selectItem'][0][0]).toEqual(USERS[1])
  })

  it('displays the number of results', async () => {
    const props = {searchResults: USERS, numberOfResults: 2}
    const wrapper = await mount(AdminUserSearchTableVue, {props})
    expect(wrapper.get('caption').text()).toBe('2 Results')
  })

  it('does not pluralize a single result', async () => {
    const props = {searchResults: [USERS[0]], numberOfResults: 1}
    const wrapper = await mount(AdminUserSearchTableVue, {props})
    expect(wrapper.get('caption').text()).toBe('1 Result')
  })
})