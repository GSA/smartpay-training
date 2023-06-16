<script setup>
  import { ref, computed } from "vue";
  import AdminUserSearchTable from "./AdminUserSearchTable.vue";
  import AdminEditReporting from "./AdminEditReporting.vue";
  import USWDSPagination from "./USWDSPagination.vue";
  import { setSelectedAgencyId} from '../stores/agencies'

  const PAGE_SIZE = 25

  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const report_url = `${base_url}/api/v1/users/search-users-by-name/`
  const update_url = `${base_url}/api/v1/users/edit-user-for-reporting/`

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
 
  async function updateUserReports(userId, agencyIds) {
    const agencies = agencyIds.map(a => a.id)
    const url = new URL(update_url)
    url.search = new URLSearchParams({user_id: userId})
    let updatedUser = await fetch(
      url, { 
        method: "PUT", 
        headers: { 
          'Content-Type': 'application/json',
          // this will be needed when admin auth is in place
          // 'Authorization': `Bearer ${user.value.jwt}` 
        },
        body:  JSON.stringify(agencies) 
      }
    ).then((r) => r.json())
    selectedUser.value.report_agencies = updatedUser.report_agencies
    setCurrentUser(undefined)
    setSelectedAgencyId(undefined)
  }

  function setCurrentUser(e) {
    selectedUser.value = e
  }

  function cancelEdit(){
    setCurrentUser(undefined)
    setSelectedAgencyId(undefined)
  }
</script>

<template>
  <div class="padding-top-4 padding-bottom-4 grid-container">
    <div 
      v-if="!selectedUser"
      class="grid-row"
    >
      <div class="usa-prose tablet:grid-col-12">
        <h3>Search for a user</h3>
        <section
          aria-label="Search component"
          class="tablet:grid-col-8"
        >
          <label for="search-field">
            Name
          </label>
          <div 
            id="gnHint"
            class="usa-hint margin-bottom-1"
          >
            Full or partial
          </div>
          <form 
            class="usa-search"
            role="search"
            @submit.prevent="search"
          >
            <input 
              id="search-field"
              v-model="searchTerm"
              class="usa-input"
              type="search"
              name="search"
            >
            <button 
              class="usa-button"
              type="submit"
            >
              <span class="usa-search__submit-text">
                Search
              </span>
            </button>
          </form>
        </section>
      </div>
      <div 
        v-if="numberOfPages"
        class="border-top-1px margin-top-6 tablet:grid-col-12"
      >
        <AdminUserSearchTable 
          :number-of-results="numberOfResults"
          :search-results="searchResults" 
          @select-item="setCurrentUser"
        />
        <USWDSPagination 
          :current-page="currentPage"
          :number-of-pages="numberOfPages" 
          @goto-page="setPage"
        /> 
      </div>
      <div 
        v-if="noResults"
        class="margin-top-3"
      >
        Your search returned zero results.
      </div>
    </div>
    <div v-else>
      <AdminEditReporting 
        :user="selectedUser"
        @save="updateUserReports"
        @cancel="cancelEdit"
      />
    </div>
  </div>
</template>