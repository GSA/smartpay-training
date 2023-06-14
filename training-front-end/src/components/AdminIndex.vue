<script setup>
  import { onBeforeMount, ref } from 'vue'
  import { useStore } from '@nanostores/vue'
  import { profile } from '../stores/user'
  import USWDSAlert from './USWDSAlert.vue'

  const authUser = useStore(profile)
  const userList = ref([])
  const error = ref()

  function loadUsers() {
    const usersEndpoint = `${import.meta.env.PUBLIC_API_BASE_URL}/api/v1/users`

    fetch(usersEndpoint, {
      method: "GET",
      headers: { "Authorization": `Bearer ${authUser.value.jwt}` }
    }).then((res) => {
      res.json().then((data) => {
        userList.value = data
      })
    }).catch((err) => {
      error.value = err
    })
  }

  onBeforeMount(() => {
    loadUsers()
  })

</script>

<template>
  <USWDSAlert
    v-if="error"
    status="warning"
    :heading="error.name"
  >
    {{ error.message }}
  </USWDSAlert>

  <table class="usa-table">
    <thead>
      <th>Name</th>
      <th>Email</th>
      <th>Agency</th>
    </thead>
    <tbody>
      <tr
        v-for="user in userList"
        :key="user.id"
      >
        <td>{{ user.name }}</td>
        <td>{{ user.email }}</td>
        <td>{{ user.agency_id }}</td>
      </tr>
    </tbody>
  </table>
</template>
