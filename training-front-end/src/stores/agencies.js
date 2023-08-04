import { atom, onMount, action, task, computed} from 'nanostores'
import { fetchAgencyList } from './helpers/getAgencies'

export const agencyList = atom([])
export const selectedAgencyId = atom(undefined)

onMount(agencyList,  () => {
  task(async () => {
    const options = await fetchAgencyList()
    agencyList.set(options)
  })
})

export const setSelectedAgencyId = action(selectedAgencyId, 'set', (store, id) => {
  store.set(id)
  return store.get()
})

export const bureauList = computed(
  selectedAgencyId, 
  id => !id
    ? [] 
    : agencyList.get().find(agency => agency.id == id ).bureaus 
  )
