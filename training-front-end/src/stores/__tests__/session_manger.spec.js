import { describe, it, expect, beforeEach, afterEach, vi} from 'vitest'

import { cleanStores, keepMount } from 'nanostores'
import { willTimeOut, continueSession } from '../session_manager'
import { profile, hasActiveSession, setUser } from '../user'

const SESSION_TIME_OUT = import.meta.env.PUBLIC_SESSION_TIME_OUT * 60 * 1000
const SESSION_WARNING_TIME = import.meta.env.PUBLIC_SESSION_WARNING_TIME * 60 * 1000

const user = {
  id: 123,
  name: "Isabel Archer",
  jwt: "test-token-123"
}

describe('Manage Session', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.restoreAllMocks()
    vi.useRealTimers()
    cleanStores(willTimeOut)
    cleanStores(profile)
    cleanStores(hasActiveSession)
  })

  it('sets willTimeOut to false initially', async () => {
    profile.set(user)
    expect(willTimeOut.get()).toBe(false)
  })

  it('sets warning flag after given time', async () => {
    keepMount(willTimeOut)
    profile.set(user)
    vi.advanceTimersByTime(SESSION_TIME_OUT - SESSION_WARNING_TIME - 10)
    expect(willTimeOut.get()).toBe(false)

    vi.advanceTimersByTime(10)
    expect(willTimeOut.get()).toBe(true)
  })

  it('calling continueSession extends the time', async () => {
    keepMount(willTimeOut)
    vi.advanceTimersByTime(SESSION_TIME_OUT - SESSION_WARNING_TIME)
    continueSession()
    expect(willTimeOut.get()).toBe(false)

    vi.advanceTimersByTime(SESSION_TIME_OUT - SESSION_WARNING_TIME)
    expect(willTimeOut.get()).toBe(true)
  })

  it('window events extent the time', async () => {
    keepMount(willTimeOut)
    vi.advanceTimersByTime(SESSION_TIME_OUT - SESSION_WARNING_TIME - 1)
    window.dispatchEvent(new Event('scroll'))

    expect(willTimeOut.get()).toBe(false)
    vi.advanceTimersByTime(SESSION_TIME_OUT - SESSION_WARNING_TIME)
    expect(willTimeOut.get()).toBe(true)
  })

  it('window events do not extent the time once warning is set', async () => {
    keepMount(willTimeOut)
    vi.advanceTimersByTime(SESSION_TIME_OUT - SESSION_WARNING_TIME)
    window.dispatchEvent(new Event('scroll'))
    expect(willTimeOut.get()).toBe(true)
  })

  it('clears the user after the session_time_out completes', async () => {
    profile.set(user)
    keepMount(willTimeOut)
    vi.advanceTimersByTime(SESSION_TIME_OUT)
    expect(profile.get()).toEqual({})
  })

  it('does not clear the user before the session_time_out completes', async () => {
    profile.set(user)
    keepMount(willTimeOut)
    vi.advanceTimersByTime(SESSION_TIME_OUT-1)
    expect(profile.get()).toEqual(user)
  })
})
