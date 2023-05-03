import { describe, it, expect, afterEach, vi} from 'vitest'
import { mount } from '@vue/test-utils'

import { cleanStores } from 'nanostores'
import EndSession from '../EndSession.vue'
import { profile } from '../../stores/user.js'

describe('EndSession', () => {
  const originalLocation = global.location

  afterEach(() => {
    vi.restoreAllMocks()
    global.location = originalLocation
    cleanStores(profile)
  })


  it('clears the user session on mount', async () => {
    profile.set({name: "Buck Mulligan", jwt: "rando-stuff"})
    await mount(EndSession)
    expect(profile.get()).toEqual({})
  })

  it('redirects to main page', async () => {
    // location.replace is not mockable in jsdom.
    const setMock = vi.fn();
    delete global.location
    global.location = { replace: setMock }

    await mount(EndSession)    
    expect(setMock).toHaveBeenCalledWith(import.meta.env.BASE_URL)
  })
})

