<script setup>
import {computed, reactive, ref, watch} from "vue"
import AdminAgencySelect from "./AdminAgencySelect.vue";
import DeleteIcon from "./icons/DeleteIcon.vue";
import USWDSComboBox from "./form-components/USWDSComboBox.vue";
import {agencyList, bureauList, selectedAgencyId, setSelectedAgencyId} from '../stores/agencies'
import {useStore} from '@nanostores/vue'
import AdminEditUserDetails from "./AdminEditUserDetails.vue";
import AdminViewUserCertificateTable from "./AdminViewUserCertificateTable.vue"

const props = defineProps({
  user: {
    type: Object,
    required: true,
  }
})

const editing = ref(false)

// Copy to avoid modifying parent prop and allow cancelling edits 
const agencies = ref([...props.user.report_agencies])

watch(
  () => props.user, 
  (updatedUser) => {
    if (updatedUser && updatedUser.report_agencies) {
      agencies.value = [...updatedUser.report_agencies];
    } else {
      agencies.value = [];
    }
  },
  { deep: true } // Ensures that nested changes within the user object are detected
);

const emit = defineEmits(['cancel', 'updateReportingAccess', 'userUpdateSuccess'])

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
      bureau: agencyId.value === e.id ? undefined : e.name
    })
  } else {
    agencies.value = agencies.value.filter(agency => agency.id != e.id)
    emit('updateReportingAccess', props.user.id, agencies.value)
  }
}

function editUser() {
  editing.value = true
}

watch(() => user_input.agency_id, async () => {
  setSelectedAgencyId(user_input.agency_id)
})

async function updateUser(successMessage) {
  emit('userUpdateSuccess', successMessage)
  editing.value = false
}

function cancelUpdate() {
  editing.value = false;
}

function formatDate(dateStr) {
  // Check if the string is null, undefined, or empty
  if (!dateStr || dateStr.trim() === '') {
    return 'N/A';
  }  
  
  const date = new Date(dateStr);

  // Check if the date is valid
  if (isNaN(date.getTime())) {
    return 'N/A';
  }

  //doing it this way to reduce dependancies 
  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  const month = monthNames[date.getMonth()];
  const day = date.getDate();
  const year = date.getFullYear();

  return `${month} ${day}, ${year}`;
}

  function formatString(str) {
    // Check if the string is null, undefined, or empty
    if (!str || str.trim() === '') {
        return 'N/A';
    }

    return str;
}
</script>

<template>
  <button
    id="cancel"
    class="usa-button usa-button--unstyled margin-y-2"
    type="button"
    @click="$emit('cancel')"
  >
    Return to User Search Results
  </button>
  <div v-if="!editing">
    <div class="usa-prose">
      <h2>
        User Profile
      </h2>
    </div>
    <div class="grid-row grid-gap padding-top-4">
      <div class="tablet:grid-col">
        <dt class="font-sans-xs">
          Full Name
        </dt>
        <dd
          id="user-name-value"
          :aria-label="'User Name: ' + user.name"
          class="margin-left-0 text-bold font-sans-sm"
        >
          {{ user.name }}
        </dd>
      </div>
      <div class="tablet:grid-col">
        <dt class="font-sans-xs">
          Created By
        </dt>
        <dd
          id="user-created-by-value"
          :aria-label="'Created By: ' + user.created_by"
          class="margin-left-0 text-bold font-sans-sm"
        >
          {{ user.created_by }}
        </dd>
      </div>
    </div>
    <div class="grid-row grid-gap padding-top-2">
      <div class="tablet:grid-col">
        <dt class="font-sans-xs">
          Email
        </dt>
        <dd
          id="user-email-value"
          :aria-label="'Email: ' + user.email"
          class="margin-left-0 text-bold font-sans-sm"
        >
          {{ user.email }}
        </dd>
      </div>
      <div class="tablet:grid-col">
        <dt class="font-sans-xs">
          Created On
        </dt>
        <dd
          id="user-created-on-value"
          :aria-label="'Created On: ' + formatDate(user.created_on)"
          class="margin-left-0 text-bold font-sans-sm"
        >
          {{ formatDate(user.created_on) }}
        </dd>
      </div>
    </div>
    <div class="grid-row grid-gap padding-top-2">
      <div class="tablet:grid-col">
        <dt class="font-sans-xs">
          Agency / Organization
        </dt>
        <dd
          id="user-agency-organization-value"
          :aria-label="'Agency / Organization: ' + user.agency.name"
          class="margin-left-0 text-bold font-sans-sm"
        >
          {{ user.agency.name }}
        </dd>
      </div>
      <div class="tablet:grid-col">
        <dt class="font-sans-xs">
          Last Modified By
        </dt>
        <dd
          id="user-modified-by-value"
          :aria-label="'Last Modified By: ' + formatString(user.modified_by)"
          class="margin-left-0 text-bold font-sans-sm"
        >
          {{ formatString(user.modified_by) }}
        </dd>
      </div>
    </div>
    <div class="grid-row grid-gap padding-top-2">
      <div class="tablet:grid-col">
        <dt class="font-sans-xs">
          Sub-Agency, Organization, or Bureau
        </dt>
        <dd
          id="user-bureau-value"
          :aria-label="'Sub-Agency, Organization, or Bureau: ' + user.agency.bureau"
          class="margin-left-0 text-bold font-sans-sm"
        >
          {{ user.agency.bureau }}
        </dd>
      </div>
      <div class="tablet:grid-col">
        <dt class="font-sans-xs">
          Last Modified On
        </dt>
        <dd
          id="user-modified-on-value"
          :aria-label="'Last Modified On: ' + formatDate(user.modified_on)"
          class="margin-left-0 text-bold font-sans-sm"
        >
          {{ formatDate(user.modified_on) }}
        </dd>
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
    <admin-edit-user-details
      :user-to-edit="user"
      @cancel="cancelUpdate"
      @complete-user-update="updateUser"
    />
  </div>
  <section
    v-if="!editing"
    class="margin-top-5"
  >
    <hr class="margin-bottom-5">
    <div class="usa-prose">
      <h3>
        Add Reporting Access
      </h3>
    </div>
    <div class="grid-row grid-gap">
      <div>
        <USWDSComboBox
          v-model="user_input.agency_id"
          :items="agency_options"
          label="Select agency or organization user should receive reports for?"
          name="agency"
          :required="true"
        />

        <div
          v-if="user_input.agency_id"
          class="border-1px padding-2 margin-top-2"
        >
          <AdminAgencySelect
            :items="bureaus"
            :parent="selectedAgency"
            :values="agencies"
            @check-item="editUserAgencies"
          />
        </div>
        <div class="margin-top-3">
          <button
            id="update-user"
            class="usa-button usa-button--outline"
            @click="$emit('updateReportingAccess', user.id, agencies)"
          >
            Add Reporting Access
          </button>
        </div>
      </div>
    </div>
  </section>
  <section
    v-if="!editing"
    class="margin-top-5"
  >
    <div>
      <div class="usa-prose">
        <h3>
          Granted Reporting Access
        </h3>
      </div>
      <table
        id="user-reporting-access-table"
        class="usa-table usa-table--borderless width-full"
      >
        <thead>
          <tr>
            <th
              class="text-no-wrap"
              scope="col"
            >
              Agency/Organization
            </th>
            <th
              class="text-no-wrap"
              scope="col"
            >
              Sub-Agency, Org, or Bureau
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="agencies.length === 0">
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
  <section
    v-if="!editing"
    class="margin-top-5"
  >
    <hr class="margin-bottom-5">
    <div>
      <div class="usa-prose">
        <AdminViewUserCertificateTable 
          :user="props.user"
        />
      </div>
    </div>
  </section>
</template>