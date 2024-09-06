<script>
  import AdminRepository from "./AdminRepository.vue";

  const repositories = {
    admin: AdminRepository,
  }

  export const RepositoryFactory = {
    get: name => repositories[name]
  }
</script>