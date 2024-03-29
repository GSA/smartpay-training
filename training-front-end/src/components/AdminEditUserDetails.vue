﻿<script setup>

import ValidatedInput from "./ValidatedInput.vue";
import {onBeforeMount, reactive, ref, watch} from "vue";
import {helpers, required, requiredIf} from "@vuelidate/validators";
import {useVuelidate} from "@vuelidate/core";
import ValidatedSelect from "./ValidatedSelect.vue";
import {useStore} from "@nanostores/vue";
import {agencyList, bureauList, setSelectedAgencyId} from "../stores/agencies.js";
import {profile} from "../stores/user.js";
import USWDSAlert from "./USWDSAlert.vue";
import SpinnerGraphic from "./SpinnerGraphic.vue";

const props = defineProps({
  userToEdit: {
    type: Object,
    required: true,
  }
})
const user = useStore(profile)
const base_url = import.meta.env.PUBLIC_API_BASE_URL
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
    required: withMessage('Please enter your agency', required),
  },
  bureau_id: {
    requiredIf: withMessage('Please enter your Sub-Agency, Organization, or Bureau', requiredIf(() => bureaus.value.length)),
  }
}
const v_all_info$ = useVuelidate(validations_all_info, user_input)

onBeforeMount(async () => {
  // Preselect agency based on the current user agency value. 
  setSelectedAgencyId(user_input.agency_id)
})

async function update_user_info() {
  error.value = ref()
  show_error.value = false
  const isFormValid = await v_all_info$.value.$validate()

  if (!isFormValid) {
    return
  }
  is_saving.value = true
  show_spinner.value = true

  // When user has choosen a bureau use that id instead of the agency
  let {bureau_id, ...user_data} = user_input
  if (bureau_id) {
    user_data.agency_id = bureau_id
  }

  const apiURL = new URL(`${base_url}/api/v1/users/${props.userToEdit.id}`)
  let response = ref();
  try {
    response.value = await fetch(apiURL, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${user.value.jwt}`
      },
      body: JSON.stringify(user_data)
    })
  } catch (error) {
    setError({
      name: 'Server Error',
      message: 'Sorry, we had an error connecting to the server.'
    })
    is_saving.value = false
    show_spinner.value = false
    return
  }
  if (!response.value.ok) {
    is_saving.value = false
    show_spinner.value = false
    if (response.value.status === 400) {
      setError({
        name: 'Unauthorized',
        message: 'You are not authorized to edit profile.'
      })
      return
    }
    if (response.value.status === 403) {
      setError({
        name: 'Unauthorized',
        message: "You can not update your own profile."
      })
      return
    }
    setError({
      name: 'Error',
      message: "Error contacting server."
    })
    return
  }
  is_saving.value = false
  show_spinner.value = false
  let updatedUser = await response.value.json()
  let successMessage = `Successfully updated ${updatedUser.email}`
  emit('completeUserUpdate', successMessage)
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
        <ValidatedSelect
          v-model="user_input.agency_id"
          client:load
          :validator="v_all_info$.agency_id"
          :options="agency_options"
          label="Agency / organization"
          name="agency"
        />
      </div>
      <div class="tablet:grid-col">
        <ValidatedSelect
          v-if="bureaus.length"
          v-model="user_input.bureau_id"
          client:load
          :validator="v_all_info$.bureau_id"
          :options="bureaus"
          label="Sub-Agency, Organization, or Bureau"
          name="bureau"
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
