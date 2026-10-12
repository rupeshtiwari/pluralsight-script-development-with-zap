# Globomantics custom active-scan rule (ZAP "Active Rules" script, Jython 2.7.2).
#
# WHAT IT DOES
#   For each parameter ZAP scans, it sends a distinctive probe and checks whether
#   the response reflects it verbatim (no output encoding). On /account/profile
#   the note value is written straight into the HTML body, so an unencoded
#   reflection there would EXECUTE as script — the rule raises a named alert.
#   This is the kind of targeted, house-specific check you write when a built-in
#   rule does not cover your app's exact concern (EO2b).
#
# ZAP calls these two functions:
#   scan(sas, msg, param, value)  - run the active check against one parameter
#   scanNode(sas, msg)            - optional per-node hook (unused here)
#
# AUTHOR NOTE (not visible in the recorded clip):
#   The rule also appends a one-line trace to /tmp/globo-rule-trace.log inside
#   the ZAP container. That file is the author preflight's ground truth: it
#   proves the rule actually executed, detected the reflection, and either
#   raised its alert or hit an error — independent of ZAP's alert store. The
#   trace does nothing on screen; the demo's proof artifact is the Alerts tab.

PROBE = "GLOBOxss7marker"
ALERT_NAME = "Globomantics unsafe reflection (custom rule)"
TRACE = "/tmp/globo-rule-trace.log"


def _trace(line):
    # Best-effort author diagnostics. Never let tracing affect the scan.
    try:
        f = open(TRACE, "a")
        f.write(line + "\n")
        f.close()
    except Exception:
        pass


def scan(sas, msg, param, value):
    _trace("scan: param=%s value=%s" % (param, value))

    # Work on a copy, put our probe into the parameter, and send it.
    probe = msg.cloneRequest()
    sas.setParam(probe, param, PROBE)
    sas.sendAndReceive(probe, False, False)

    body = probe.getResponseBody().toString()
    if PROBE not in body:
        _trace("scan: param=%s not reflected" % param)
        return

    # Reflected without encoding -> raise the Globomantics alert on this param.
    uri = probe.getRequestHeader().getURI().toString()
    _trace("reflected: param=%s uri=%s" % (param, uri))

    # Raise on the probe we actually sent: it carries the request/response that
    # demonstrates the finding, and in an active scan its history reference is
    # what ZAP attaches the alert to.
    try:
        alert = (sas.newAlert()
                 .setRisk(2)          # 0 info 1 low 2 medium 3 high
                 .setConfidence(2)    # 0 fp 1 low 2 medium 3 high
                 .setName(ALERT_NAME)
                 .setDescription("The parameter value is reflected in the HTML "
                                 "response without output encoding, so an "
                                 "attacker-supplied script would execute.")
                 .setParam(param)
                 .setAttack(PROBE)
                 .setEvidence(PROBE)
                 .setCweId(79)        # Cross-site Scripting
                 .setWascId(20)       # Improper Input Handling
                 .setMessage(probe))
        # 'raise' is a Python keyword, so call the builder's raise() via getattr.
        getattr(alert, "raise")()
        _trace("raised: builder newAlert().raise() for param=%s" % param)
    except Exception as e:
        _trace("ERROR builder raise: %s" % repr(e))
        # Fall back to the classic many-arg raiseAlert in case this build still
        # supports it, so the alert is not lost if the builder path is rejected.
        try:
            sas.raiseAlert(2, 2, ALERT_NAME,
                           "Reflected without output encoding.",
                           uri, param, PROBE, "", "", PROBE, 79, 20, probe)
            _trace("raised: classic sas.raiseAlert() for param=%s" % param)
        except Exception as e2:
            _trace("ERROR classic raiseAlert: %s" % repr(e2))


def scanNode(sas, msg):
    pass
