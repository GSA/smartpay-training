import { describe, it, expect } from "vitest";

import { mount } from "@vue/test-utils";
import PageNavigation from "../USWDSPagination.vue";

describe("PageNvigation", () => {
    it("renders properly", () => {
        const wrapper = mount(PageNavigation, { props: { numberOfPages: 18, currentPage: 1 } });
        const el = wrapper.find('[data-test="page-navigation-list"]')
        expect(el.exists()).toBe(true)
    });

    it("does not show previously link when on first page", () => {
        const wrapper = mount(PageNavigation, { props: { numberOfPages: 5, currentPage: 0 } });
        const el = wrapper.get('[data-test="previous-page-link"]')
        expect(el.isVisible()).toBe(false)
    });

    it("does show previously link when not on first page", () => {
        const wrapper = mount(PageNavigation, { props: { numberOfPages: 5, currentPage: 1 } });
        const el = wrapper.get('[data-test="previous-page-link"]')
        expect(el.isVisible()).toBe(true)
    });

    it("does show previously link when not on last page", () => {
        const wrapper = mount(PageNavigation, { props: { numberOfPages: 5, currentPage: 2 } });
        const el = wrapper.get('[data-test="next-page-link"]')
        expect(el.isVisible()).toBe(true)
    });
    
    it("does not show previously link when on last page", () => {
        const wrapper = mount(PageNavigation, { props: { numberOfPages: 5, currentPage: 4 } });
        const el = wrapper.get('[data-test="next-page-link"]')
        expect(el.isVisible()).toBe(false)
    });

    it("renders first 5 page links", () => {
        const wrapper = mount(PageNavigation, { props: { numberOfPages: 5, currentPage: 0 } });
        const elements = wrapper.findAll('[data-test="page-link"]')
        
        expect(elements.length).toBe(5)
        expect(elements[0].text()).toBe('1')
        expect(elements[1].text()).toBe('2')
        expect(elements[2].text()).toBe('3')
        expect(elements[3].text()).toBe('4')
        expect(elements[4].text()).toBe('5')
    });

    it("renders a single page", () => {
        const wrapper = mount(PageNavigation, { props: { numberOfPages: 1, currentPage: 0 } });
        const elements = wrapper.findAll('[data-test="page-link"]')
        
        expect(elements.length).toBe(1)
        expect(elements[0].text()).toBe('1')
    });
    
    it("displays current page", () => {
        const wrapper = mount(PageNavigation, { props: { numberOfPages: 5, currentPage: 2 } });
        const elements = wrapper.findAll('[data-test="page-link"]')

        expect(elements[2].classes()).toContain('usa-current')
        expect(elements[0].classes()).not.toContain('usa-current')
    });

    it("displays end ellipsis then last link with more than 7 pages when first pages are selected", () => {
        const wrapper = mount(PageNavigation, { props: { numberOfPages: 8, currentPage: 3 } });
        const startEllipsis = wrapper.find('[data-test="first-ellipsis"]')
        const lastEllipsis = wrapper.find('[data-test="last-ellipsis"]')
        const linkElements = wrapper.findAll('[data-test="page-link"]')

        expect(startEllipsis.exists()).toBe(false)
        expect(lastEllipsis.exists()).toBe(true)
        expect(linkElements.length).toBe(6)
        expect(linkElements[3].text()).toBe('4')
        expect(linkElements[3].classes()).toContain('usa-current')
        expect(linkElements[4].text()).toBe('5')
        expect(linkElements[5].text()).toBe('8')
    });

    it("displays start ellipsis then last link with more than 7 pages when last pages are selected", () => {
        const wrapper = mount(PageNavigation, { props: { numberOfPages: 8, currentPage: 7 } });
        const startEllipsis = wrapper.find('[data-test="first-ellipsis"]')
        const lastEllipsis = wrapper.find('[data-test="last-ellipsis"]')
        const linkElements = wrapper.findAll('[data-test="page-link"]')

        expect(startEllipsis.exists()).toBe(true)
        expect(lastEllipsis.exists()).toBe(false)
        expect(linkElements.length).toBe(6)
        expect(linkElements[5].text()).toBe('8')
        expect(linkElements[1].text()).toBe('4')
    });

    it("displays both ellipsis with internal pages with more than 8 pages when internal page is selected", () => {
        const wrapper = mount(PageNavigation, { props: { numberOfPages: 9, currentPage: 4 } });
        const startEllipsis = wrapper.find('[data-test="first-ellipsis"]')
        const lastEllipsis = wrapper.find('[data-test="last-ellipsis"]')
        const linkElements = wrapper.findAll('[data-test="page-link"]')

        expect(startEllipsis.exists()).toBe(true)
        expect(lastEllipsis.exists()).toBe(true)
        expect(linkElements.length).toBe(5)
        expect(linkElements[1].text()).toBe('4')
        expect(linkElements[2].text()).toBe('5')
        expect(linkElements[2].classes()).toContain('usa-current')
        expect(linkElements[3].text()).toBe('6')
    });

    it("emits the page index when link is clicked", () => {
        const wrapper = mount(PageNavigation, { props: { numberOfPages: 5, currentPage: 3 } });
        const linkElements = wrapper.findAll('[data-test="page-link"]')
        linkElements[4].trigger('click')
        
        expect(wrapper.emitted()).toHaveProperty('gotoPage')
        const pageEvent = wrapper.emitted('gotoPage')
        expect(pageEvent).toHaveLength(1)
        expect(pageEvent[0]).toEqual([4])

        linkElements[0].trigger('click')
        expect(pageEvent).toHaveLength(2)
        expect(pageEvent[1]).toEqual([0])

     });
});
