# Module 1, Test application behavior and extend ZAP

<div align="center">

![Security](https://img.shields.io/badge/Module_1-Application_Security-FF1675?style=for-the-badge)

<img src="../../docs/learner-diagrams/m1-demo1-architecture.svg" width="100%" alt="Focused application security tests and ZAP" />

<sub>Illustrative diagram · Generated using ChatGPT</sub>

</div>

The Globomantics Store has several distinct input boundaries. Maya must test them precisely, extend ZAP with custom scripts, and prove the scanner reached the authenticated code she intended to assess.

## What you will learn

**Demo 1, Validate injection, XSS and CSRF.** A focused ZAP policy detects three types of injection; context-specific payloads validate XSS, and two sessions reveal the CSRF token-binding failure. These findings are then reconciled with real application behavior *(EO1a, EO1b, EO1c)*.

[Open Module 1 Demo 1 →](m1-demo1-targeted-injection-xss-csrf/README.md)

**Demo 2, Extend ZAP with JavaScript.** Add a request marker through an HTTP Sender script, then verify the outbound message, live Script Console line and registered script state *(EO2a)*.

[Open Module 1 Demo 2 →](m1-demo2-javascript-http-sender/README.md)

**Demo 3, Scan an authenticated page with Python scripts.** Register a custom active-scan rule and separate scripted login, then prove that ZAP reaches the protected profile and raises the named custom alert *(EO2b, EO2c)*.

[Open Module 1 Demo 3 →](m1-demo3-python-scanning-authentication/README.md)

## Start an exercise

Prepare your Mac **once** using `./setup/setup-macos.sh` from the repository root. Follow the chosen demo README to select its starter branch, start its local app and ZAP with `./scripts/lab-up.sh` or `lab-reset.sh`, and run its four concept-named steps in order.

[← Course home](../../README.md)
