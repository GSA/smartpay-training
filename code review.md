# Pull Request (PR) Review Process

## Introduction

We perform a code review in order to ensure that the produced code meets the [Quality Assurance Surveillance Plan](https://github.com/GSA/SmartPay-RFQ/blob/main/RFQ.md#25-list-of-deliverables-with-quality-assurance-surveillance-plan-qasp), as defined in the [RFQ](https://github.com/GSA/SmartPay-RFQ/blob/main/RFQ.md):

| Deliverable | Performance Standard(s) | Acceptable Quality Level | Method of Assessment |
| :--- | :--- | :--- | :--- |
| Tested Code | Code delivered under the order must have substantial test code coverage | Minimum of 90% test coverage of all code. All areas of code are meaningfully tested | Combination of manual review and automated testing |
| Properly Styled Code | [18F Coding Styles](https://engineering.18f.gov/frontend/#js-style) Reference Guide | 0 linting errors and 0 warnings | Combination of manual review and automated testing |
| Accessible | [Web Content Accessibility Guidelines 2.1 AA standards](https://www.w3.org/TR/WCAG21/); [Section 508 Compliance](https://www.section508.gov/) | 0 errors reported using an automated scanner and 0 errors reported in manual testing | Combination of manual review and automated testing (such as [pa11y](https://github.com/pa11y/pa11y)) |
| Deployed | Code must successfully build and deploy into staging environment | Successful build with a single command | Combination of manual review and automated testing |
| Documented | Summary of user stories completed every sprint. All dependencies are listed and the licenses are documented. Major functionality in the software/source code is documented. Individual methods are documented inline in a format that permits the use of tools such as JSDoc. System diagram is provided. Relevant security controls are documented and kept up to date. | Combination of manual review and automated testing, if available | Manual review |
| Secure | Code is free of known static and runtime vulnerabilities | Code submitted must be free of medium- and high-level static and dynamic security vulnerabilities | Tests free of medium- and high-level vulnerabilities from a static testing SaaS (such as Snyk or npm audit), from dynamic testing tools like OWASP ZAP (with documentation explaining any false positives), and ongoing code review informed by OWASP or similar standards |
| User research | Features and functionality developed should be driven by user insights and data analytics. Usability testing and other user research methods must be conducted at regular intervals throughout the development process (not just at the beginning or end). | Research plans and artifacts from usability testing and/or other research methods with end users are available at the end of every applicable sprint, in accordance with the Contractor’s research plan. | SmartPay will manually evaluate the artifacts based on a research plan provided by the contractor at the end of the second sprint and every applicable sprint thereafter. |

## Approach

It is important to approach a code review with the right frame of mind:

* Expect to ask lots of questions, not as an interrogation, but as an ongoing conversation, taking place between the government and the vendor.
* This is an Agile process and, as such, we treat the output of every sprint as a completed product. Security, accessibility, UX, tests, browser compatibility, etc. are not features, to be implemented in future sprints, but are things that we expect to be incorporated constantly, and completed at the end of each sprint.
* Remember that we are all learning together here. If you see something in the code that you don’t understand, it’s incumbent on you to say so. Maybe you know something that the developer doesn’t, maybe the developer knows something that you don’t, but they only way to find out is to ask.

## What we look for

Code reviews are about keeping code clean and limiting technical debt. We will look for things that increase technical debt or create an environment where technical debt can be introduced easily later.

### Untested code
We’re mostly going to look at new and changed code. For changed code, we’ll check the existing tests to make sure they’ve been updated if necessary. For new code, we’ll check that new tests were created.

### Does not contain secrets
We look to ensure that new and/or changed code does not contain secrets (account names, passwords, private keys, private hostnames, service endpoints and other confidential secrets).

### All logical paths are tested
Tests should cover all branches of logical decisions (e.g., `if / else` statements). We’ll check this by looking at a code coverage report that shows which lines were executed.

### Logical `AND` and `OR` operations are tested
Boolean operations can be somewhat-hidden logical paths. That is, a code coverage report will show every line is tested, but if boolean parts of a condition aren’t fully exercised, then some logical paths aren’t actually tested. We’ll check the tests to make sure they check both sides of logical operations.

### Test names describe what the tests are doing
Test names shouldn’t be overly technical. Ideally folks outside the development team can read the tests and know what’s passing and what’s failing. Test names should describe their behavior and not just be the name of the method being tested. We’ll check the test names to make sure they’re descriptive.

### Tests actually do what they’re supposed to
It’s easy to get to 100% code coverage without actually testing anything. We’ll look at the tests themselves to make sure they’re actually making the right assertions about the methods under test.

### Cyclomatic complexity, code depth, and method lengths are reasonable
We’ll use automated tools to perform [static source analysis](https://18f.gsa.gov/2016/10/04/what-is-static-source-analysis/). Anywhere the metrics are higher than what we’d generally like, we’ll look at the code itself to see if they make sense. We’re going to take a more in-depth look when we see a cyclomatic complexity above 10, a code depth above 5, or a method length above 25 lines.

### Opportunities to abstract and refactor
We’ll look for duplication in the code where it might make sense to break functionality into methods that can be reused.

### Unwieldy methods
Methods that are hard to reason through are also difficult to test, difficult to maintain, and prone to bugs. We’ll look out for methods that are complex, and suggest either refactoring that method or possibly breaking it into smaller pieces.

### Meaningful method and variable names
Method names should accurately reflect what the method does, and variable names should pretty clearly indicate what data they’re holding. Don’t be afraid of long names.  This also applies to method argument names. Ideally, someone looking at a method signature should be able to infer what it does without any additional documentation. We’ll look at these names to be sure they make sense. Good naming practices contribute to self-documenting code and reduce the manual documentation burden.

### Commented-out code
With good version control, it should be unnecessary to comment-out blocks of code — just delete them and get them from source history if you really need them again in the future.  Obviously it’s fine to comment out code while you’re developing, but once a feature is ready to merge, that former code should just be removed. We’ll be looking for these commented code blocks.

### Necessary comments
Comments in the code should describe complex bits of logic that aren’t easily glanceable — if someone new to the code can’t skim it and understand it, a comment might be in order. As we’re reviewing the code, if we find a bit we can’t understand quickly from the code and context, we’ll be looking for a comment that explains it. Comments should appear with the code they’re describing.

### Documented APIs
If code exposes a public API — whether that’s public methods on a class or HTTP endpoints in a REST service — those public methods should be documented.  We like documentation that can be extracted into some pretty markup (e.g., .NET’s XML comments, OAS, Swagger). We’ll check that any public-facing methods have useful documentation.

### Adherence to the project’s style guide
The project should adopt a code style guide and code should conform. Which guide the team chooses is less important than the consistency that comes from actually using it. We’ll check to make sure there’s a linter configured to check code style, that it passes, and that any exceptions are documented and explained in the code.

## What we’ll do

### We’ll be nitpicky
Code is a UX. Its users are other developers. In the spirit of user-centered design, we’ll be interested in the experience of future developers. We’ll look at code with this question in mind: “Would I want to work on this?”

### We’ll be thorough
After the work to write the code, it deserves for us to give it proper attention. We’ll take the time to carefully look over it and give our feedback.

### We’ll ask questions
If we’re not sure about something, we’ll ask for clarity. We may ask a lot.

### We’ll be kind
We wouldn’t want anyone being mean to us because of an oversight, mistake, or just a different idea, and we’ll extend that courtesy to others. Code reviews are really conversations, not dictates. We’ll make suggestions rather than simply saying, “that’s wrong.”

## Checklist

We use this list when performing a code review to ensure that all tasks have been completed.

- [ ] review the pull request itself, to get oriented
	- [ ] read the description of the pull request, which should summarize the changes made
	- [ ] read through every task on the Scrum board that's encompassed by this pull request
	- [ ] read the description of the commits that comprise the pull request
- [ ] If changes were made in the UI (if not, skip):
  - [ ] If desired, run `docker system prune` to remove any unused docker images from previous code review.
  - [ ] Fetch the pull request for the sprint (e.g., `git fetch origin pull/{PR #}/head:sprint-{Sprint #}`), and then switch to that branch (e.g. `git checkout sprint-{Sprint #}`)
  - [ ] stand up the site locally, with `./docker-run.sh`
	- [ ] test all functionality in all major browsers, emphasizing the functionality that this pull request addresses
	- [ ] for internal Court functionality, perform the most thorough testing in Edge, though also test in Chrome and Firefox
	- [ ] for public-facing functionality, test in browsers consistent with [public browser use data](https://analytics.usa.gov/)
	- [ ] test in Mobile Safari and Mobile Chrome (or an emulator like Chrome DevTools), with the caveat that not all internal Court functionality will be necessary on these platforms
	- [ ] use an automated audit tool for code quality and practices (recommended: [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools/), aka [Lighthouse](https://chrome.google.com/webstore/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk))
		- [ ] look at efficiency of page loads, asset sizes, HTTP connection management, etc.
	- [ ] review for accessibility
		- [ ] use an automated audit tool, such as Chrome Audit or aXe
		- [ ] navigate site only with the keyboard
		- [ ] use VoiceOver or Narrator to navigate the site with audio only, with the display turned off
		- [ ] manually test anything that pa11y cannot test automatically (e.g., contrast of text over images)
- [ ] review static code analysis results in [the vendor’s DeepScan account](https://deepscan.io/dashboard/#view=project&tid=8976&pid=17137&bid=383813&prid=874192&subview=overview)
- [ ] examine OWASP ZAP output in `docs/`, to ensure that any errors are known to be false positives or have been previously declared to be acceptable
- [ ] skim all new code, in the context of existing code, [looking for problems](#what-we-look-for) (knowing that the vast majority of new code will be covered by tests)
- [ ] review all tests
	- [ ] look at code coverage of tests in GitHub Actions
	- [ ] methodically review all new tests for correctness, quality of naming
- [ ] determine what code isn’t tested, review that rigorously
- [ ] review documentation to ensure that it matches changes
	- [ ] user-visible changes (including API users like the IRS) are documented in CHANGELOG.md (which is linked from US Tax Court website).
- [ ] provide comments on the pull request on GitHub, as necessary
	- [ ] for comments that are specific to a particular line of code, comment on those specific lines

- [ ] for each feature-level bug (i.e., it’s working as designed, but designed wrong), open a new issue and put it in the backlog
