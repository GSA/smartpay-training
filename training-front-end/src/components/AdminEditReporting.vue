<script setup>
  import { reactive, watch, ref, computed } from "vue"
  import AdminAgencySelect from "./AdminAgencySelect.vue";
  import DeleteIcon from "./icons/DeleteIcon.vue";
  import USWDSComboBox from "./USWDSComboBox.vue";
  import { bureauList, agencyList, setSelectedAgencyId, selectedAgencyId} from '../stores/agencies'
  import { useStore } from '@nanostores/vue'
  import AdminEditUserDetails from "@components/AdminEditUserDetails.vue";
  
  const props = defineProps({
    user: {
      type: Object,
      required: true,
    }
  })
   
  const editing = ref(false)
  
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
  
  function editUser(){
    editing.value = true
  }

  watch(() => user_input.agency_id, async() => {
    setSelectedAgencyId(user_input.agency_id)
  })
</script>

<template>
  <button
      id="cancel"
      type="button"
      class="usa-button usa-button--unstyled margin-y-2"
      @click="$emit('cancel')"
  >
    Return to User Search Results
  </button>
  <div v-if="!editing">
    <div class="usa-prose">
      <h3>
        User Profile
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
            :readonly="true"
        >
      </div>
      <div class="tablet:grid-col">
        <label
            for="input-email"
            class="usa-label"
        >
          Email
        </label>
        <input
            id="input-email"
            class="usa-input bg-base-lightest"
            name="input-email"
            :value="user.email"
            :readonly="true"
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
            :readonly="true"
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
            :readonly="true"
        >
      </div>
    </div>
    <div class="margin-top-3">
      <button
          id="toggle-user-edit"
          class="usa-button usa-button--outline"
          @click="editUser()"
      >
        Edit User Profile
      </button>
    </div>
  </div>
  <div v-if="editing">
    <admin-edit-user-details></admin-edit-user-details>
  </div>
  
  
  <section class="margin-top-5" v-if="!editing">
    <hr class="margin-bottom-5">
    <div class="usa-prose">
      <h4>
        Add Reporting Access
      </h4>
    </div>
    <div class="grid-row grid-gap">
      <div>
        <USWDSComboBox 
          v-model="user_input.agency_id"
          :items="agency_options"
          name="agency"
          label="Select agency or organization user should receive reports for?"
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
            class="usa-button usa-button--outline"
            @click="$emit('save', user.id, agencies)"
          >
            Add Reporting Access
          </button>
        </div>
      </div>
    </div>
  </section>
  <section class="margin-top-5" v-if="!editing">
    <div>
      <div class="usa-prose">
        <h4>
          Granted Reporting Access
        </h4>
      </div>
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
        <tr v-if="agencies.length == 0">
          <td colspan="4">
            None
          </td>
        </tr>
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
  </section>
</template>