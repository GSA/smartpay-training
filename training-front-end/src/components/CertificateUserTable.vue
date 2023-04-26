<script setup>
import { onMounted, ref } from "vue"
import { useStore } from '@nanostores/vue'
import { profile} from '../stores/user'

const api_url = import.meta.env.PUBLIC_API_BASE_URL
const user = useStore(profile)
const agency = ref('')

onMounted(async () => {
  let r = await fetch(`${api_url}/api/v1/agencies/${user.value.agency_id}`)
  .then(r => r.json())
  .catch(e => console.log("error hitting api: ", e))
  agency.value = r['name']
})
</script>
<template>
  <table class="usa-table usa-table--borderless width-full">
    <caption>
      <span class="font-sans-lg">Account Details</span>
    </caption>
    <thead>
      <tr>
        <th scope="col">
          Name
        </th>
        <th scope="col">
          Email
        </th>
        <th scope="col">
          Agency/Organization
        </th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          {{ user.name }}
        </td>
        <td>
          {{ user.email }}
        </td>
        <td>
          {{ agency }}
        </td>
      </tr>
    </tbody>
  </table>
</template>
