import { action } from 'nanostores'
import { persistentAtom, setPersistentEngine } from '@nanostores/persistent'

/**
 * This is a simple message bus which stores a message in the brower's storage
 * to allow other pages to display it if needed. This is currently only used
 * by the GlobalMessage component on the index page to allow a message about 
 * a previously expired session to be displayed to the user.
 * 
 * To use import and call `setMessage(message, level)`. The level should 
 * correspond to the classMap in components/USWDSAlert.vue.
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

export const message = persistentAtom('message', undefined,
{
  listen: false,
  encode: JSON.stringify,
  decode: JSON.parse
})

export const setMessage = action(message, 'setMessage', (store, text, level) => store.set([text, level]))
export const clearMessage = action(message, 'clearMessage', store => store.set(undefined))