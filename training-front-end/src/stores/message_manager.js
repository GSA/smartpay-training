import { action } from 'nanostores'
import { persistentAtom } from '@nanostores/persistent'

export const message = persistentAtom('message', undefined,
{
  encode: JSON.stringify,
  decode: JSON.parse
})

export const setMessage = action(message, 'setMessage', (store, text) => store.set(text))
export const clearMessage = action(message, 'clearMessage', store => store.set(undefined))