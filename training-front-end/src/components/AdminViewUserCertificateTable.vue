<script setup>
  import { onMounted, ref } from "vue"
  import FileDownLoad from "./icons/FileDownload.vue"
  import { useStore } from '@nanostores/vue'
  import { profile} from '../stores/user'

  const props = defineProps({
    user: {
      type: Object,
      required: true,
    }
  })


  const base_url = import.meta.env.BASE_URL
  const api_url = import.meta.env.PUBLIC_API_BASE_URL
  const adminUser = useStore(profile)


  const cert_icons = {
    'Travel Training for Card/Account Holders and Approving Officials': 'smartpay-blue-travel-plain.svg',
    'Travel Training for Agency/Organization Program Coordinators': 'smartpay-blue-travel-plain.svg',
    'Purchase Training for Card/Account Holders and Approving Officials': 'smartpay-red-purchase-plain.svg',
    'Purchase Training For Program Coordinators': 'smartpay-red-purchase-plain.svg',
    'Fleet Training For Program Coordinators': 'smartpay-green-fleet-plain.svg',
    'GSA SmartPay Program Certification (GSPC)': 'gspc.svg'
  }

  const certificates = ref([]) 
 
  onMounted(async() => {
      certificates.value = await fetch(`${api_url}/api/v1/certificates/${props.user.id}`, {
        method: 'GET',
        headers: {'Authorization': `Bearer ${adminUser.value.jwt}`}
      }
       ).then((r) => r.json())
    })

  const data_format = { year:"numeric", month:"long", day:"numeric"}
  const formatted_date = date => new Date(date).toLocaleDateString('en-US', data_format)
  const formatted_time = date => new Date(date).toLocaleTimeString('en-US')
  const cert_img_src = cert => `${base_url}images/${cert_icons[cert]}`

</script>

<template>
  <table 
    v-if="certificates.length" 
    class="usa-table usa-table--borderless width-full"
  >
    <caption>
      <span class="font-sans-lg">View Certificates</span>
    </caption>
    <thead>
      <tr>
        <th
          scope="col"
          style="padding-left: 0;"
        >
          Certificate Name
        </th>
        <th scope="col">
          Date Earned
        </th>
        <th scope="col">
          Time Earned
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
          <div class="grid-row">
            <div class="grid-col flex-auto">          
              <img
                width="38.5"
                height="24"
                :src="cert_img_src(cert.cert_title)" 
                class="text-middle margin-right-1"
                aria-hidden="true" 
                alt=""
              >
            </div>
            <div class="grid-col">
              {{ cert.cert_title }}
            </div>
          </div>
        </td>
        <td>
          {{ formatted_date(cert.completion_date) }}
        </td>
        <td>
          {{ formatted_time(cert.completion_date) }}
        </td>
        <td>
          <form
            :action="`${api_url}/api/v1/certificate/${cert.certificate_type}/${cert.id}`" 
            method="post"
          >
            <input 
              type="hidden"
              name="jwtToken"
              :value="adminUser.jwt"
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
    User has not earned any certificates yet.
  </div>
</template>
