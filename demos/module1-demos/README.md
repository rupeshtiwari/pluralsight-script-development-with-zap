<div align="center">

# Module 1 · Validate and Extend ZAP

### Turn an alert into evidence, then extend the scanner to fit the application

![ZAP Scanning](https://img.shields.io/badge/Targeted_Scanning-EO1a--EO1c-0284c7?style=for-the-badge)
![ZAP Scripting](https://img.shields.io/badge/Custom_Scripting-EO2a--EO2c-d946ef?style=for-the-badge)

<img src="../../docs/learner-diagrams/m1-demo1-architecture.svg" width="100%" alt="Targeted injection, XSS and CSRF verification architecture"/>

<sub>Illustrative architecture · Generated using ChatGPT</sub>

</div>

## Why Does This Matter?

A scan can call an endpoint vulnerable without proving the underlying behavior, and a default scanner may not understand the business-specific checks or authentication needed by your application. Maya Chen, the Globomantics security engineer, needs evidence she can defend: the exact parameter, the actual request and response, and a meaningful engineering decision.

## Learning Objectives You Can Practice

| Objective | What You Will Learn | Demo |
|---|---|---|
| **EO1a** | Configure specialized scanners for injection vulnerabilities (SQL, NoSQL, Command) | [Targeted Injection, XSS & CSRF](m1-demo1-targeted-injection-xss-csrf/README.md) |
| **EO1b** | Implement Cross-Site Scripting (XSS) validation with context-specific payloads | [Targeted Injection, XSS & CSRF](m1-demo1-targeted-injection-xss-csrf/README.md) |
| **EO1c** | Execute CSRF token bypass techniques for testing anti-CSRF protections | [Targeted Injection, XSS & CSRF](m1-demo1-targeted-injection-xss-csrf/README.md) |
| **EO2a** | Develop JavaScript scripts to extend ZAP functionality | [JavaScript HTTP Sender](m1-demo2-javascript-http-sender/README.md) |
| **EO2b** | Implement Python scripts for custom scanning rules | [Python Rule & Authentication](m1-demo3-python-scanning-authentication/README.md) |
| **EO2c** | Apply scripting for authentication sequence automation | [Python Rule & Authentication](m1-demo3-python-scanning-authentication/README.md) |

## Choose One Independent Exercise

<table>
<tr><th>Demo</th><th>Real Question</th><th>Evidence You Will Inspect</th><th>Guide</th></tr>
<tr><td><b>1 · Targeted vulnerabilities</b></td><td>Which alerts correspond to actual injection, XSS and CSRF behavior?</td><td>Targeted rule list, request/response, token controls and alert disposition</td><td><a href="m1-demo1-targeted-injection-xss-csrf/README.md">Open Demo 1 →</a></td></tr>
<tr><td><b>2 · JavaScript HTTP Sender</b></td><td>Did our custom hook really change an outgoing HTTP request?</td><td>Marker header, live Script Console line and enabled registration</td><td><a href="m1-demo2-javascript-http-sender/README.md">Open Demo 2 →</a></td></tr>
<tr><td><b>3 · Python scripts and login</b></td><td>Can a custom rule reliably test a profile that requires authentication?</td><td>Jython rule source, scripted login, 401-versus-200 and custom alert</td><td><a href="m1-demo3-python-scanning-authentication/README.md">Open Demo 3 →</a></td></tr>
</table>

## How To Start

From the repository root run `./setup/setup-macos.sh` once. Choose a demo's `m1-demoN-before` branch and follow that demo's README. Each page gives the exact folder, four concept-named commands, expected proof, preflight and cleanup. The `*-after` branch is your completed reference. No earlier demo must be executed first.

**Local interfaces:** Globomantics Store at <http://localhost:8000/> · ZAP GUI at <http://localhost:8080/zap/> · ZAP API/proxy at <http://localhost:8090/>.

All vulnerability testing is restricted to the supplied authorized Globomantics training application.

[← Return To Course Home](../../README.md)
