# GitHub Repository Presentation — Maintainer Checklist

## About (GitHub Settings; not a README field)
**Description:** Hands-on OWASP ZAP labs: injection, XSS, CSRF, JavaScript and Jython scripting, authenticated scans, API reports, and GitHub Actions security gates.

**Website:** Link to the published Pluralsight course when available; leave blank rather than inventing a course URL.

**Topics:** `owasp-zap`, `appsec`, `devsecops`, `security-testing`, `github-actions`, `fastapi`, `python`, `javascript`, `docker-compose`, `pluralsight`.

Set description and topics via the repository homepage **About → gear icon**. The connected GitHub integration used in this session offers no repository metadata write action; the About/Topics values here are **prepared, not applied**. To apply them, open the repository, select the About section's gear icon, paste the description, and add topics.

## Releases

**Current status: no published releases or tags.** A release requires a versioned, validated learner deliverable with complete runtime verification of all relevant demos, branch- and SHA-matched CI evidence, and an approved freeze checkpoint. Only then select **Releases → Draft a new release** in GitHub, create a semantically named tag (for example `v1.0.0` only when actually ready), describe the six demos and known limits, and publish with actual artifacts. Do not invent a release or publish an unverified demo package to fill the sidebar.

## Packages
The project consumes the official pinned OWASP ZAP image and uses Docker Compose. It does not publish a new software package. An empty **Packages** section is accurate; publish a package only when the course actually maintains an installable artifact.

## Public production notes
The temporary `docs/.author-instructions/` folder is visible to anyone because this repository is public. Move its contents to a separately access-controlled production repo before final Pluralsight submission, remove the public files, and assume the historic commits still contain those contents. Never store private recordings or secrets here.

## Future Skills Automation Contract
At project creation or migration, verify the latest available connector capabilities. When an authenticated integration exposes About/Topics/release actions, apply those fields directly with owner authorization. When it does not, do not claim success: provide the exact UI steps, keep release and package publishing contingent on genuine deliverables, and document the incomplete metadata checklist.
