<script setup>
  defineProps({
    searchResults: {
      type: Array,
      required: false,
      default() {
        return []
      }
    }
  })

  defineEmits(['selectItem'])

  function hasReporting(user) {
    return user.report_agencies.length > 0
  }
</script>
<template>
  <div v-if="searchResults.length"  class=" border-top-1px margin-top-6">
    <table 
      
      class="usa-table usa-table--borderless width-full"
    >
      <caption>
        <span class="font-sans-lg">Results</span>
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
            Agency
          </th>
          <th scope="col">
            Bureau
          </th>
          <th scope="col">
            Access
          </th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="(user, index) in searchResults" 
          :key="index"
        >
          <td>
            <button @click="$emit('selectItem', user)" type="button" class="usa-button usa-button--unstyled">
              {{ user.name }}
            </button>
          </td>
          <td>
            {{ user.email }}
          </td>
          <td>
            {{ user.agency.name }}
          </td>
          <td>
            {{ user.agency.bureau }}
          </td>
          <td>
            <span v-if="hasReporting(user)">Reporting</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>