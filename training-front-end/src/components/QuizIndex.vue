<script setup>
  import { ref } from 'vue'
  import Alert from './Alert.vue'
  import Quiz from './Quiz.vue'
  import Loginless from '../components/Loginless.vue';

  const props = defineProps(['page_id', 'title'])

	const error = ref()

  function startLoading() {
    error.value = undefined
  }
	function setError(event){
    error.value = event
	}
</script>

<template>
  <div  class="grid-container" data-test="post-submit">
    <Alert v-if="error" class="tablet:grid-col-8" status="warning" :heading="error.name">
      {{ error.message }}
    </Alert>
    <Loginless @startLoading="startLoading"  @error="setError" :page_id="page_id" :title="title">
      <Quiz :title="title" />
    </Loginless>
  </div>
</template>