<script setup>
  import { UseFocusTrap } from '@vueuse/integrations/useFocusTrap/component'
  defineEmits(['continueSession', 'exit'])
</script>

<template>
  <teleport to="body">
    <UseFocusTrap>
      <div
        class="usa-modal-wrapper"
        role="dialog"
        aria-labelledby="modal-heading"
        aria-describedby="modal-description"
      >
        <div class="usa-modal-overlay">
          <div
            id="exit-modal"
            class="usa-modal"
            tabindex="-1"
          >
            <div class="usa-modal__content">
              <div class="usa-modal__main">
                <h2 
                  id="modal-heading"
                  class="usa-modal__heading" 
                >
                  Your session will end soon.
                </h2>
                <div class="usa-prose">
                  <p id="modal-description">
                    You’ve been inactive for too long. Please choose to stay signed in
                    or sign out. Otherwise, you’ll be signed out automatically in five
                    minutes.
                  </p>
                </div>
                <div class="usa-modal__footer">
                  <ul class="usa-button-group">
                    <li class="usa-button-group__item">
                      <button 
                        type="button"
                        class="usa-button"
                        @click="$emit('continueSession')"
                      >
                        Yes, stay signed in
                      </button>
                    </li>
                    <li class="usa-button-group__item">
                      <button
                        type="button"
                        class="usa-button usa-button--unstyled padding-105 text-center"
                        @click="$emit('exit')"
                      >
                        Exit
                      </button>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </UseFocusTrap>
  </teleport>
</template>