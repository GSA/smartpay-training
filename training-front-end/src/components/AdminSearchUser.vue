<script setup>
  import { ref, computed } from "vue";
  import AdminUserSearchTable from "./AdminUserSearchTable.vue";
  import AdminEditReporting from "./AdminEditReporting.vue";
  import USWDSPagination from "./USWDSPagination.vue";

  const PAGE_SIZE = 25

  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const report_url = `${base_url}/api/v1/users/search-users-by-name/`

  const currentPage = ref(0)
  const numberOfResults = ref(0)
  const numberOfPages = computed(() => Math.ceil(numberOfResults.value/PAGE_SIZE))

  const searchTerm = ref('')
  const selectedUser = ref()
  const searchResults = ref([])
  const noResults = ref(false)

  async function setPage(page) {
    currentPage.value = page
    await search()
  }

  async function search() {
    noResults.value = false
    const url = new URL(`${report_url}${searchTerm.value}`)
    url.search = new URLSearchParams({page_number: currentPage.value + 1})
    let search_results = await fetch(url).then((r) => r.json())
    searchResults.value = search_results.users
    numberOfResults.value = search_results.total_count
    noResults.value = search_results.total_count === 0
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
      <div v-if="numberOfPages"  class=" border-top-1px margin-top-6 tablet:grid-col-12">
        <AdminUserSearchTable 
          :numberOfResults="numberOfResults"
          :searchResults="searchResults" 
          @selectItem="setCurrentUser"
        />
        <USWDSPagination 
          :currentPage="currentPage"
          :numberOfPages="numberOfPages" 
          @gotoPage="setPage"
        /> 
      </div>
      <div v-if="noResults">
      Your search returned zero results.
      </div>

    </div>
    <div v-else>
      <AdminEditReporting 
        :user="selectedUser"
        @addAgency="addAgency"
        @deleteAgency="deleteAgency"
        @cancel="setCurrentUser(undefined)"
      />
    </div>
</div>
</template>