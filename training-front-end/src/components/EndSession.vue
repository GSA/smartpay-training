<script setup>
  import { onMounted } from 'vue'
  import { clearUser } from '../stores/user'
 
  onMounted(() => {
    clearUser()
    window.location.href  = "/"
  })
</script>