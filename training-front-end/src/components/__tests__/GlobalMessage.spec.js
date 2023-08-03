import { describe, it, expect, afterEach} from 'vitest'
import { mount } from '@vue/test-utils'
import { cleanStores } from 'nanostores'
import GlobalMessage from '../GlobalMessage.vue'
import USWDSAlert from '../USWDSAlert.vue'
import { setMessage, message } from '../../stores/message_manager'

describe('GlobalMessage', () => {

  afterEach(() => {
    cleanStores(message)
  })

  it('is not active when there is no message', async () => {
    const wrapper = mount(GlobalMessage)
    const alert = await wrapper.findComponent(USWDSAlert)
    expect(alert.exists()).toBe(false)
  })

  it('is active when there is a message', async () => {
    setMessage("A screaming comes across the sky.", "success")
    const wrapper = await mount(GlobalMessage)
    const alert = wrapper.findComponent(USWDSAlert)
    expect(alert.exists()).toBe(true)
  })

  it('displays the message', async () => {
    setMessage("It has happened before…", "success")
    const wrapper = await mount(GlobalMessage)
    const alert = wrapper.findComponent(USWDSAlert)
    expect(alert.text()).toContain("It has happened before…")
  })

  it('removes the global message after displaying it', async () => {
    setMessage("…but there is nothing to compare it to now", "success")
    await mount(GlobalMessage)
    expect(message.get()).toBe(undefined)
  })

  it('displays the success alert level', async () => {
    setMessage("It is too late. The Evacuation still proceeds,", "success")
    const wrapper = await mount(GlobalMessage)
    const alert = wrapper.findComponent(USWDSAlert)
    expect(alert.classes()).toContain('usa-alert--success')
  })

  it('displays the success alert level', async () => {
    setMessage("but it's all theatre", "warning")
    const wrapper = await mount(GlobalMessage)
    const alert = wrapper.findComponent(USWDSAlert)
    expect(alert.classes()).toContain('usa-alert--warning')
  })
})
