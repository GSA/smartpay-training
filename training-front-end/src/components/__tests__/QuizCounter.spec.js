import { describe, it, expect } from "vitest";

import { mount } from "@vue/test-utils";
import QuizCounter from "../QuizCounter.vue";

describe("QuizCounter", () => {
  it("renders counts properly", () => {
    const wrapper = mount(QuizCounter, { props: { current: 3, total: 6}});
    expect(wrapper.text()).toContain("3 of 6 Questions")
  })

  it("renders screen reader text", () => {
    const wrapper = mount(QuizCounter, { props: { current: 3, total: 6}});
    const sr_span = wrapper.find('span[class="usa-sr-only"]')
    expect(sr_span.text()).toBe("Question")
  })
})