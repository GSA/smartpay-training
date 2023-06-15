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
        'numberOfPages': Number,
        'currentPage': Number // zero-indexed
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
    <nav v-if="numberOfPages" aria-label="Pagination" class="usa-pagination">
    <ul class="usa-pagination__list" data-test="page-navigation-list">
        <li  class="usa-pagination__item usa-pagination__arrow">
        <a
            :style="{visibility: showPrevious ? 'visible' : 'hidden'}" 
            data-test="previous-page-link"
            href="javascript:void(0);"
            @click.prevent="$emit('gotoPage', currentPage - 1)"
            class="usa-pagination__link usa-pagination__previous-page"
            aria-label="Previous page"
            ><NavigateBack />
            <span class="usa-pagination__link-text">Previous</span></a
        >
        </li>
        <li class="usa-pagination__item usa-pagination__page-no">
            <a
                href="javascript:void(0);"
                @click.prevent="$emit('gotoPage', 0)"
                data-test="page-link"
                :class="{'usa-current': currentPage == 0}"
                class="usa-pagination__button"
                aria-label="Page 1"
                >1</a
            >
        </li>
        <li
            v-if='interiorIndexStart != 2'
            class="usa-pagination__item usa-pagination__overflow"
            role="presentation"
            data-test="first-ellipsis"
            >
            <span>…</span>
        </li>
        <li v-for="page in range(interiorIndexStart, interiorIndexEnd)" class="usa-pagination__item usa-pagination__page-no">
            <a
                href="javascript:void(0);"
                @click.prevent="$emit('gotoPage', page - 1)"
                data-test="page-link"
                :class="{'usa-current': page == currentPage + 1 }"
                class="usa-pagination__button"
                aria-label="Page {{page}}"
                >{{page}}</a
            >
        </li>
        <li
            v-if='interiorIndexEnd != numberOfPages - 1 '
            class="usa-pagination__item usa-pagination__overflow"
            role="presentation"
            data-test="last-ellipsis"
            >
            <span>…</span>
        </li>
        <li v-if='numberOfPages > 1' class="usa-pagination__item usa-pagination__page-no">
            <a
                href="javascript:void(0);"
                @click.prevent="$emit('gotoPage', numberOfPages - 1)"
                data-test="page-link"
                :class="{'usa-current': currentPage == numberOfPages - 1}"
                class="usa-pagination__button"
                aria-label="Last Page, page {{numberOfPages}}"
                >{{numberOfPages}}</a
            >
        </li>
        
        <li  class="usa-pagination__item usa-pagination__arrow">
        <a   
            :style="{visibility: beforeLastPage ? 'visible' : 'hidden'}" 
            data-test="next-page-link"
            @click.prevent="$emit('gotoPage', currentPage + 1)"
            href="javascript:void(0);"
            class="usa-pagination__link usa-pagination__next-page"
            aria-label="Next page"
            ><span class="usa-pagination__link-text">Next </span
            ><NavigateNext />
        </a>
        </li>
    </ul>
    </nav>
</template>