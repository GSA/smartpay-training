import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount } from '@vue/test-utils'
import ExitMenu from '../ExitMenu.vue'
import {profile } from '../../stores/user.js'

describe('ExitMenu', () => {
  const originalLocation = global.location

  afterEach(() => {
    vi.restoreAllMocks()
    global.location = originalLocation
  })

  it('exit menu item is not displayed when user does not have an active session', async () => {
    const wrapper = await mount(ExitMenu)
    const exit_button = wrapper.find('[data-test="exit-button"]') 
    expect(exit_button.exists()).toBe(false)
  })

  it('displays exit button when user has active session', async () => {
    profile.set({'name': 'Buck Mulligan', 'jwt':"some-jwt"})
    const wrapper = await mount(ExitMenu)
    const exit_button = wrapper.find('[data-test=exit-button]') 
    expect(exit_button.exists()).toBe(true)
  })

  it('changes the window location to /exit', async () => {
    // location.replace is not mockable in jsdom.
    const setMock = vi.fn();
    delete global.location
    global.location = { replace: setMock }

    profile.set({'name': 'Buck Mulligan', 'jwt':"some-jwt"})
    const wrapper = await mount(ExitMenu)
    const exit_button = wrapper.find('[data-test=exit-button]') 
    await exit_button.trigger('click')

    expect(setMock).toHaveBeenCalledWith(import.meta.env.BASE_URL+'exit')
  })
})

