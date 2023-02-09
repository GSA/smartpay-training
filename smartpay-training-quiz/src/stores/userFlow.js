import { ref, reactive } from 'vue'
import { defineStore } from 'pinia'

export const  userFlowStore = defineStore('userStore', () => {
    const base_url = import.meta.env.VITE_API_BASE_URL

    const jwt = ref('')
    const loading = ref(false)
    const user = reactive({
        first_name: '',
        last_name: '',
        email: '',
        agency: '',
    })

    function getUserFromToken(token) { 
        const url = `${base_url}/api/v1/get-user/${token}`  
        fetch(url)
        .then(res => {
            if (res.ok) {
                return res.json()
            }
            return Promise.reject(res)
        })
        .then(json => {
            user.first_name =  json.user.first_name
            user.last_name =  json.user.last_name
            user.email =  json.user.email
            user.agency =  json.user.agency
            jwt.value = json.jwt
        })
        .catch((err) => {
            loading.value = false
        })
  }

  return { jwt, getUserFromToken, user }
})
