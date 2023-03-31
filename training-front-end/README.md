# GSA SmartPay® Training front end

```
npm install
npm run dev
```

## 🚀 Project Structure

This is an [Astro](https://astro.build) project. Astro is a framework designed primarily as a static site generator, but allows the use of UI components from frameworks like Vue and React. This project builds the dynamic elements using [Vue](https://vuejs.org) components.

```
/
├── public/
├── sass/
├── src/
│   └── assets/
│   └── components/
│       └── tests/
│   └── layouts/
│   └── pages/
│       └── home/
│       └── quiz/
│       └── training/
│       └── index.astro
├── gulpfile.cjs
└── package.json
```

Astro looks for `.astro` or `.md` files in the `src/pages/` directory. Each page is exposed as a route based on its file name.

There's nothing special about `src/components/`, but that's where we like to put any Astro and Vue components. Components intended as parent components for pages are placed in `src/layouts`. Again, there's nothing special about that directory, it's just a way to distinguish between small, reusable components, and those reresenting pages.

Any static assets, like images, can be placed in the `public/` directory. These will be exposed at the root url. Note that this can be problematic on cloud.pages where branch previews are mounted on a child path. This limits the usefulness of absolute urls while developing. Assets can also be placed in `src/assets` these are available as imports to astro components and will be packed correctly when the app builds. For me information, see [Astro Images documentation](https://docs.astro.build/en/guides/images/).

## 🚢 Deploying to Cloud.gov pages

Cloud.gov will look for a `package.json` file in the root of the repo (the parent of this directory), where it will find the `federalist` script is expects. That script will cd into this directory and run the build script in the `package.json` here. For more information see [Monorepos on Pages](https://cloud.gov/pages/documentation/monorepos-on-pages/).

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                | Action                                           |
| :--------------------- | :----------------------------------------------- |
| `npm install`          | Installs dependencies                            |
| `npm run dev`          | Starts local dev server at `localhost:3000`      |
| `npm run build`        | Build your production site to `../_site_/`       |
| `npm run preview`      | Preview your build locally, before deploying     |
| `npm run test:unit`    | Runs unit tests                                  |
| `npm run astro ...`    | Run CLI commands like `astro add`, `astro check` |
| `npm run astro --help` | Get help using the Astro CLI                     |

## 👀 Want to learn more about Astro?

Feel free to check [our documentation](https://docs.astro.build) or jump into their [Discord server](https://astro.build/chat).
