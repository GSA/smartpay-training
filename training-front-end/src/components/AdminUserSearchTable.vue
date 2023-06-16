<script setup>
  import { computed } from "vue";
  const props = defineProps({
    searchResults: {
      type: Array,
      required: true
    },
    numberOfResults: {
      type: Number,
      required: true
    }
  })

  defineEmits(['selectItem'])

  const resultCount = computed(() => props.numberOfResults == 1 ? "1 Result" : `${props.numberOfResults} Results`)

  function hasReporting(user) {
    return user.report_agencies.length > 0
  }
</script>
<template>
  <table class="usa-table usa-table--borderless width-full">
    <caption>
      <span class="font-sans-lg">
        {{ resultCount }}
      </span>
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
        <td class="text-no-wrap">
          <button 
            type="button"
            class="usa-button usa-button--unstyled"
            @click="$emit('selectItem', user)" 
          >
            {{ user.name }}
          </button>
        </td>
        <td class="text-no-wrap">
          {{ user.email }}
        </td>
        <td>
          {{ user.agency.name }}
        </td>
        <td>
          {{ user.agency.bureau }}
        </td>
        <td>
          <span v-if="hasReporting(user)">
            Reporting
          </span>
        </td>
      </tr>
    </tbody>
  </table>
</template>