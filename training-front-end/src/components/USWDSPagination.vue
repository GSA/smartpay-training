<script setup>
/**
 * Implementation of pagination element
 * See: https://designsystem.digital.gov/components/pagination/
 * 
 * 
 */
    import { computed } from 'vue'
    import NavigateNext from "./icons/NavigateNext.vue"
    import NavigateBack from "./icons/NavigateBack.vue"

    defineEmits(['gotoPage'])

    const props = defineProps({
        'numberOfPages': {
          type: Number,
          required: true
        },
        'currentPage': {  // zero-indexed
          type: Number,
          required: false,
          default: 0
        }
    })

    const showPrevious = computed(() => props.numberOfPages && props.currentPage > 0)
    const beforeLastPage = computed(() => props.numberOfPages && props.currentPage < props.numberOfPages -  1)

    /**
     * Returns a half-open range of integers
     */
    function range(start, stop) {
        return  Array.from({length: stop - start + 1}, (_, idx) => idx + start)
    }

    const interiorIndexStart = computed(() => {
        if (props.numberOfPages <= 7 || props.currentPage < 4) return 2
        return Math.min(props.currentPage , props.numberOfPages - 4)
    })

    const interiorIndexEnd = computed(() => {
        if (props.numberOfPages <= 7 || props.currentPage >= props.numberOfPages - 4) return props.numberOfPages - 1
        return Math.max(props.currentPage + 2, 5)
    })
</script>
<template>
  <nav
    v-if="numberOfPages"
    class="usa-pagination"
    aria-label="Pagination"
  >
    <ul 
      class="usa-pagination__list"
      data-test="page-navigation-list"
    >
      <li class="usa-pagination__item usa-pagination__arrow">
        <a
          :style="{visibility: showPrevious ? 'visible' : 'hidden'}" 
          data-test="previous-page-link"
          href="javascript:void(0);"
          class="usa-pagination__link usa-pagination__previous-page"
          aria-label="Previous page"
          @click.prevent="$emit('gotoPage', currentPage - 1)"
        ><NavigateBack />
          <span class="usa-pagination__link-text">Previous</span>
        </a>
      </li>
      <li class="usa-pagination__item usa-pagination__page-no">
        <a
          href="javascript:void(0);"
          class="usa-pagination__button"
          data-test="page-link"
          :class="{'usa-current': currentPage == 0}"
          aria-label="Page 1"
          @click.prevent="$emit('gotoPage', 0)"
        >1</a>
      </li>
      <li
        v-if="interiorIndexStart != 2"
        class="usa-pagination__item usa-pagination__overflow"
        role="presentation"
        data-test="first-ellipsis"
      >
        <span>…</span>
      </li>
      <li 
        v-for="page in range(interiorIndexStart, interiorIndexEnd)"
        :key="page"
        class="usa-pagination__item usa-pagination__page-no"
      >
        <a
          href="javascript:void(0);"
          class="usa-pagination__button"
          data-test="page-link"
          :class="{'usa-current': page == currentPage + 1 }"
          aria-label="Page {{page}}"
          @click.prevent="$emit('gotoPage', page - 1)"
        >{{ page }}</a>
      </li>
      <li
        v-if="interiorIndexEnd != numberOfPages - 1"
        class="usa-pagination__item usa-pagination__overflow"
        role="presentation"
        data-test="last-ellipsis"
      >
        <span>…</span>
      </li>
      <li
        v-if="numberOfPages > 1"
        class="usa-pagination__item usa-pagination__page-no"
      >
        <a
          href="javascript:void(0);"
          class="usa-pagination__button"
          data-test="page-link"
          :class="{'usa-current': currentPage == numberOfPages - 1}"
          aria-label="Last Page, page {{numberOfPages}}"
          @click.prevent="$emit('gotoPage', numberOfPages - 1)"
        >{{ numberOfPages }}</a>
      </li>
      
      <li class="usa-pagination__item usa-pagination__arrow">
        <a   
          href="javascript:void(0);"
          class="usa-pagination__link usa-pagination__next-page"
          :style="{visibility: beforeLastPage ? 'visible' : 'hidden'}" 
          data-test="next-page-link"
          aria-label="Next page"
          @click.prevent="$emit('gotoPage', currentPage + 1)"
        ><span class="usa-pagination__link-text">Next </span><NavigateNext />
        </a>
      </li>
    </ul>
  </nav>
</template>