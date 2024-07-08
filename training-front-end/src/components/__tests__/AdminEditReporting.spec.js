import { describe, it, expect, afterEach, beforeEach, vi} from 'vitest'
import { mount } from '@vue/test-utils'
import AdminEditReporting from '../AdminEditReporting.vue'

import users from './fixtures/sample_users'
import agencies from './fixtures/sample_agency_response'

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
    const name = wrapper.find('dd[id="user-name-value"]')
    const email = wrapper.find('dd[id="user-email-value"]')
    const agency = wrapper.find('dd[id="user-agency-organization-value"]')
    const bureau = wrapper.find('dd[id="user-bureau-value"]')

    expect(name.text()).toContain('Hugh Steeply')
    expect(email.text()).toContain('helen.steeply@ous.gov')
    expect(agency.text()).toContain('Office of Unspecified Services')
    expect(bureau.text()).toContain('Secret Service')
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

  it('displays none when the user is not associated with an agency', async () => {
    const props = {user: users[0]}
    const wrapper = mount(AdminEditReporting, {props})
    let table_rows = wrapper.findAll('tr')
    
    const delete_button_row_1 = table_rows[1].find('button')
    const delete_button_row_2 = table_rows[2].find('button')

    await delete_button_row_1.trigger('click')
    await delete_button_row_2.trigger('click')


    table_rows = wrapper.findAll('tr')
    expect(table_rows.length).toBe(2)
    expect(table_rows[1].text()).toContain('None')
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
    expect(table_rows.length).toBe(7)
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
    expect(table_rows.length).toBe(7)
    expect(table_rows[3].text()).toContain("Ennet House")
  })
})