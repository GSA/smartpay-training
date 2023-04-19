import { describe, it, expect, afterEach, vi} from 'vitest'

import { cleanStores, keepMount } from 'nanostores'
import { profile, getUserFromToken} from '../user'

const fetchData = {
  user: {
    id: 123,
    name: "Gaspara Stampa"
  },
  jwt: "test-token-123"
}

const base_url = "http://www.example.com"
const param_token = "123-abc-xzy"

describe('getUserFromToken', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    cleanStores(profile)
  })

  it('it calls the API with the token', async () => {
    const fetch_spy = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:201, json: () => Promise.resolve(fetchData) })
    })
    keepMount(profile)
    await getUserFromToken(base_url, param_token)
    expect(fetch_spy).toHaveBeenCalled(`${base_url}/api/v1/get-user/${param_token}` )
  })

  it('it sets the user in the store based on api value', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:201, json: () => Promise.resolve(fetchData) })
    })
    keepMount(profile)
    await getUserFromToken(base_url, param_token)
    expect(profile.get()).toEqual({ 
      name: 'Gaspara Stampa', 
      id: 123, 
      jwt: "test-token-123"
    })
  })

  it('throws an error when the api does not return a 2xx value', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false, status:404})
    })
    await expect(getUserFromToken(base_url, param_token)).rejects.toThrowError('This link is either expired');
  })
  
  it('throws an error when there is a server error', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.reject('Whoops, server error')
    })
    await expect(getUserFromToken(base_url, param_token)).rejects.toThrow('Sorry, we had an error connecting to the server');
  })
})