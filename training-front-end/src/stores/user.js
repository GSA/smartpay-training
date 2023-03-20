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
  } catch(e) {
    console.log("error connecting to api", e)
    throw e
  }
  if (!res.ok) {
    clearUser()
    throw "invalid token"
  }

  let {user, jwt} = await res.json()
  store.set({...user, jwt: jwt})
})
 

export const getUserFromJWT = action(profile, 'validateUser', async (store, base_url, jwt) => {
  const url = `${base_url}/api/v1/validate-jwt/${token}` 
  let res 
  try {
    res = fetch(url, { 
      method: "POST", 
      headers: { 'Content-Type': 'application/json'},
      body:  jwt
    })
  } catch(e) {
    // server error?
    console.log("error connecting to api", e)
    throw e
  }
  if (!res.ok) {
    clearUser()
    throw "invalid token"
  }
  let user = await res.json()
  store.set({...user, jwt:jwt})
})