import { describe, it, expect, afterEach} from 'vitest'
import { mount } from '@vue/test-utils'
import { cleanStores } from 'nanostores'
import GlobalMessage from '../GlobalMessage.vue'
import USWDSAlert from '../USWDSAlert.vue'
import { message } from '../../stores/message_manager'

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
    message.set("A screaming comes across the sky.")
    const wrapper = await mount(GlobalMessage)
    const alert = wrapper.findComponent(USWDSAlert)
    expect(alert.exists()).toBe(true)
  })

  it('displays the message', async () => {
    message.set("It has happened before…")
    const wrapper = await mount(GlobalMessage)
    const alert = wrapper.findComponent(USWDSAlert)
    expect(alert.text()).toContain("It has happened before…")
  })

  it('removes the global message after displaying it', async () => {
    message.set("…but there is nothing to compare it to now")
    await mount(GlobalMessage)
    expect(message.get()).toBe(undefined)
  })
})
