<script setup>
  import { ref, onErrorCaptured, onBeforeMount } from 'vue';
  import { useStore } from '@nanostores/vue'
  import { profile} from '../stores/user'
  import USWDSAlert from './USWDSAlert.vue'
  import Loginless from './LoginlessFlow.vue';

  const user = useStore(profile)
  const base_url = import.meta.env.PUBLIC_API_BASE_URL
  const quiz = ref()
  const userSelections = ref([])

  const props = defineProps({
    'pageId': {
      type: String,
      required: true,
    }, 
    'title': {
      type: String,
      required: true,
    },
    'header': {
      type: String,
      required: true,
    },
    'subhead': {
      type: String,
      required: true,
    }
  })

  onBeforeMount(async () => {

  })

  onErrorCaptured((err) => {
    setError(err)
    return false
  })

	const error = ref()


  function startLoading() {
    error.value = undefined
  }

	function setError(event){
    error.value = event
	}
</script>

<template>
  <div 
    class="padding-top-4 padding-bottom-4" 
    :class="{'bg-base-lightest': isStarted && !isSubmitted}"
  >
    <div
      class="grid-container"
      data-test="post-submit"
    >
      <div class="grid-row">
        <div class="tablet:grid-col-12">
          <USWDSAlert
            v-if="error"
            class="tablet:grid-col-8"
            status="error"
            :heading="error.name"
          >
            {{ error.message }}
          </USWDSAlert>
          <Suspense>
            <template #fallback>
              …Loading
            </template>
            <Loginless
              page-id="gspc_registration"
              :title="title"
              :header="header"
              parameters="date=01-31-2012"
              link-destination-text="GSPC Registration"
              @start-loading="startLoading"
              @error="setError"
            >
              <template #initial-greeting>
                <h2>GSPC Registration</h2>
                <p>Enter your email address to login. You'll receive an email with an access link.</p>
              </template>
              
              <template #more-info>
                <h2>Welcome!</h2>
                <p>Before you can register for GSPC, you'll need to create and complete your profile.</p>
              </template>

              <h2>GSPC Placeholder</h2>
              <p>logged in</p>
            </Loginless>
          </Suspense>
        </div>
      </div>
    </div>
  </div>
</template>