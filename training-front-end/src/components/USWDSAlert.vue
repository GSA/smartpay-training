<script setup>
    import { computed } from 'vue'

    const props = defineProps({
        heading: {
            type: String,
            default: "Info"
        },
        status:  {
            type: String,
            default: "informative"
        },
        hasHeading: {
          type: Boolean,
          default: true
        }
    })

    const classMap = {
        informative: "usa-alert--info",
        warning: "usa-alert--warning",
        error: "usa-alert--error",
        success: "usa-alert--success"
    }

    const alertClass = computed(() => {
        return classMap[props.status]
    })

</script>
<template>
  <div 
    class="usa-alert margin-y-2" 
    :class="alertClass" 
    data-test="alert-container"
  >
    <div class="usa-alert__body">
      <h4 
        v-if="hasHeading"
        class="usa-alert__heading" 
        data-test="heading"
      >
        {{ heading }}
      </h4>
      <p 
        class="usa-alert__text" 
        data-test="message"
      >
        <slot />
      </p>
    </div>
  </div>
</template>