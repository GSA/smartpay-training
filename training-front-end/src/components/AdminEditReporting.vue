<script setup>
  import { reactive, watch, ref, computed } from "vue"
  import AdminAgencySelect from "./AdminAgencySelect.vue";
  import DeleteIcon from "./icons/DeleteIcon.vue";
  import USWDSComboBox from "./USWDSComboBox.vue";
  import { bureauList, agencyList, setSelectedAgencyId, selectedAgencyId} from '../stores/agencies'
  import { useStore } from '@nanostores/vue'
  
  const props = defineProps({
    user: {
      type: Object,
      required: true,
    }
  })

  // Copy to avoid modifying parent prop and allow cancelling edits 
  const agencies = ref([...props.user.report_agencies])

  defineEmits(['cancel', 'save'])

  const agency_options = useStore(agencyList)
  const bureaus = useStore(bureauList)
  const agencyId = useStore(selectedAgencyId)

  const user_input = reactive({
    agency_id: undefined,
  })

  const selectedAgency = computed(() => agency_options.value.find(agency => agency.id == agencyId.value))

  function editUserAgencies(e, checked) {
    if (checked) {
      agencies.value.push({
        id: e.id,
        name: selectedAgency.value.name,
        bureau: agencyId.value == e.id ? undefined : e.name
      })
    } else {
      agencies.value = agencies.value.filter(agency => agency.id != e.id)
    }
  }

  watch(() => user_input.agency_id, async() => {
    setSelectedAgencyId(user_input.agency_id)
  })
</script>

<template>
  <div class="usa-prose">
    <h3>
      Edit User
    </h3>
  </div>
  <div class="grid-row grid-gap">
    <div class="tablet:grid-col">
      <label
        for="input-full-name"
        class="usa-label"
      >
        Full Name
      </label>
      <input 
        id="input-full-name"
        class="usa-input bg-base-lightest"
        name="input-full-name"
        :value="user.name"
        disabled
      >
    </div>
    <div class="tablet:grid-col">
      <label
        for="input-email"
        class="usa-label" 
      >
        Full Name
      </label>
      <input
        id="input-email"
        class="usa-input bg-base-lightest"
        name="input-email"
        :value="user.email" 
        disabled
      >
    </div>
  </div>
  <div class="grid-row grid-gap">
    <div class="tablet:grid-col">
      <label 
        for="input-agency"
        class="usa-label"
      >
        Agency / Organization
      </label>
      <input
        id="input-agency"
        class="usa-input bg-base-lightest"
        name="input-agency" 
        :value="user.agency.name"
        disabled
      >
    </div>
    <div class="tablet:grid-col">
      <label
        class="usa-label"
        for="input-bureau"
      >
        Sub-Agency, Organization, or Bureau
      </label>
      <input
        id="input-bureau"
        class="usa-input bg-base-lightest"
        name="input-bureau"
        :value="user.agency.bureau"
        disabled
      >
    </div>
  </div>
  
  <section class="margin-top-5">
    <div class="usa-prose">
      <h3>
        Add Agency/Organization Reporting Access
      </h3>
    </div>
    <div class="grid-row grid-gap">
      <div class="tablet:grid-col">
        <USWDSComboBox 
          v-model="user_input.agency_id"
          :items="agency_options"
          name="agency"
          label="Search for an agency"
        />

        <div 
          v-if="user_input.agency_id"
          class="border-1px padding-2 margin-top-2"
        >
          <AdminAgencySelect 
            :items="bureaus"
            :values="agencies"
            :parent="selectedAgency"
            @check-item="editUserAgencies"
          />
        </div>
        <div class="margin-top-3">
          <button 
            id="update-user"
            class="usa-button"
            @click="$emit('save', user.id, agencies)"
          >
            Update
          </button>
        </div>
        <button 
          id="cancel"
          type="button"
          class="usa-button usa-button--unstyled margin-y-2"
          @click="$emit('cancel')"
        >
          Cancel and return to search results
        </button>
      </div>
      <div class="tablet:grid-col">
        <table class="usa-table usa-table--borderless width-full">
          <thead>
            <tr>
              <th 
                scope="col" 
                class="text-no-wrap"
              >
                Agency/Organization
              </th>
              <th
                scope="col"
                class="text-no-wrap"
              >
                Sub-Agency, Org, or Bureau
              </th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="agency in agencies" 
              :key="agency.id"
            >
              <td>
                {{ agency.name }}
              </td>
              <td>
                <div class="display-flex flex-justify">
                  <div>
                    {{ agency.bureau }}
                  </div>
                  <div class="flex-align-self-center">
                    <button 
                      class="usa-button usa-button--unstyled font-serif-lg"
                      @click="editUserAgencies(agency, false)"
                    >
                      <DeleteIcon />
                    </button>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>