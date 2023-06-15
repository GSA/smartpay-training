<script setup>
  import { reactive, watch, ref } from "vue"
  import MultiSelect from '@components/MultiSelect.vue';
  import USWDSComboBox from "./USWDSComboBox.vue";
  import { bureauList, agencyList, setSelectedAgencyId, selectedAgencyId} from '../stores/agencies'
  import { useStore } from '@nanostores/vue'
  import ValidatedSelect from './ValidatedSelect.vue';
  import { useVuelidate } from '@vuelidate/core';
  import { required, helpers } from '@vuelidate/validators';
  const { withMessage } = helpers

  const props = defineProps({
    user: {
      type: Object,
      required: true,
    }
  })

  // we want to be able to cancel edits so
  // avoid modifying parent prop.
  const agencies = ref([...props.user.report_agencies])

  const emit = defineEmits(['addAgency', 'deleteAgency', 'cancel'])

  const agency_options = useStore(agencyList)
  const bureaus = useStore(bureauList)
  const agencyId = useStore(selectedAgencyId)

  const user_input = reactive({
    agency_id: undefined,
    bureau_id: undefined
  })

  function editUserAgencies(e, checked) {
    if (checked) {
      const agency = agency_options.value.find(agency => agency.id == agencyId.value)
      agencies.value.push({
        id: e.id,
        name: agency.name,
        bureau: e.name
      })
    } else {
      agencies.value = agencies.value.filter(agency => agency.id != e.id)
    }
  }

  watch(() => user_input.agency_id, async() => {
    setSelectedAgencyId(user_input.agency_id)
    user_input.bureau_id = undefined
  })

  const validations_all_info = {
    agency_id: {
      required: withMessage('Please enter your agency', required),
    }
  }
  const v_all_info$ = useVuelidate(validations_all_info, user_input)

</script>
<template>
  <div class="usa-prose">
    <h3>
      Edit User
    </h3>
  </div>
  <div class="grid-row grid-gap">
    <div class="tablet:grid-col">
      <label class="usa-label" for="input-full-name">Full Name</label>
      <input class="usa-input bg-base-lightest" id="input-full-name" name="input-full-name" :value="user.name" disabled/>
    </div>
    <div class="tablet:grid-col">
      <label class="usa-label" for="input-email">Full Name</label>
      <input class="usa-input bg-base-lightest" id="input-email" name="input-email" :value="user.email" disabled/>
    </div>
  </div>
  <div class="grid-row grid-gap">
    <div class="tablet:grid-col">
      <label class="usa-label" for="input-agency">Agency / Organization</label>
      <input class="usa-input bg-base-lightest" id="input-agency" name="input-agency" :value="user.agency.name" disabled/>
    </div>
    <div class="tablet:grid-col">
      <label class="usa-label" for="input-bureau">Sub-Agency, Organization, or Bureau</label>
      <input class="usa-input bg-base-lightest" id="input-bureau" name="input-bureau" :value="user.agency.bureau" disabled/>
    </div>
  </div>
  <div v-for="agency in agencies" :key="agency.id" class="margin-y-2">
    <button @click="editUserAgencies(agency, false)">[X]</button> {{ agency.name }} {{ agency.bureau }}
  </div>

  <div class="grid-row grid-gap">
    <div class="tablet:grid-col">
      <USWDSComboBox 
        v-model="user_input.agency_id"
        :items="agency_options"
        name="agency"
        label="Agency / Organization"
      />
    </div>
    <div class="tablet:grid-col">
      <MultiSelect :items="bureaus" :values="agencies" @checkItem="editUserAgencies"/>
    </div>
  </div>
  <div class="margin-top-3">
    <button class="usa-button">
      Update
    </button>
  </div>
  <button 
    @click="$emit('cancel')"
    type="button"
    class="usa-button usa-button--unstyled margin-y-2"
  >
    Cancel and return to search results
  </button>
</template>