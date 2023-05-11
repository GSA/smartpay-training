<template>
    <div class="display-flex">
      <div class="spinner"></div>
      <div class="margin-top-1 margin-left-1">Processing...</div>
    </div>
</template>
 <style scoped>
 .spinner {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  animation: spin 1s infinite linear;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
 </style>