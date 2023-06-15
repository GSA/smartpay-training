<script setup>
  import { reactive, watch, ref } from "vue"
  import MultiSelect from '@components/MultiSelect.vue';
  import { bureauList, agencyList, setSelectedAgencyId, selectedAgencyId} from '../stores/agencies'
  import { useStore } from '@nanostores/vue'
  import ValidatedSelect from './ValidatedSelect.vue';
  import { useVuelidate } from '@vuelidate/core';
  import { required, requiredIf, helpers } from '@vuelidate/validators';
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
      console.log(e, agencies.value)
      agencies.value = agencies.value.filter(agency => agency.id != e.id)
      //emit('deleteAgency', e.id)
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
  <div>
    {{ user.name }} | {{ user.email }} 
  </div>
  <div v-for="agency in agencies" :key="agency.id">
    <button @click="editUserAgencies(agency, false)">[X]</button> {{ agency.name }} {{ agency.bureau }}
  </div>

  <ValidatedSelect
    v-model="user_input.agency_id"
    :validator="v_all_info$.agency_id"
    :options="agency_options"
    label="Agency / organization"
    name="agency"
  />
  <MultiSelect :items="bureaus" :values="agencies" @checkItem="editUserAgencies"/>
  <button 
    @click="$emit('cancel')"
    type="button"
    class="usa-button usa-button--unstyled margin-y-2"
  >
    Cancel and return to search results
  </button>
</template>