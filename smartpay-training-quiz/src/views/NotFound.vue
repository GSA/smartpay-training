<template>
    <div  class="background flex-fill">
    <div class="usa-section">
        <div class="grid-container">
        <div class="grid-row grid-gap">
            <main class="" id="main-content">
            <div class="usa-prose">
                <h1>Page not found</h1>
                <p class="usa-intro">
                We’re sorry, we can’t find the page you’re looking for. It might
                have been removed, changed its name, or is otherwise unavailable.
                </p>
                <p>
                If you typed the URL directly, check your spelling and
                capitalization. Our URLs look like this:
                <strong>&lt;agency.gov/example-one&gt;</strong>.
                </p>
                <p>
                Visit our homepage for helpful tools and resources, or contact us
                and we’ll point you in the right direction.
                </p>
                <div class="margin-y-5">
                <ul class="usa-button-group">
                    <li class="usa-button-group__item">
                        <router-link to="/">Visit homepage</router-link>
                    </li>
                </ul>
                </div>
               
                <p class="text-base"><strong>Error code:</strong> 404</p>
            </div>
            </main>
        </div>
        </div>
    </div>
</div>
</template>