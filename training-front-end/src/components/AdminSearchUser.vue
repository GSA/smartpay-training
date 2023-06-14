<script setup>
  import {ref} from "vue";
  import AdminUserSearchTable from "./AdminUserSearchTable.vue";
  import AdminEditReporting from "./AdminEditReporting.vue";

  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const report_url = `${base_url}/api/v1/users/search-users-by-name/`

  const searchTerm = ref('')
  const selectedUser = ref()
  const searchResults = ref([])

  async function search() {
    searchResults.value = await fetch(`${report_url}${searchTerm.value}`).then((r) => r.json())
  }
 
  function setCurrentUser(e) {
    selectedUser.value = e
  }

  function addAgency(e) {
    selectedUser.value.report_agencies.push(e)
  }

  function deleteAgency(id) {
    selectedUser.value.report_agencies = selectedUser.value.report_agencies.filter(agency => agency.id != id)
  }
</script>

<template>
   <div class="padding-top-4 padding-bottom-4 grid-container">

    <div v-if="!selectedUser" class=" grid-row">
      <div class="usa-prose tablet:grid-col-12">
        <h3>Search for a user</h3>
        <section aria-label="Search component" class="tablet:grid-col-8">
          <label for="search-field">Name</label>
          <div class="usa-hint margin-bottom-1" id="gnHint">Full or partial</div>
          <form @submit.prevent="search" class="usa-search" role="search">
            <input v-model="searchTerm" class="usa-input" id="search-field" type="search" name="search" />
            <button class="usa-button" type="submit">
              <span class="usa-search__submit-text">Search </span>
            </button>
          </form>
        </section>
      </div>
      <AdminUserSearchTable :searchResults="searchResults" @selectItem="setCurrentUser" />
    </div>
    <div v-else>
      <AdminEditReporting 
        :user="selectedUser"
        @addAgency="addAgency"
        @deleteAgency="deleteAgency"
      />
    </div>
    
</div>
</template>