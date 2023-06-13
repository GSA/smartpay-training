<script setup>
  import { reactive, watch } from "vue"
  import MultiSelect from '@components/MultiSelect.vue';
  import { bureauList, agencyList, setSelectedAgencyId, selectedAgencyId} from '../stores/agencies'
  import { useStore } from '@nanostores/vue'
  import ValidatedSelect from './ValidatedSelect.vue';
  import { useVuelidate } from '@vuelidate/core';
  import { required, requiredIf, helpers } from '@vuelidate/validators';
  const { withMessage } = helpers


const user = reactive({
    "email": "mark.meyer@gsa.gov",
    "name": "Mark Meyer",
    "id": 1,
    "agency_id": 51,
    "agency": {
      "name": "General Services Administration",
      "bureau": null,
      "id": 51
    },
    "roles": [
      {
        "name": "Report",
        "id": 1
      }
    ],
    "report_agencies": {
      51: {
        "name": "General Services Administration",
        "bureau": null,
        "id": 51
      },
      135: {
        "name": "Department of Education",
        "bureau": "Office of Career, Technical, and Adult Education",
        "id": 135
      }
    }
  })

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
      user.report_agencies[e.id] = {
        id: e.id,
        name: agency.name,
        bureau: e.name
      }
    } else {
      delete user.report_agencies[e.id]
    }
    console.log("Event: ", e, checked)
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
  <div v-for="agency in user.report_agencies">
    x {{agency.name}} | {{ agency.bureau }}
  </div>

  <ValidatedSelect
    v-model="user_input.agency_id"
    :validator="v_all_info$.agency_id"
    :options="agency_options"
    label="Agency / organization"
    name="agency"
  />
  <MultiSelect :items="bureaus" :values="user.report_agencies" @checkItem="editUserAgencies"/>
</template>