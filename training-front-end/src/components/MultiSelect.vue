<script setup>
  import { ref, computed} from "vue"
  const title = "Sub-Agency, Organization, or Bureau"
  const filtertext = ref('')

  const props = defineProps({
    'items': {
      type: Array,
      required: false,
      default: undefined
    },
    'values': {
      type: Object,
      required: true
    }
  })
  const emit = defineEmits(['checkItem'])

  const filtereditems = computed(() => props.items && props.items.filter(
    item => item
      .name
      .toLowerCase()
      .split(/[ ,]+/)
      .some(word => word
        .toLowerCase()
        .startsWith(filtertext.value.toLowerCase()))
  ))
</script>

<template>
  <div id="item-container" class="usa-prose">
    Search: {{ filtertext }}
    <fieldset id="agencies" class="usa-fieldset">
      <label for="agency-search">Filter by sub-agency name</label>
      <input v-model="filtertext" id="agency-search" class="agency-filter usa-input" name="agency-search" type="text" />
      <div id="agency-filter-help-text" class="usa-prose" aria-live="polite" aria-atomic="true"></div>

      <div id="selected-agencies" class="list">
          <div class="usa-checkbox" v-for="item in filtereditems" :key="item.id">
            <input 
              class="usa-checkbox__input" 
              :id="item.id"
              type="checkbox" 
              name="agencies[]" 
              :value="item.id"
              :checked="values.hasOwnProperty(item.id)"
              @change="$emit('checkItem', item, $event.target.checked)"
            >
            <label class="usa-checkbox__label agency-name" :for="item.id">{{ item.name }}</label>
            <div class="agency-short-name" hidden>{{item.name}}</div>
          </div>
      </div>
    </fieldset>
  </div>
</template>