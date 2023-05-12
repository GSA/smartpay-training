import { describe, it, expect, beforeEach, afterEach, vi} from 'vitest'
import { mount } from '@vue/test-utils'
import ExitMenu from '../ExitMenu.vue'
import SessionManager from '../SessionManager.vue'
import { willTimeOut } from '../../stores/session_manager.js'
import { profile, hasActiveSession } from '../../stores/user.js'
import { cleanStores } from 'nanostores'

describe('SessionManager', () => {
  const originalLocation = global.location
  beforeEach(() => {
    // create teleport target
    const el = document.createElement('div')
    el.id = 'header_main_menu'
    document.body.appendChild(el)
    vi.useFakeTimers()
  })
  
  afterEach(() => {
    vi.restoreAllMocks()
    vi.useRealTimers()
    global.location = originalLocation
    document.body.outerHTML = ''
    cleanStores(profile)
    cleanStores(hasActiveSession)
    cleanStores(willTimeOut)
  })

  it('exit menu item is not displayed when user does not have an active session', async () => {
    const wrapper = await mount(SessionManager)
    const exit_button = wrapper.findComponent(ExitMenu) 
    expect(exit_button.exists()).toBe(false)
  })

  it('displays exit button when user has active session', async () => {
    profile.set({'name': 'Buck Mulligan', 'jwt':"some-jwt"})
    const wrapper = await mount(SessionManager)
    const exit_button = wrapper.findComponent(ExitMenu) 
    expect(exit_button.exists()).toBe(true)
  })

  it('changes the window location to /exit', async () => {
    // location.replace is not mockable in jsdom.
    const setMock = vi.fn();
    delete global.location
    global.location = { replace: setMock }

    profile.set({'name': 'Buck Mulligan', 'jwt':"some-jwt"})

    const wrapper = await mount(SessionManager)
    const exit_menu = await wrapper.findComponent(ExitMenu)  

    const exit_button = exit_menu.find('[data-test=exit-button]')
    await exit_button.trigger('click')

    expect(setMock).toHaveBeenCalledWith(import.meta.env.BASE_URL+'exit')
  })
})

