<script setup>
  import { ref, computed } from "vue";
  import AdminUserSearchTable from "./AdminUserSearchTable.vue";
  import AdminEditReporting from "./AdminEditReporting.vue";
  import USWDSPagination from "./USWDSPagination.vue";
  import USWDSAlert from './USWDSAlert.vue'
  import { setSelectedAgencyId} from '../stores/agencies'
  import { RepositoryFactory } from "./RepositoryFactory.vue";
  import {useStore} from "@nanostores/vue";
  import {profile} from "../stores/user.js";
  const adminRepository = RepositoryFactory.get('admin')

  const PAGE_SIZE = 25

  const base_url = import.meta.env.BASE_URL
  const user = useStore(profile)
  const isAdminUser = computed(() => user.value.roles.includes('Admin'))
  let currentPage = ref(0)
  let numberOfResults = ref(0)
  const numberOfPages = computed(() => Math.ceil(numberOfResults.value/PAGE_SIZE))

  let searchTerm = ref('')
  const selectedUser = ref()
  let searchResults = ref([])
  const noResults = ref(false)
  const error = ref()
  const showSuccessMessage = ref(false)
  const successMessage = ref()

  async function setPage(page) {
    currentPage.value = page
    await search()
  }

  async function search() {
    clearAlerts()
    noResults.value = false
    try {
      let search_results = await adminRepository.userSearch(searchTerm.value, currentPage.value)
      searchResults.value = search_results.users
      numberOfResults.value = search_results.total_count
      noResults.value = search_results.total_count === 0
    } catch (err) {
      error.value = err
    }
  }
 
  async function updateUserReports(userId, agencyIds) {
    try {
      let updatedUser = await adminRepository.updateUserReports(userId, agencyIds)
      selectedUser.value.report_agencies = updatedUser.report_agencies
      updateUserSuccess("Updated users reporting access")
      refreshSelectedUser()
    } catch (err){
      error.value = err
    }
  }

  async function refreshSelectedUser(){
    if(!selectedUser.value){
      return
    }

    try{
      selectedUser.value = await adminRepository.getUser(selectedUser.value.id)
    } catch (err) {
      error.value = err
    }
  }

  function setSelectedUser(e) {
    selectedUser.value = e
  }

  function cancelEdit(){
    setSelectedUser(undefined)
    setSelectedAgencyId(undefined)
    // refresh search on cancel from edit reporting page as you can also update user details on the page without
    // updating the reporting access. Refresh page to display updated details.
    search()
  }
  
  async function updateUserSuccess(message) {
    refreshSelectedUser()
    successMessage.value = message
    showSuccessMessage.value = true
  }
  
  function clearAlerts() {
    error.value = undefined
    successMessage.value = undefined
    showSuccessMessage.value = false
  }
</script>

<template>
  <section
    v-if="isAdminUser"
    class="usa-prose"
  >
    <div class="padding-top-4 padding-bottom-4 grid-container">
      <USWDSAlert
        v-if="error"
        status="error"
        :heading="error.name"
      >
        {{ error.message }}
      </USWDSAlert>
      <USWDSAlert
        v-if="showSuccessMessage"
        status="success"
        class="usa-alert--slim"
        :has-heading="false"
      >
        {{ successMessage }}
      </USWDSAlert>
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
              Name or Email
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
                :disabled="!searchTerm"
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
            @select-item="setSelectedUser"
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
          @update-reporting-access="updateUserReports"
          @cancel="cancelEdit"
          @user-update-success="updateUserSuccess"
        />
      </div>
    </div>
  </section>
  <section v-else>
    <USWDSAlert
      status="error"
      class="usa-alert"
      heading="You are not authorized to access."
    >
      Your email account is not authorized to access. If you should be authorized, you can contact the
      <a
        class="usa-link"
        href="mailto:gsa_smartpay@gsa.gov"
      >
        GSA SmartPay team
      </a> to gain access.
    </USWDSAlert>
    <p><a :href="base_url">Return to Home</a></p>
  </section>
</template>