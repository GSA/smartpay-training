<script setup>
  import AdminRepository from './AdminRepository.vue';
  import ReportUtilities from './ReportUtilities.vue';

  async function downloadGspcReport() {
    let response = await AdminRepository.downloadGspcReport()
    let blob = await response.blob();
    ReportUtilities.downloadBlobAsFile(blob, 'GspcCompletionReport.csv')
  }

</script>
<template>
  <li class="usa-card tablet:grid-col-12">
    <div class="usa-card__container">
      <div class="usa-card__header">
        <h4 class="usa-card__heading">
          Download GSPC Report
        </h4>
      </div>
      <div class="usa-card__body">
        <p>
          We’ve created a report for you in CSV format. You can open it in the spreadsheet 
          application of your choice (e.g. Microsoft Excel, Google Sheets, Apple Numbers).
        </p>
      </div>         
      <div class="usa-card__footer">
        <button
          class="usa-button"
          @click="downloadGspcReport"
        >
          Download Report
        </button>
      </div>
    </div>
  </li>
</template>