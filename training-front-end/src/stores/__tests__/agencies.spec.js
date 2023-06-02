import { describe, it, expect, afterEach, vi} from 'vitest'

import { cleanStores, keepMount, allTasks } from 'nanostores'
import { agencyList, setSelectedAgencyId, bureauList} from '../agencies'
import * as agencyListRequest from '../helpers/getAgencies'

const agency_api = [
  { 'id': 1, 'name': 'General Services Administration', 'bureaus': []},
  { 'id': 2, 
    'name': 'Department of the Treasury', 
    'bureaus': [
      {'id': 3, 'name': 'United States Mint'},
      {'id': 4, 'name': 'Financial Crimes Enforcement'}
    ]
  },
  { 'id': 5, 'name': 'Department of the Interior', 'bureaus': []}
]

describe('Agency Store', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    cleanStores(agencyList)
  })
  it('sets agencies on mount', async () => {
    vi.spyOn(agencyListRequest, 'fetchAgencyList').mockImplementation(() => Promise.resolve(agency_api))
    keepMount(agencyList)
    await allTasks()
    expect(agencyList.get()).toEqual(agency_api)
  })
  it('sets bureaus list when agency has bureaus', async () => {
    vi.spyOn(agencyListRequest, 'fetchAgencyList').mockImplementation(() => Promise.resolve(agency_api))
    keepMount(agencyList)
    await allTasks()
    setSelectedAgencyId(2)
    expect(bureauList.get()).toEqual(agency_api[1].bureaus)
  })
  it('resets bureaus to an empty list when selectedAgency is undefined', async () => {
    vi.spyOn(agencyListRequest, 'fetchAgencyList').mockImplementation(() => Promise.resolve(agency_api))
    keepMount(agencyList)
    await allTasks()
    setSelectedAgencyId(2)
    expect(bureauList.get()).toEqual(agency_api[1].bureaus)
    setSelectedAgencyId(undefined)
    expect(bureauList.get()).toEqual([])
  })
})

