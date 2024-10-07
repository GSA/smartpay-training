<script setup>
  /**
	 * Responsible for handling the form that generates and email link.
	 * After the form is submitted it displays a message telling the user
	 * to check their email.
   * 
   * The prop `allowRegistration` determines whether this component
   * will prompt the user for registration details if the api does 
   * not recognize their email. When set to false, it will only
   * allow known address to proceed.
	 */

  import { ref, reactive, computed, onMounted, watch } from 'vue';
  import { profile, getUserFromToken } from '../stores/user'
  import { bureauList, agencyList, setSelectedAgencyId} from '../stores/agencies'
  import { useStore } from '@nanostores/vue'
  import ValidatedInput from './ValidatedInput.vue';
  import ValidatedSelect from './ValidatedSelect.vue';
  import USWDSAlert from './USWDSAlert.vue';
  import { useVuelidate } from '@vuelidate/core';
  import { required, requiredIf, email, helpers } from '@vuelidate/validators';
  import SpinnerGraphic from './SpinnerGraphic.vue'


  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const { withMessage } = helpers

  const props = defineProps({
    'pageId': {
      type: String,
      required: true
    },
    'title': {
      type: String,
      required: true
    },
    'header': {
      type: String,
      required: true
    },
    'allowRegistration': {
      type: Boolean,
      required: false,
      default: true
    },
    'linkDestinationText': {
      type: String,
      required: true
    },
    'parameters': {
      type: String,
      required: false,
      default: ""
    }
  })

  const emit = defineEmits(['startLoading', 'endLoading', 'error'])
  const user = useStore(profile)
  const agency_options = useStore(agencyList)
  const bureaus = useStore(bureauList)
  const isLoggedIn = computed(() => Boolean(user.value.jwt))
   
  const user_input = reactive({
    name: undefined,
    email: undefined,
    agency_id: undefined,
    bureau_id: undefined
  })

  watch(() => user_input.agency_id, async() => {
    setSelectedAgencyId(user_input.agency_id)
    user_input.bureau_id = undefined
  })

  /* Form validation for email alone */
  const known_email = () => !unregisteredEmail.value || props.allowRegistration
  const validations_just_email = {
    email: {
      email: withMessage('Please enter a valid email address', email),
      required: withMessage('Please enter a valid email address', required),
      known_email: withMessage(
        "We couldn’t find the email address you entered. Please check that you entered an email address you’ve used before and that you entered it correctly.",
        known_email
      )
    }
  }
  const v_email$ = useVuelidate(validations_just_email, user_input)

  watch(() => user_input.email, async() => {
    unregisteredEmail.value = false
  })

  /* Form validation for additional information if we allow registration here */
  const showAdditionalFormFields = computed(() => props.allowRegistration && unregisteredEmail.value)
  const validations_all_info = {
    name: {
      required: withMessage('Please enter your full name', required)
    },
    email: {
      email: withMessage('Please enter a valid email address', email),
      required: withMessage('Please enter a valid email address', required),
    },
    agency_id: {
      required: withMessage('Please enter your agency', required),
    },
    bureau_id: {
      requiredIf: withMessage('Please enter your Sub-Agency, Organization, or Bureau', requiredIf(() => bureaus.value.length)),
    }
  }
  const v_all_info$ = useVuelidate(validations_all_info, user_input)

  const isLoaded = ref(false)
  const isLoading = ref(false)
  const isFlowComplete = ref(false)
  const unregisteredEmail = ref(false)
  const showSpinner = ref(false)
  const showFedWarning = ref(true)

  function clearToken() {
    const url = new URL(window.location);
    //remove token from url
    const params = new URLSearchParams(url.search);
    params.delete('t')
    url.search = params
    history.replaceState({}, '', url)
  }

  onMounted(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const parm_token = urlParams.get('t')

    if (parm_token) {
      try {
        await getUserFromToken(base_url, parm_token)
        clearToken();
      } catch(e) {
        emit('error', e)
        showSpinner.value = false;
      }
    }
    isLoaded.value = true
    showSpinner.value = false;
  })

  async function start_email_flow() {
    showFedWarning.value = true
    const validation = unregisteredEmail.value ? v_all_info$ : v_email$
    const isFormValid = await validation.value.$validate()

    if (!isFormValid) {
      showSpinner.value = false;
     return
    }

    emit('startLoading')
    isLoading.value = true
    showSpinner.value = true

    const apiURL = new URL(`${base_url}/api/v1/get-link`)
    let res
    // When user has chosen a bureau use that id instead of the agency
    let {bureau_id, ...user_data} = user_input
    if (bureau_id) {
      user_data.agency_id = bureau_id
    }
    try {
       res = await fetch(apiURL,  {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({
          user: user_data,
          dest: {page_id: props.pageId, parameters: props.parameters, title: props.title}
        })
      })
    } catch (err) {
      showFedWarning.value = false
      isLoading.value = false
      showSpinner.value = false
      const e = new Error("Sorry, we had an error connecting to the server.")
      e.name = "Server Error"
      emit('endLoading')
      throw e
    }

    if (!res.ok) {
      showFedWarning.value = false
      isLoading.value = false
      showSpinner.value = false;
      if (res.status == 401) {
        throw new Error("Unauthorized")
      }
      throw new Error("Error contacting server")
    }

    const status = res.status

    if (status == 201) {
      // the api sends a 201 if the token was created
      // in the cache and an email was sent
      isFlowComplete.value = true

    } else {
      // any other 2xx response should assume
      // it worked, but we need more info
      unregisteredEmail.value = true
    }
    isLoading.value = false
    showSpinner.value = false
    emit('endLoading')
  }
</script>

<template>
  <div v-if="!isLoggedIn && isLoaded">
    <div
      v-if="isFlowComplete"
      class="grid-row"
      data-test="post-submit"
    >
      <div class="tablet:grid-col-8 usa-prose margin-y-4">
        <h2 class="usa-prose">
          Check your email
        </h2>
        <p>We sent you an email at <b>{{ user_input.email }}</b> with a link to access {{ linkDestinationText }}. This link is only active for 24 hours. If you have not received the email within 15 minutes, please check your spam folder.</p>

        <p>Not the right email? <a href=".">Send another email</a></p>
      </div>
    </div>
    <div
      v-else
      class="grid-row"
      data-test="pre-submit"
    >
      <div
        v-if="showAdditionalFormFields"
        class=" usa-prose"
      >
        <slot name="more-info" />
        <form
          class="usa-form usa-form--large margin-bottom-3 "
          data-test="name-submit-form"
          @submit.prevent="start_email_flow"
        >
          <ValidatedInput
            v-model="user_input.email"
            client:load
            :validator="v_all_info$.email"
            label="Email Address"
            name="email"
            :readonly="true"
          />
          <ValidatedInput
            v-model="user_input.name"
            client:load
            :validator="v_all_info$.name"
            label="Full Name"
            name="name"
          />
          <ValidatedSelect
            v-model="user_input.agency_id"
            client:load
            :validator="v_all_info$.agency_id"
            :options="agency_options"
            label="Agency / organization"
            name="agency"
          />
          <ValidatedSelect
            v-if="bureaus.length"
            v-model="user_input.bureau_id"
            client:load
            :validator="v_all_info$.bureau_id"
            :options="bureaus"
            label="Sub-Agency, Organization, or Bureau"
            name="bureau"
          />
          <input
            class="usa-button"
            type="submit"
            value="Submit"
            :disabled="isLoading"
            data-test="submit"
          >
        </form>
      </div>
      <div
        v-else
        class="usa-prose"
      >
        <USWDSAlert
          v-if="showFedWarning"
          status="warning"
          class="usa-alert--slim"
          :has-heading="false"
        >
          This is a U.S. General Services Administration Federal Government computer system that is “FOR OFFICIAL USE ONLY.” This system is subject to monitoring. Individuals found performing unauthorized activities are subject to disciplinary action including criminal prosecution.<br><br>

          We only obtain your information necessary to access this system. We collect information such as agency name and email address, to issue training certificates and for agency reporting management. We carefully protect your information and will not make it available to web tracking software for retention. We do not disclose, give, sell, or transfer any personal information about our visitors, unless required for law enforcement or statute.<br><br>

          To access the GSA SmartPay® training system, please use your business or work email only, and not a personal email address.
        </USWDSAlert>
        <slot name="initial-greeting" />


        <form
          class="usa-form usa-form--large margin-bottom-3 "
          data-test="email-submit-form"
          @submit.prevent="start_email_flow"
        >
          <ValidatedInput
            v-model="user_input.email"
            client:load
            :validator="v_email$.email"
            :is-invalid="v_email$.email.$error"
            label="Email Address"
            name="email"
            :error-message="v_email$.email.$message"
          />
          <div class="grid-row">
            <div class="grid-col tablet:grid-col-3 ">
              <input
                class="usa-button"
                type="submit"
                value="Submit"
                :disabled="isLoading"
                data-test="submit"
              >
            </div>
            <!--display spinner along with submit button in one row for desktop-->
            <div
              v-if="showSpinner"
              class="display-none tablet:display-block tablet:grid-col-1 tablet:padding-top-3 tablet:margin-left-neg-1"
            >
              <SpinnerGraphic />
            </div>
          </div>
          <!--display spinner under submit button for mobile view-->
          <div
            v-if="showSpinner"
            class="tablet:display-none margin-top-1 text-center"
          >
            <SpinnerGraphic />
          </div>
        </form>
      </div>
    </div>
  </div>
  <div
    v-else
    data-test="child-component"
  >
    <slot v-if="isLoaded" />
  </div>
</template>
