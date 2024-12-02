<script setup>
import {computed, onMounted, reactive, ref, watch} from "vue"
import { useStore } from '@nanostores/vue'
import { useVuelidate } from "@vuelidate/core";
import { profile } from '../stores/user' 
import USWDSAlert from './USWDSAlert.vue'
import ValidatedDateRangePicker from "./form-components/ValidatedDateRangePicker.vue";
import ValidatedCheckboxGroup from "@components/form-components/ValidatedCheckboxGroup.vue";
import USWDSComboBox from "@components/form-components/USWDSComboBox.vue";
import {agencyList, bureauList, setSelectedAgencyId} from "../stores/agencies.js";

const user = useStore(profile)
const isReportUser = computed(() => user.value.roles.includes('Report'))
const agency_options = useStore(agencyList)
const bureaus = useStore(bureauList)
const report_agencies = user.value.report_agencies
let filteredAgencyOptions = ref([])
let filteredBureauOptions = ref([])

filteredAgencyOptions = computed(() => {
  return agency_options.value.filter((agency) => report_agencies.map(x => x.name).includes(agency.name))
})

filteredBureauOptions = computed(() => {
  return bureaus.value.filter((bureau) => report_agencies.map(x => x.id).includes(bureau.id))
})

const base_url = import.meta.env.PUBLIC_API_BASE_URL
const report_url = `${base_url}/api/v1/users/download-user-quiz-completion-report`

//Properties 
const user_input = reactive({
  agency_id: undefined,
  bureau_id: undefined,
  quiz_names: undefined,
  completion_date_range: undefined,
})

watch(() => user_input.agency_id, async() => {
  setSelectedAgencyId(user_input.agency_id)
  user_input.bureau_id = undefined
})


const validation_info = {
  agency_id: {},
  bureau_id: {},
  completion_date_range: {},
  quiz_names: {}
}

const quiz_names_options = [
  {value: 'Fleet Training For Program Coordinators', label: 'Fleet Training For Program Coordinators'},
  {value: 'Purchase Training for Card/Account Holders and Approving Officials', label: 'Purchase Training for Card/Account Holders and Approving Officials'},
  {value: 'Purchase Training For Program Coordinators', label: 'Purchase Training For Program Coordinators'},
  {value: 'Travel Training for Agency/Organization Program Coordinators', label: 'Travel Training for Agency/Organization Program Coordinators'},
  {value: 'Travel Training for Card/Account Holders and Approving Officials', label: 'Travel Training for Card/Account Holders and Approving Officials'},
];

const v_all_info$ = useVuelidate(validation_info, user_input)

</script>
<template>
  <section
      v-if="isReportUser"
      class="usa-prose"
  >
    <div class="padding-top-4 padding-bottom-4 grid-container">
      <h2>Download Your Report</h2>
      <h2>Enter Report Parameters</h2>
      <p>
        The GSA SmartPay Training Report has no required parameters.
      </p>
      <p>
        <b>Note:</b> If a report is generated with an individual completing multiple trainings, each training will be listed separately on the report.
      </p>
      <form
          ref="form"
          class="usa-form usa-form--large margin-bottom-3"
          data-test="report-form"
      >
        <ValidatedDateRangePicker
            v-model="user_input.completion_date_range"
            client:load
            :validator="v_all_info$.completion_date_range"
            label="Completion date range"
            name="Completion date range"
        />
        <ValidatedCheckboxGroup
            v-model="user_input.quiz_names"
            :options="quiz_names_options"
            :validator="v_all_info$.quiz_names"
            name="Quiz type(s)"
            legend="Quiz type(s)"
        />
        <USWDSComboBox
            v-model="user_input.agency_id"
            client:load
            :validator="v_all_info$.agency_id"
            :items="filteredAgencyOptions"
            label="Agency / organization"
            name="Agency"
        />
        <USWDSComboBox
            v-if="filteredBureauOptions.length"
            v-model="user_input.bureau_id"
            client:load
            :validator="v_all_info$.bureau_id"
            :items="filteredBureauOptions"
            label="Sub-agency, organization, or bureau"
            name="Bureau"
        />

      </form>
    </div>


  </section>
  <section v-else>
    <USWDSAlert
        status="error"
        class="usa-alert"
        heading="You are not authorized to receive reports."
    >
      Your email account is not authorized to access training reports. If you should be authorized, you can
      <a
          class="usa-link"
          href="mailto:gsa_smartpay@gsa.gov"
      >
        contact the GSA SmartPay team
      </a> to gain access.
    </USWDSAlert>
  </section>
</template>