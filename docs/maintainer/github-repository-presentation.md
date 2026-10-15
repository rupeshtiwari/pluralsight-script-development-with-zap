# GitHub Repository Presentation — Maintainer Checklist

## About (GitHub Settings; not a README field)
**Description:** Hands-on OWASP ZAP labs: injection, XSS, CSRF, JavaScript and Jython scripting, authenticated scans, API reports, and GitHub Actions security gates.

**Website:** Link to the published Pluralsight course when available; leave blank rather than inventing a course URL.

**Topics:** `owasp-zap`, `appsec`, `devsecops`, `security-testing`, `github-actions`, `fastapi`, `python`, `javascript`, `docker-compose`, `pluralsight`.

Set description and topics via the repository homepage **About → gear icon**. The connected GitHub integration used here cannot update these repository metadata fields.

## Releases
A GitHub release is a **versioned milestone**, not something to create simply to fill the sidebar. After every demo branch is validated on target machines, tag the intended frozen student release, attach final lab ZIPs if desired, and publish concise release notes from the GitHub **Releases → Draft a new release** UI. As of the organization pass, no release is being represented as published.

## Packages
The project consumes the official pinned OWASP ZAP image and uses Docker Compose. It does not publish a new software package. An empty **Packages** section is accurate; publish a package only when the course actually maintains an installable artifact.

## Public production notes
The temporary `docs/.author-instructions/` folder is visible to anyone because this repository is public. Move its contents to a separately access-controlled production repo before final Pluralsight submission, remove the public files, and assume the historic commits still contain those contents. Never store private recordings or secrets here.
