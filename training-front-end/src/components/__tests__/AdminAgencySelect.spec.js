import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount } from '@vue/test-utils'
import AdminAgencySelectVue from '../AdminAgencySelect.vue'

const parent =   {
  "name": "Incandenza Enterprises",
  "id": 10
}

const agencies = [
  {
    "name": "Office of Unspecified Services",
    "id": 60
  },
  {
    "name": "Enfield Tennis Academy",
    "id": 20
  }
]

const selected = [
  {
    "name": "Enfield Tennis Academy",
    "bureau": "Office of the Administrator",
    "id": 20
  }
]

describe('AdminAgencySelect', async () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })
  it('displays items', async () => {
    const props = {items: agencies, values: selected, parent: parent}
    const wrapper = mount(AdminAgencySelectVue, {props})
    const options = wrapper.findAll('input[type="checkbox"]')
    expect(options.length).toBe(2)
  })
  it('displays names of items', async () => {
    const props = {items: agencies, values: selected, parent: parent}
    const wrapper = mount(AdminAgencySelectVue, {props})
    const label1 = wrapper.find('label[for="60"]')
    const label2 = wrapper.find('label[for="20"]')

    expect(label1.text()).toBe('Office of Unspecified Services')
    expect(label2.text()).toBe('Enfield Tennis Academy')
  })

  it('checks items that match selected values', async () => {
    const props = {items: agencies, values: selected, parent: parent}
    const wrapper = mount(AdminAgencySelectVue, {props})
    const selectedCheckBox = wrapper.find('input[id="20"]')
    const unSelectedCheckBox = wrapper.find('input[id="60"]')
    
    expect(selectedCheckBox.element.checked).toBe(true)
    expect(unSelectedCheckBox.element.checked).toBe(false)
  })

  it('displays parent when no items are present', async () => {
    const props = {values: selected, parent: parent}
    const wrapper = mount(AdminAgencySelectVue, {props})
    const parentLabel = wrapper.find('label[for="10"]')
    expect(parentLabel.text()).toBe('Incandenza Enterprises')
    const options = wrapper.findAll('input[type="checkbox"]')
    expect(options.length).toBe(1)
  })

  it('filters results based on input', async () => {
    const props = {items: agencies, values: selected, parent: parent}
    const wrapper = mount(AdminAgencySelectVue, {props})
    const filterInput = wrapper.find("input[type='text']")
    await filterInput.setValue('Unspec')
    const label1 = wrapper.find('label[for="60"]')
    const label2 = wrapper.find('label[for="20"]')

    expect(label1.exists()).toBe(true)
    expect(label2.exists()).toBe(false)
  })

  it('it only filters on the begining of words', async () => {
    const props = {items: agencies, values: selected, parent: parent}
    const wrapper = mount(AdminAgencySelectVue, {props})
    const filterInput = wrapper.find("input[type='text']")
    await filterInput.setValue('spec')

    const label1 = wrapper.find('label[for="60"]')
    const label2 = wrapper.find('label[for="20"]')

    expect(label1.exists()).toBe(false)
    expect(label2.exists()).toBe(false)
  })

  it('emits checked value when item is selected', async () => {
    const props = {items: agencies, values: selected, parent: parent}
    const wrapper = mount(AdminAgencySelectVue, {props})
    const selectedCheckBox = wrapper.find('input[id="60"]')
    await selectedCheckBox.setChecked()
    expect(wrapper.emitted()['checkItem'][0][0]).toEqual(agencies[0])
    expect(wrapper.emitted()['checkItem'][0][1]).toEqual(true)
  })

  it('emits checked value when item is unselected', async () => {
    const props = {items: agencies, values: selected, parent: parent}
    const wrapper = mount(AdminAgencySelectVue, {props})
    const selectedCheckBox = wrapper.find('input[id="20"]')
    await selectedCheckBox.setChecked(false)
    expect(wrapper.emitted()['checkItem'][0][0]).toEqual(agencies[1])
    expect(wrapper.emitted()['checkItem'][0][1]).toEqual(false)
  })

  it('emits parent value when parent item is selected', async () => {
    const props = {values: selected, parent: parent}
    const wrapper = mount(AdminAgencySelectVue, {props})
    const selectedCheckBox = wrapper.find('input[id="10"]')
    await selectedCheckBox.setChecked()
    expect(wrapper.emitted()['checkItem'][0][0]).toEqual(parent)
    expect(wrapper.emitted()['checkItem'][0][1]).toEqual(true)
  })
})