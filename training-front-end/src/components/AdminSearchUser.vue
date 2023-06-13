<script setup>
  import {ref} from "vue";

  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const report_url = `${base_url}/api/v1/users/search-users-by-name/`

  const searchterm = ref('')
  const searchResults = ref([])
  async function search() {
    searchResults.value = await fetch(`${report_url}${searchterm.value}`).then((r) => r.json())
    console.log(searchResults.value)
  }
  function hasReporting(user) {
    return user.report_agencies.length > 0
  }
</script>

<template>
 
   <div class="padding-top-4 padding-bottom-4 grid-container">

    <div class=" grid-row">
      <div class="usa-prose tablet:grid-col-12">
        <h3>Search for a user</h3>
        <section aria-label="Search component" class="tablet:grid-col-8">
          <label for="search-field">Name</label>
          <div class="usa-hint margin-bottom-1" id="gnHint">Full or partial</div>
          <form @submit.prevent="search" class="usa-search" role="search">
            <input v-model="searchterm" class="usa-input" id="search-field" type="search" name="search" />
            <button class="usa-button" type="submit">
              <span class="usa-search__submit-text">Search </span>
            </button>
          </form>
        </section>
      </div>
    </div>
  
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
            {{ user.name }}
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
</div>
</template>