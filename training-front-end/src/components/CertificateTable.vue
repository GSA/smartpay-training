<script setup>
import FileDownLoad from "./icons/FileDownload.vue"
const base_url = import.meta.env.BASE_URL

const card_icons = {
  'Travel Training for Card/Account Holders and Approving Officials': 'smartpay-blue-travel-plain.svg'
}
defineProps({
  certificates: {
    type: Array,
    default: () => []
  }
})

const data_format = { year:"numeric", month:"long", day:"numeric"}
const formatted_date = date => new Date(date).toLocaleDateString('en-US', data_format)
const card_src = training => `${base_url}images/${card_icons[training]}`
</script>
<template>
  <table class="usa-table usa-table--borderless width-full">
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
          >
          {{ cert.quiz_name }}
        </td>
        <td>
          {{ formatted_date(cert.completion_date) }}
        </td>
        <td>
          <button class="usa-button usa-button--unstyled">
            <FileDownLoad /> Download
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>