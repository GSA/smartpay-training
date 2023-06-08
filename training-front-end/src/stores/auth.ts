import { persistentAtom } from "@nanostores/persistent"
import { action } from "nanostores"

// When the user is directed to login, this store remembers the page they were
// on before redirecting them to UAA. When they return from UAA, the
// AuthRedirect component uses this to return them to the original page.
export const $redirectTarget = persistentAtom<string>("authRedirectTarget", "")

export const setRedirectTarget = action($redirectTarget, "setRedirectTarget", (store, target) => {
  store.set(target)
})
