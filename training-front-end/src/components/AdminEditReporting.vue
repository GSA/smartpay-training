<script setup>
  import { reactive, watch } from "vue"
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

  const emit = defineEmits(['addAgency', 'deleteAgency'])

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
      emit("addAgency",  {
        id: e.id,
        name: agency.name,
        bureau: e.name
      })
    } else {
      emit('deleteAgency', e.id)
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
  <div v-for="agency in user.report_agencies" :key="agency.id">
    <button @click="$emit('deleteAgency',agency.id)">[X]</button> {{ agency.name }} {{ agency.bureau }}
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