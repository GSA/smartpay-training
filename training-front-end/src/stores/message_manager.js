import { action } from 'nanostores'
import { persistentAtom } from '@nanostores/persistent'

/**
 * This is a simple message bus which stores a message in the brower's storage
 * to allow other pages to display it if needed. This is currently only used
 * by the GlobalMessage component on the index page to allow a message about 
 * a previously expired session to be displayed to the user.
 */

export const message = persistentAtom('message', undefined,
{
  encode: JSON.stringify,
  decode: JSON.parse
})

export const setMessage = action(message, 'setMessage', (store, text) => store.set(text))
export const clearMessage = action(message, 'clearMessage', store => store.set(undefined))