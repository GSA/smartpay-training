<script setup>
  import { onBeforeMount, onMounted, ref } from 'vue'
  import AuthService from '../services/auth'

  const auth = new AuthService()
  const users = ref([])
  let token = ""

  const base_url = import.meta.env.PUBLIC_API_BASE_URL

  function loadUsers() {
    const url = `${base_url}/api/v1/users`

    fetch(url, {
      method: "GET",
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
    }).then((res) => {
      res.json().then((data) => {
        users.value = data
      })
    }).catch((err) => {
      console.log("ERROR", err)
    })
  }

  onBeforeMount(() => {
    auth.getAccessToken().then((data) => {
      token = data
      loadUsers()
    })
  })

</script>

<template>
  <table class="usa-table">
    <thead>
      <th>Name</th>
      <th>Email</th>
      <th>Agency</th>
    </thead>
    <tbody>
      <tr v-for="user in users">
        <td>{{ user.name }}</td>
        <td>{{ user.email }}</td>
        <td>{{ user.agency_id }}</td>
      </tr>
    </tbody>
  </table>
</template>
