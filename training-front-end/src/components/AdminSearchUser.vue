<script setup>
  import {ref} from "vue";

  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const report_url = `${base_url}/api/v1/users/search-users-by-name/`

  const searchterm = ref('')
  const searchResults = ref([])
  async function search() {
    searchResults.value = await fetch(`${api_url}/api/v1/certificates/${searchterm}`).then((r) => r.json())
  }
</script>

<template>
 
   <div class="padding-top-4 padding-bottom-4 grid-container">
    
    <div class="grid-row">
      <div class="tablet:grid-col-12">
        <h2>Search for a user</h2>
        <section aria-label="Search component" class="tablet:grid-col-8">
          <label for="search-field">Name</label>
          <div class="usa-hint margin-bottom-1" id="gnHint">Full or partial</div>
          <form class="usa-search" role="search">
            <input v-model="searchterm" class="usa-input" id="search-field" type="search" name="search" />
            <button class="usa-button" type="submit">
              <span class="usa-search__submit-text">Search </span>
            </button>
          </form>
        </section>
      </div>
    </div>
  </div>
</template>