import { describe, it, expect, afterEach, beforeEach, vi} from 'vitest'
import { mount } from '@vue/test-utils'
import AdminEditReporting from '../AdminEditReporting.vue'
import AdminAgencySelect from "../AdminAgencySelect.vue";

import users from './fixtures/sample_users'

const agencies = [
  {
    "id": 20,
    "name": "Department of Education",
    "bureaus": [
      {
        "id": 132,
        "name": "Enfield Tennis Academy"
      },
    ]
  },
  {
    "id": 10,
    "name": "Ennet House",
    "bureaus": []
  }
]
describe('AdminAgencySelect', async () => {
  beforeEach(() => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(agencies) })
    })
  })
  afterEach(() => {
    vi.restoreAllMocks()
  })
  it('displays the basic user information', async () => {
    const props = {user: users[0]}
    const wrapper = mount(AdminEditReporting, {props})
    const name = wrapper.find('input[id="input-full-name"]')
    const email = wrapper.find('input[id="input-email"]')
    const agency = wrapper.find('input[id="input-agency"]')
    const bureau = wrapper.find('input[id="input-bureau"]')

    expect(name.element.value).toBe('Hugh Steeply')
    expect(email.element.value).toBe('helen.steeply@ous.gov')
    expect(bureau.element.value).toBe('Secret Service')
  })

  it('displays table with header and user reporting agencies', async () => {
    const props = {user: users[0]}
    const wrapper = mount(AdminEditReporting, {props})
    const table_rows = wrapper.findAll('tr')
    
    expect(table_rows.length).toBe(3)
    expect(table_rows[1].text()).toContain('Office of Unspecified Services')
    expect(table_rows[1].text()).toContain('Secret Service')
    expect(table_rows[2].text()).toContain('A.T.F')
  })

  it('delete [trash can] button removes agency', async () => {
    const props = {user: users[0]}
    const wrapper = mount(AdminEditReporting, {props})
    let table_rows = wrapper.findAll('tr')
    
    const delete_button_row_1 = table_rows[1].find('button')
    await delete_button_row_1.trigger('click')

    table_rows = wrapper.findAll('tr')
    expect(table_rows.length).toBe(2)
    expect(table_rows[1].text()).toContain('A.T.F')
  })

  it("emits user id and user's updated agencies on save", async () => {
    const props = {user: users[0]}
    const wrapper = mount(AdminEditReporting, {props})
    const table_rows = wrapper.findAll('tr')
    
    const delete_button_row_1 = table_rows[1].find('button')
    await delete_button_row_1.trigger('click')

    const update_button = wrapper.find('button[id="update-user"]')
    update_button.trigger('click')

    expect(wrapper.emitted()['save'][0][0]).toEqual(users[0].id)
    expect(wrapper.emitted()['save'][0][1]).toEqual([users[0].report_agencies[1]])
  })

  it("emits cancel when cancel button is clicked", async () => {
    const props = {user: users[0]}
    const wrapper = mount(AdminEditReporting, {props})
    const cancel_button = wrapper.find('button[id="cancel"]')
    await cancel_button.trigger('click')

    expect(wrapper.emitted()).toHaveProperty('cancel')
  })

  it("adds/removes agency when user marks check boxes", async () => {
    const props = {user: users[0]}
    const wrapper = mount(AdminEditReporting, {props})

    const agencySelect = wrapper.find('select')
    await agencySelect.setValue(20)
    
    const checkbox = wrapper.find('input[type="checkbox"]')

    await checkbox.setChecked()
    let table_rows = wrapper.findAll('tr')
    expect(table_rows.length).toBe(4)
    expect(table_rows[3].text()).toContain("Enfield Tennis Academy")
    
    await checkbox.setChecked(false)
    table_rows = wrapper.findAll('tr')
    expect(table_rows.length).toBe(3)
  })
  it("adds agency without bureau when user marks check boxes", async () => {
    const props = {user: users[0]}
    const wrapper = mount(AdminEditReporting, {props})

    const agencySelect = wrapper.find('select')
    await agencySelect.setValue(10)
    
    const checkbox = wrapper.find('input[type="checkbox"]')

    await checkbox.setChecked()
    let table_rows = wrapper.findAll('tr')
    expect(table_rows.length).toBe(4)
    expect(table_rows[3].text()).toContain("Ennet House")
  })
})