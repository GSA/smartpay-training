<script setup>

import ValidatedInput from "./form-components/ValidatedInput.vue";
import {onBeforeMount, reactive, ref, watch} from "vue";
import {helpers, required, requiredIf} from "@vuelidate/validators";
import {useVuelidate} from "@vuelidate/core";
import {useStore} from "@nanostores/vue";
import {agencyList, bureauList, setSelectedAgencyId} from "../stores/agencies.js";
import USWDSAlert from "./USWDSAlert.vue";
import SpinnerGraphic from "./SpinnerGraphic.vue";
import { RepositoryFactory } from "./RepositoryFactory.vue";
import USWDSComboBox from "./form-components/USWDSComboBox.vue";
const adminRepository = RepositoryFactory.get('admin')

const props = defineProps({
  userToEdit: {
    type: Object,
    required: true,
  }
})

const {withMessage} = helpers
const agency_options = useStore(agencyList)
const bureaus = useStore(bureauList)
const is_saving = ref(false)
const error = ref()
const show_error = ref(false)
const show_spinner = ref(false)

const emit = defineEmits(['cancel', 'completeUserUpdate'])

const currentUserAgencyId = agency_options.value.find(agency => agency.name === props.userToEdit.agency.name).id

const user_input = reactive({
  name: props.userToEdit.name,
  email: props.userToEdit.email,
  agency_id: currentUserAgencyId,
  bureau_id: props.userToEdit.agency_id
})

watch(() => user_input.agency_id, async () => {
  setSelectedAgencyId(user_input.agency_id)
  user_input.bureau_id = undefined
})

const validations_all_info = {
  name: {
    required: withMessage('Please enter your full name', required)
  },
  agency_id: {
    required: withMessage('Please select your agency', required),
  },
  bureau_id: {
    requiredIf: withMessage('Please select your Sub-Agency, Organization, or Bureau', requiredIf(() => bureaus.value.length)),
  }
}
const v_all_info$ = useVuelidate(validations_all_info, user_input)

onBeforeMount(async () => {
  // Preselect agency based on the current user agency value. 
  setSelectedAgencyId(user_input.agency_id)
})

async function update_user_info() {
  clearErrors()
  const isFormValid = await v_all_info$.value.$validate()

  if (!isFormValid) {
    return
  }
  is_saving.value = true
  show_spinner.value = true

  // When user has chosen a bureau use that id instead of the agency
  let {bureau_id, ...user_data} = user_input
  if (bureau_id) {
    user_data.agency_id = bureau_id
  }

  try{
    let updatedUser = await adminRepository.updateUser(props.userToEdit.id, user_data)
    let successMessage = `Successfully updated ${updatedUser.email}`
    emit('completeUserUpdate', successMessage)
  } catch(err){
    setError({
      name: 'Response Error',
      message: err
    })
  }

  is_saving.value = false
  show_spinner.value = false
}

function clearErrors(){
  error.value = ref()
  show_error.value = false
}

function setError(event) {
  error.value = event
  show_error.value = true
}
</script>

<template>
  <div class="usa-prose">
    <h3>
      Edit User Profile
    </h3>
  </div>
  <USWDSAlert
    v-if="show_error"
    status="error"
    :heading="error.name"
  >
    {{ error.message }}
  </USWDSAlert>
  <form
    class="margin-bottom-3"
    @submit.prevent="update_user_info"
  >
    <div class="grid-row grid-gap">
      <div class="tablet:grid-col">
        <ValidatedInput
          v-model="user_input.name"
          client:load
          :validator="v_all_info$.name"
          label="Full Name"
          name="name"
          :required="true"
        />
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
          :value="userToEdit.email"
          :readonly="true"
        >
      </div>
    </div>
    <div class="grid-row grid-gap">
      <div class="tablet:grid-col">
        <USWDSComboBox
          v-model="user_input.agency_id"
          client:load
          :validator="v_all_info$.agency_id"
          :items="agency_options"
          label="Agency / organization"
          name="agency"
          :required="true"
          :model-value="user_input.agency_id"
        />
      </div>
      <div class="tablet:grid-col">
        <USWDSComboBox
          v-if="bureaus.length"
          v-model="user_input.bureau_id"
          client:load
          :validator="v_all_info$.bureau_id"
          :items="bureaus"
          label="Sub-Agency, Organization, or Bureau"
          name="bureau"
          :required="true"
          :model-value="user_input.bureau_id"
        />
      </div>
    </div>
    <div class="grid-row grid-gap margin-top-3">
      <div class="tablet:grid-col">
        <input
          class="usa-button"
          type="submit"
          value="Save Profile"
          :disabled="is_saving"
        >
        <button
          id="cancel"
          type="button"
          class="usa-button usa-button--outline"
          :disabled="is_saving"
          @click="$emit('cancel')"
        >
          Cancel
        </button>
        <div
          v-if="show_spinner"
          class="display-none tablet:display-block tablet:grid-col-1 tablet:padding-top-3 tablet:margin-left-neg-1"
        >
          <SpinnerGraphic />
        </div>
      </div>
    </div>
  </form>
</template>
