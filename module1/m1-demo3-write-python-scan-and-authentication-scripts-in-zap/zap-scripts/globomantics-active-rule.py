# Globomantics custom active-scan rule (ZAP "Active Rules" script, Jython 2.7.2).
#
# WHAT IT DOES
#   For each parameter ZAP scans, it sends a distinctive probe value and checks
#   whether the response reflects that probe verbatim (no output encoding). If it
#   does, the rule raises a custom Globomantics alert. This is the kind of
#   targeted, house-specific check you write when a built-in rule does not cover
#   your app's exact concern (EO2b).
#
# ZAP calls these two functions:
#   scan(sas, msg, param, value)  - run the active checks against one parameter
#   scanNode(sas, msg)            - optional per-node hook (unused here)

# A probe that is easy to spot and unlikely to occur naturally in a response.
PROBE = "GLOBOxss7marker"

# Alert identity (shown in the Alerts tab and in ZAP reports).
ALERT_NAME = "Globomantics unsafe reflection (custom rule)"
DESC = ("The parameter value is reflected in the response without output "
        "encoding, so attacker-controlled markup reaches the page.")
SOLN = "Encode output for the context it lands in before rendering it."


def _raise(sas, param, url, msg):
    """Raise the custom alert, supporting both the classic and builder APIs."""
    # 1) Classic positional API (keyword-safe in Jython) — works on most helpers.
    try:
        sas.raiseAlert(2, 2, ALERT_NAME, DESC, url, param, PROBE, "", SOLN,
                       PROBE, 79, 20, msg)
        print("[globo-rule] alert raised via raiseAlert on param=%s" % param)
        return
    except Exception as e1:
        print("[globo-rule] raiseAlert unavailable (%s); trying newAlert()" % e1)
    # 2) Modern builder API. 'raise' is a Jython keyword, so call it via getattr.
    try:
        builder = (sas.newAlert()
                   .setRisk(2).setConfidence(2).setName(ALERT_NAME)
                   .setDescription(DESC).setParam(param).setAttack(PROBE)
                   .setEvidence(PROBE).setMessage(msg))
        getattr(builder, "raise")()
        print("[globo-rule] alert raised via newAlert on param=%s" % param)
    except Exception as e2:
        print("[globo-rule] FAILED to raise alert on param=%s: %s" % (param, e2))


def scan(sas, msg, param, value):
    probe_msg = msg.cloneRequest()
    sas.setParam(probe_msg, param, PROBE)
    sas.sendAndReceive(probe_msg, False, False)

    body = probe_msg.getResponseBody().toString()
    status = probe_msg.getResponseHeader().getStatusCode()
    found = PROBE in body
    print("[globo-rule] param=%s status=%s reflected=%s" % (param, status, found))

    if found:
        _raise(sas, param, probe_msg.getRequestHeader().getURI().toString(), probe_msg)


def scanNode(sas, msg):
    # No per-node behavior for this rule.
    pass
