<script setup>
  /**
	 * Responsible for handling the form that generates and email link.
	 * After the form is submitted it displays a message telling the user
	 * to check their email.
	 */

  import { ref, reactive, computed, onMounted, watch } from 'vue';
  import { profile, getUserFromToken } from '../stores/user'
  import { useStore } from '@nanostores/vue'
  import ValidatedInput from './ValidatedInput.vue';
  import ValidatedSelect from './ValidatedSelect.vue';
  import { useVuelidate } from '@markmeyer/vuelidate-core';
  import { required, email, helpers } from '@markmeyer/vuelidate-validators';

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
    }
  })
  const emit = defineEmits(['startLoading', 'endLoading', 'error'])
  const user = useStore(profile)
  const isLoggedIn = computed(() => Boolean(user.value.jwt))

  const user_input = reactive({
    name: undefined,
    email: undefined,
    agency_id: undefined
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

  /* Form validation for additional information if we allow registation here */
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
    }
  }
  const v_all_info$ = useVuelidate(validations_all_info, user_input)

  const tempURL = ref('')
  const isLoaded = ref(false)
  const isLoading = ref(false)
  const isFlowComplete = ref(false)
  const unregisteredEmail = ref(false)

  function clearToken() {
    const url = new URL(window.location);
    url.search = ''
    history.replaceState({}, '', url)
  }

  onMounted(async () => {
    // Handle token in url query if it exists
    const urlParams = new URLSearchParams(window.location.search);
    const parm_token = urlParams.get('t')

    if (parm_token) {
      try {
        await getUserFromToken(base_url, parm_token)
        clearToken();
      } catch(e) {
        emit('error', e)
      }
    } 
    isLoaded.value = true
  })

  async function start_email_flow() {
    const validation = unregisteredEmail.value ? v_all_info$ : v_email$
    const isFormValid = await validation.value.$validate() 

    if (!isFormValid) {
     return
    }

    emit('startLoading')
    isLoading.value = true
    
    const apiURL = new URL(`${base_url}/api/v1/get-link`)
    let res
    try {
       res = await fetch(apiURL,  {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({
          user: user_input, 
          dest: {page_id: props.pageId, title: props.title}
        })
      })
    } catch (err) {
      isLoading.value = false
      const e = new Error("Sorry, we had an error connecting to the server.")
      e.name = "Server Error"
      emit('endLoading')
      throw e
    }
    
    if (! res.ok) { 
      throw new Error(res)
    }

    const json = await res.json()
    const status = res.status
      
    if (status == 201) {
      // the api sends a 201 if the token was created
      // in the cache and an email was sent
      const token = new URL(json.token)
      tempURL.value = `${window.location.href}${token.search}` // this is just temporary while in Dev
      isFlowComplete.value = true
    } else {
      // any other 2xx response should assume
      // it worked, but we need more info
      unregisteredEmail.value = true
    }
    isLoading.value = false
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
        <p>We just sent you an email at <b>{{ user_input.email }}</b> with a link to access {{ linkDestinationText }}. This link is only active for 24 hours.</p>
        
        <p>Not the right email? <a href="/user_input">Send another email</a></p>
            
        <p><b>Temp for development</b></p>
        <p>
          URL that was emailed: <a :href="tempURL">{{ tempURL }}</a>
        </p>
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
          <fieldset class="usa-fieldset">
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
              label="Name"
              name="name"
            />
            <Suspense>
              <ValidatedSelect 
                v-model="user_input.agency_id" 
                client:load
                :validator="v_all_info$.agency_id"
                label="Agency / organization"
                name="agency"
              />
            </Suspense>
            <input
              class="usa-button"
              type="submit"
              value="Submit"
              :disabled="isLoading"
              data-test="submit"
            >
          </fieldset>
        </form>
      </div>
      <div 
        v-else
        class="usa-prose"
      >
        <slot name="initial-greeting" />

        <form
          class="usa-form usa-form--large margin-bottom-3 "
          data-test="email-submit-form"
          @submit.prevent="start_email_flow"
        >
          <fieldset class="usa-fieldset">
            <ValidatedInput 
              v-model="user_input.email" 
              client:load
              :validator="v_email$.email"
              :is-invalid="v_email$.email.$error" 
              label="Email Address"
              name="email"
              :error-message="v_email$.email.$message" 
            />  
            <input 
              class="usa-button"
              type="submit"
              value="Submit"
              :disabled="isLoading"
              data-test="submit"
            >
          </fieldset>
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
