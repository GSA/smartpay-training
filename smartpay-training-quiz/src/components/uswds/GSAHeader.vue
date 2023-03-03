<script setup>
    const props = defineProps({
        'linkHome': {
            type: Boolean,
            default: true,
        },
    })
</script>
<template>
<header class="usa-header usa-header--extended">
  <div class="usa-navbar">
    <div v-if="linkHome" class="usa-logo" id="header-logo">
        <router-link to="/">
            <img class="usa-logo-img" src="@/assets/images/gsa-smartpay-training-logo.svg" alt="GSA SmartPay Logo" title="U.S. General Services Administration">
        </router-link>
    </div>
    <div v-else class="usa-logo" id="header-logo">
        <img class="usa-logo-img" src="@/assets/images/gsa-smartpay-training-logo.svg" alt="GSA SmartPay Logo" title="U.S. General Services Administration">
    </div>
  </div>
  <button type="button" class="usa-menu-btn">Menu</button>
  <nav aria-label="Primary navigation" class="usa-nav">
    <div class="usa-nav__inner">
      <button type="button" class="usa-nav__close">
        <img src="@/assets/images/usa-icons/close.svg" role="img" alt="Close" />
      </button>
      <ul class="usa-nav__primary usa-accordion">
        <li class="usa-nav__primary-item">
          <button
            type="button"
            class="usa-accordion__button usa-nav__link"
            aria-expanded="false"
            aria-controls="extended-nav-section-one"
          >
            <span>Account Holders &amp; Approving Officials</span>
          </button>
          <ul id="extended-nav-section-one" class="usa-nav__submenu">
            <li class="usa-nav__submenu-item">
              <a href=""><span>&lt;Navigation link&gt;</span></a>
            </li>
            <li class="usa-nav__submenu-item">
              <a href=""><span>&lt;Navigation link&gt;</span></a>
            </li>
            <li class="usa-nav__submenu-item">
              <a href=""><span>&lt;Navigation link&gt;</span></a>
            </li>
            <li class="usa-nav__submenu-item">
              <a href=""><span>&lt;Navigation link&gt;</span></a>
            </li>
          </ul>
        </li>
        <li class="usa-nav__primary-item">
          <button
            type="button"
            class="usa-accordion__button usa-nav__link"
            aria-expanded="false"
            aria-controls="extended-nav-section-two"
          >
            <span>Program Coordinators</span>
          </button>
          <ul id="extended-nav-section-two" class="usa-nav__submenu">
            <li class="usa-nav__submenu-item">
              <a href=""><span>&lt;Navigation link&gt;</span></a>
            </li>
            <li class="usa-nav__submenu-item">
              <a href=""><span>&lt;Navigation link&gt;</span></a>
            </li>
            <li class="usa-nav__submenu-item">
              <a href=""><span>&lt;Navigation link&gt;</span></a>
            </li>
          </ul>
        </li>
        <li class="usa-nav__primary-item">
          <a href="" class="usa-nav-link"><span>Additional Training</span></a>
        </li>
      </ul>
      <div class="usa-nav__secondary">
        <ul class="usa-nav__secondary-links">
          <li class="usa-nav__secondary-item">
            <a href="javascript:void(0);">
              Visit SmartPay website
            </a>
          </li>
          <li class="usa-nav__secondary-item">
            <a href="javascript:void(0);">
              Contact us
            </a>
          </li>
        </ul>
        <section aria-label="Search component">
          <form class="usa-search usa-search--small" role="search">
            <label class="usa-sr-only" for="search-field">Search</label>
            <input
              class="usa-input"
              id="search-field"
              type="search"
              name="search"
            />
            <button class="usa-button" type="submit">
              <img
                src="@/assets/images/usa-icons-bg/search--white.svg"
                class="usa-search__submit-icon"
                alt="Search"
              />
            </button>
          </form>
        </section>
      </div>
    </div>
  </nav>
  </header>

 </template>