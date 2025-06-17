<script setup>
import {useStore} from "@nanostores/vue";
import {profile} from "../stores/user.js";
import {computed} from "vue";
import USWDSAlert from "./USWDSAlert.vue";

const base_url = import.meta.env.BASE_URL
const user = useStore(profile)
const isAdminUser = computed(() => user.value.roles.includes('Admin'))
</script>
<template>
  <section
      v-if="isAdminUser"
      class="usa-prose"
  >
    <div class="padding-top-4 padding-bottom-4 grid-container">
      <ul class="usa-card-group">
        <li class="usa-card tablet:grid-col-6">
          <div id="user-maintenance-card" class="usa-card__container">
            <div class="usa-card__header">
              <h4 class="usa-card__heading">User Maintenance</h4>
            </div>
            <div class="usa-card__body">
              <p>
                Allows administrators to search for users and view or manage their user permissions.
              </p>
            </div>
            <div class="usa-card__footer">
              <a :href="`${base_url}admin/user_search/`" class="card_link usa-button">
                Search for users
              </a>
            </div>
          </div>
        </li>
        <li class="usa-card tablet:grid-col-6">
          <div id="gspc-card" class="usa-card__container">
            <div class="usa-card__header">
              <h4 class="usa-card__heading">GSA SmartPay® Program Certification Management</h4>
            </div>
            <div class="usa-card__body">
              <p>
                Allows administrators to notify GSPC attendees to complete requirements and receive a certificate.
              </p>
            </div>
            <div class="usa-card__footer">
              <a :href="`${base_url}admin/gspc/`" class="card_link usa-button">
                Manage GSPC attendees
              </a>
            </div>
          </div>
        </li>
        <li class="usa-card tablet:grid-col-6">
          <div id="system-reports-card" class="usa-card__container">
            <div class="usa-card__header">
              <h4 class="usa-card__heading">System Reports</h4>
            </div>
            <div class="usa-card__body">
              <p>
                Allows administrators to download reports.
              </p>
            </div>
            <div class="usa-card__footer">
              <a :href="`${base_url}admin/reports/`" class="card_link usa-button">
                Reports
              </a>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </section>
  <section v-else>
    <USWDSAlert
        status="error"
        class="usa-alert"
        heading="You are not authorized to access."
    >
      Your email account is not authorized to access. If you should be authorized, you can contact the
      <a
          class="usa-link"
          href="mailto:gsa_smartpay@gsa.gov"
      >
         GSA SmartPay team
      </a> to gain access.
    </USWDSAlert>
  </section>
</template>