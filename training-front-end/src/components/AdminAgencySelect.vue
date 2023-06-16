<script setup>
  import { ref, computed} from "vue"

  defineEmits(['checkItem'])

  const props = defineProps({
    'items': {
      type: Array,
      required: false,
      default: undefined
    },
    'values': {
      type: Object,
      required: true
    },
    'parent': {
      type: Object,
      required: true
    }
  })
  
  const filtertext = ref('')

  function isChecked(id) {
    return props.values.some(item => item.id == id)
  }
  const hasSubAgencies = computed(() => props.items && props.items.length > 0)
  const filtereditems = computed(() => props.items && props.items.filter(
    item => item
      .name
      .toLowerCase()
      .split(/\W+/)
      .some(word => word
        .toLowerCase()
        .startsWith(filtertext.value.toLowerCase()))
  ))
</script>

<template>
  <div 
    id="item-container"
    class="usa-prose"
  >
    <fieldset
      id="agencies"
      class="usa-fieldset"
    >
      <label
        v-if="hasSubAgencies"
        class="usa-label margin-top-0"
        for="agency-search"
      >
        Filter by sub-agency name
      </label>
      <input
        v-if="hasSubAgencies"
        id="agency-search"
        v-model="filtertext"
        class="agency-filter usa-input margin-bottom-2"
        name="agency-search"
        type="text" 
      >
      <div
        id="selected-agencies"
        class="list maxh-card-lg overflow-y-scroll padding-bottom-1"
      >
        <div
          v-if="!hasSubAgencies"
          class="usa-checkbox"
        >
          <input 
            :id="parent.id"
            class="usa-checkbox__input" 
            type="checkbox" 
            name="agencies[]" 
            :value="parent.id"
            :checked="isChecked(parent.id)"
            @change="$emit('checkItem', parent, $event.target.checked)"
          >
          <label 
            class="usa-checkbox__label agency-name"
            :for="parent.id"
          >
            {{ parent.name }}
          </label>
        </div>
        <div 
          v-for="item in filtereditems"
          :key="item.id"          
          class="usa-checkbox border-top-1px border-base-lighter padding-bottom-2" 
        >
          <input 
            :id="item.id"
            class="usa-checkbox__input" 
            type="checkbox" 
            name="agencies[]" 
            :value="item.id"
            :checked="isChecked(item.id)"
            @change="$emit('checkItem', item, $event.target.checked)"
          >
          <label
            class="usa-checkbox__label agency-name"
            :for="item.id"
          >
            {{ item.name }}
          </label>
        </div>
      </div>
    </fieldset>
  </div>
</template>