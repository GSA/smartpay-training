// When the user is directed to login, this store remembers the page they were
// on before redirecting them to UAA. When they return from UAA, the
// AuthRedirect component uses this to return them to the original page.

import { persistentAtom, setPersistentEngine } from "@nanostores/persistent"
import { action } from "nanostores"

/*
 * Change default to use sessionStorage instead of localStorage,
 * which will cause the session to be cleared when the tab closers
 */
let listeners: any[] = []

const events = {
  addEventListener(_: any, callback: any) {
    listeners.push(callback)
  },
  removeEventListener(_: any, callback: any) {
    listeners = listeners.filter(i => i != callback)
  },
  perKey: false
}
setPersistentEngine(window.sessionStorage, events)

export const redirectTarget = persistentAtom<string | undefined>("authRedirectTarget", "")

export const setRedirectTarget = action(redirectTarget, "setRedirectTarget", (store, target) => {
  store.set(target)
})

export const clearRedirectTarget = action(redirectTarget, "clearRedirectTarget", (store) => {
  store.set(undefined)
})
