import { describe, it, expect, afterEach, beforeEach, vi} from 'vitest'

import { cleanStores, keepMount } from 'nanostores'
import { profile, getUserFromToken, getUserFromTokenExchange} from '../user'
import AuthService from '../../services/auth'

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
  beforeEach(() => {
    vi.spyOn(AuthService.prototype, 'logout').mockImplementation(() => {})
  })
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

  it('sets token from token exchange', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(fetchData) })
    })
    keepMount(profile)
    await getUserFromTokenExchange(base_url, param_token)
    expect(profile.get()).toEqual({ 
      name: 'Gaspara Stampa', 
      id: 123, 
      jwt: "test-token-123"
    })
  })

  it('calls the api to perform token exchange', async () => {
    const fetch_spy = vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: true, status:200, json: () => Promise.resolve(fetchData) })
    })
    keepMount(profile)
    await getUserFromTokenExchange(base_url, param_token)
    expect(fetch_spy).toHaveBeenCalledWith(
      `${base_url}/api/v1/auth/exchange`, 
      {
        headers: {
          Authorization: 'Bearer 123-abc-xzy'
        },
        method: "POST"
      }
    )
  })
  
  it('throws an error when there is a server error on token exchange', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.reject('Whoops, server error')
    })
    await expect(getUserFromTokenExchange(base_url, param_token)).rejects.toThrow('We were unable to log you in (exchange error).');
  })

  it('throws an error when the server returns 403 on token exchange', async () => {
    vi.spyOn(global, 'fetch').mockImplementation(() => {
      return Promise.resolve({ok: false, status:403, json: () => Promise.resolve("Unauthorized") })
    })
    await expect(getUserFromTokenExchange(base_url, param_token)).rejects.toThrow('Your account is not authorized to access this feature.');
  })
})