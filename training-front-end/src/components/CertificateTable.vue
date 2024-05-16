<script setup>
  import { onMounted, ref } from "vue"
  import FileDownLoad from "./icons/FileDownload.vue"
  import { useStore } from '@nanostores/vue'
  import { profile} from '../stores/user'

  const base_url = import.meta.env.BASE_URL
  const api_url = import.meta.env.PUBLIC_API_BASE_URL
  const user = useStore(profile)


  const card_icons = {
    'Travel Training for Card/Account Holders and Approving Officials': 'smartpay-blue-travel-plain.svg',
    'Travel Training for Agency/Organization Program Coordinators': 'smartpay-blue-travel-plain.svg',
    'Purchase Training for Card/Account Holders and Approving Officials': 'smartpay-red-purchase-plain.svg',
    'Purchase Training For Program Coordinators': 'smartpay-red-purchase-plain.svg',
    'Fleet Training For Program Coordinators': 'smartpay-green-fleet-plain.svg'
  }

  const certificates = ref([]) 
 
  onMounted(async() => {
      certificates.value = await fetch(`${api_url}/api/v1/certificates/`, {
        method: 'GET',
        headers: {'Authorization': `Bearer ${user.value.jwt}`}
      }
       ).then((r) => r.json())
    })

  const data_format = { year:"numeric", month:"long", day:"numeric"}
  const formatted_date = date => new Date(date).toLocaleDateString('en-US', data_format)
  const card_src = training => `${base_url}images/${card_icons[training]}`

</script>

<template>
  <table 
    v-if="certificates.length" 
    class="usa-table usa-table--borderless width-full"
  >
    <caption>
      <span class="font-sans-lg">Certificates</span>
    </caption>
    <thead>
      <tr>
        <th scope="col">
          Business Line
        </th>
        <th scope="col">
          Date Earned
        </th>
        <th scope="col">
          Certificate
        </th>
      </tr>
    </thead>
    <tbody>
      <tr 
        v-for="(cert, index) in certificates" 
        :key="index"
      >
        <td>
          <img 
            :src="card_src(cert.quiz_name)" 
            class="text-middle margin-right-1" 
            :style="{height:'1.5rem'}" 
            aria-hidden="true" 
            alt=""
          >
          {{ cert.quiz_name }}
        </td>
        <td>
          {{ formatted_date(cert.completion_date) }}
        </td>
        <td>
          <form
            :action="`${api_url}/api/v1/certificate/quiz/${cert.id}`" 
            method="post"
          >
            <input 
              type="hidden"
              name="jwtToken"
              :value="user.jwt"
            >
            <button
              class="usa-button usa-button--unstyled"
              type="submit"
            >
              <FileDownLoad /> Download
            </button>
          </form>
        </td>
      </tr>
    </tbody>
  </table>
  <div v-else>
    <h3>
      Certificates
    </h3>
    <!--eslint-disable-next-line vue/max-attributes-per-line-->
    You have not earned any certificates yet. <a :href="base_url" class="usa-link">Take a training</a> to earn a certificate.
  </div>
</template>