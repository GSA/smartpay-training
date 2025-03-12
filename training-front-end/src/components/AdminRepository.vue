<script>
  import { profile} from '../stores/user'
  import { useStore } from '@nanostores/vue'
  import {ref} from "vue";

const user = useStore(profile)

const base_url = import.meta.env.PUBLIC_API_BASE_URL
const users_api = `${base_url}/api/v1/users/`
const gspc_api = `${base_url}/api/v1/gspc/`

const userSearch = async function(searchText, currentPage){
    const url = new URL(`${users_api}`)
    url.search = new URLSearchParams({searchText: searchText, page_number: currentPage + 1})

    const response = await fetch(
      url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${user.value.jwt}`
        }
      }
    )
    if (! response.ok) {
      const message = await response.text()
      throw new Error(message)
    }
    return await response.json()
  }

  const updateUserReports = async function(userId, agencyIds) {
    const agencies = agencyIds.map(a => a.id)
    const url = new URL(`${users_api}edit-user-for-reporting/`)
    url.search = new URLSearchParams({user_id: userId})

    const response = await fetch(
      url, { 
        method: "PATCH", 
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.value.jwt}` 
        },
        body:  JSON.stringify(agencies) 
      }
    )
    if (!response.ok) {
      const message = await response.text()
      throw new Error(message)
    }
    return await response.json()
  }

    
  const getUser = async function(userId){
    const url = new URL(`${users_api}${userId}`)

    const response = await fetch(
      url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${user.value.jwt}`
        }
      }
    )
    if (! response.ok) {
      const message = await response.text()
      throw new Error(message)
    }
    return await response.json()
  }

  const updateUser = async function(userId, userData){
    const apiURL = new URL(`${users_api}${userId}`)
    let response = ref();
    try {
      response.value = await fetch(apiURL, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.value.jwt}`
        },
        body: JSON.stringify(userData)
      })
    } catch {
        throw new Error('Sorry, we had an error connecting to the server.')
      }
    
    if (!response.value.ok) {
      if (response.value.status === 400) {
        throw new Error('You are not authorized to edit profile.')
      }
      if (response.value.status === 403) {
        throw new Error("You can not update your own profile.")
      }
      throw new Error("Error contacting server.")
    }
    return await response.value.json()
  }

  const downloadGspcReport = async function(){
    const response = await fetch(`${gspc_api}download-gspc-completion-report`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${user.value.jwt}` },
      });

    if (!response.ok) {
        const message = await response.text()
        throw new Error(message)
      }

    return await response // needs to be returned as raw not json
  }

  const sendGspcInvites = async function(emailAddresses, certificationExpirationDate){
    const apiURL = new URL(`${gspc_api}send-invites`)
    let response = await fetch(apiURL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json','Authorization': `Bearer ${user.value.jwt}` },
        body: JSON.stringify({
          email_addresses: emailAddresses,
          certification_expiration_date: certificationExpirationDate
        })
      });

    if (!response.ok) {
      if (response.status == 401) {
        throw new Error("Unauthorized")
      }
      throw new Error("Error contacting server")
    }

    return await response.json()
  }

  const sendGspcFollowUps = async function(emailAddresses, certificationExpirationDate){
    const apiURL = new URL(`${gspc_api}send-follow-ups`)
    let response = await fetch(apiURL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json','Authorization': `Bearer ${user.value.jwt}` },
      });

    if (!response.ok) {
      if (response.status == 401) {
        throw new Error("Unauthorized")
      }
      throw new Error("Error contacting server")
    }

    return
  }

  const downloadTrainingReport = async function(filterData){
    const response = await fetch(`${base_url}/api/v1/users/download-admin-smartpay-training-report`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${user.value.jwt}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(filterData)
      });
    if (!response.ok) {
        const message = await response.text()
        throw new Error(message)
      }

    return await response //needs to be returned as raw not json
  }



export default {
  userSearch,
  updateUserReports,
  getUser,
  updateUser,
  downloadGspcReport,
  downloadTrainingReport,
  sendGspcInvites,
  sendGspcFollowUps
}

</script>