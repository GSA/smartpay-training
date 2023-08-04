import { persistentAtom, setPersistentEngine } from '@nanostores/persistent'
import { action, computed } from 'nanostores'


/*
 * Change default to use sessionStorage instead of localStorage,
 * which will cause the session to be cleared when the tab closers
 */
let listeners = []

const events = {
  addEventListener(key, callback) {
    listeners.push(callback)
  },
  removeEventListener(key, callback) {
    listeners = listeners.filter(i => i != callback)
  },
  perKey: false
}
setPersistentEngine(window.sessionStorage, events)

export const profile = persistentAtom('user_test', {},
{
  encode: JSON.stringify,
  decode: JSON.parse
})

export const hasActiveSession = computed(profile, user => Boolean(user.jwt))

export const clearUser = action(profile, 'clearUser', async store => {
  store.set({})
})

export const getUserFromToken = action(profile, 'getUserFromToken', async (store, base_url, token) => {
  const url = `${base_url}/api/v1/get-user/${token}`
  let res
  try {
    res = await fetch(url)
  } catch(err) {
    // THis would indicate an API problem
    // What to tell the user here?
    const e = new Error("Sorry, we had an error connecting to the server.")
    e.name = "Server Error"
    throw e
  }
  if (!res.ok) {
    clearUser()
    const e = new Error('This link is either expired or is invalid. Links to training are only valid for 24 hours. Please request a new link with the form below.')
    e.name = "Invalid Link"
    throw e
  }

  let {user, jwt} = await res.json()
  store.set({...user, jwt: jwt})
})

export const getUserFromTokenExchange = action(profile, 'getUserFromTokenExchange', async (store, base_url, uaa_token) => {
  const url = `${base_url}/api/v1/auth/exchange`
  let res

  try {
    res = await fetch(url, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${uaa_token}`
      }
    })
  } catch(err) {
    throw new Error(
      "We were unable to log you in (exchange error).",
      { name: "Server Error" }
    )
  }

  if (res.status === 403) {
    throw new Error(
      "Your account is not authorized to access this feature.",
      { name: "Unauthorized" }
    )
  }

  const { user, jwt } = await res.json()
  store.set({ ...user, jwt })
})
