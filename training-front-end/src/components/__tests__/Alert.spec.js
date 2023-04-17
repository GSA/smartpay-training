import { describe, it, expect } from "vitest";
import { mount } from "@vue/test-utils";
import Alert from "../Alert.vue";

describe("Alert", () => {
  it("renders default case properly", () => {
    const wrapper = mount(Alert, { slots: { default: "The library, and step on it"}});
    const heading = wrapper.get('[data-test="heading"]')
    const message = wrapper.get('[data-test="message"]')

    expect(heading.text()).toBe("Info");
    expect(message.text()).toBe("The library, and step on it");
    expect(wrapper.classes()).toContain('usa-alert--info')
  });

  it("renders header prop as the alert header", () => {
    const wrapper = mount(Alert, { 
        props: {heading: "Warning!!"},
        slots: { default: "The library, and step on it"}
    });
    const header = wrapper.get('[data-test="heading"]')

    expect(header.text()).toBe("Warning!!");
  });

  it("renders status prop by indicating corresponding USWDS calss", () => {
    const wrapper = mount(Alert, { 
        props: {heading: "Error!!", status: "error"},
        slots: { default: "The truth will set you free. But not until it is finished with you."}
    });
    const header = wrapper.get('[data-test="heading"]')

    expect(header.text()).toBe("Error!!");
    expect(wrapper.classes()).toContain('usa-alert--error')
  });
});
