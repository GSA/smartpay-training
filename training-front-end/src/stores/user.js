import { persistentAtom } from '@nanostores/persistent'
import { action } from 'nanostores'

export const profile = persistentAtom('user', {},
{
  encode: JSON.stringify,
  decode: JSON.parse
})

export const clearUser = action(profile, 'clearUser', store => store.set({}))

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
 