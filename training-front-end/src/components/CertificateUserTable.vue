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
        <!--wbr will create soft break for mobile view-->
        <th scope="col">
          Agency/<wbr>Organization
        </th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          {{ user.name }}
        </td>
        <td class="mobile_view">
          {{ user.email }}
        </td>
        <td>
          {{ agency }}
        </td>
      </tr>
    </tbody>
  </table>
</template>
<style scoped>
/* 
have to make the email address word break for mobile view, 
otherwise it will stick out of container because email address is treated as one word
 */
.mobile_view{
  word-break:break-word;
  width:35%
}
</style>
