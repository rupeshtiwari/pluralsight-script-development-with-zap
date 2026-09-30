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
#
# `sas` is a ScriptsActiveScanner; `msg` is the request being scanned.

# A probe that is easy to spot and unlikely to occur naturally in a response.
PROBE = "GLOBOxss7'\"<globo>"

# Alert identity (shown in the Alerts tab and in ZAP reports).
ALERT_NAME = "Globomantics unsafe reflection (custom rule)"


def scan(sas, msg, param, value):
    # Work on a copy so the original scanned message is left intact.
    probe_msg = msg.cloneRequest()

    # Put our probe into the parameter under test, then send it.
    sas.setParam(probe_msg, param, PROBE)
    sas.sendAndReceive(probe_msg, False, False)

    body = probe_msg.getResponseBody().toString()

    # If the probe comes back unchanged, the value was reflected without
    # encoding — raise the Globomantics alert on this parameter.
    if PROBE in body:
        alert = (
            sas.newAlert()
            .setRisk(2)          # 0 info, 1 low, 2 medium, 3 high
            .setConfidence(2)    # 0 fp, 1 low, 2 medium, 3 high
            .setName(ALERT_NAME)
            .setDescription(
                "The parameter value is reflected in the response without "
                "output encoding, so attacker-controlled markup reaches the page."
            )
            .setParam(param)
            .setAttack(PROBE)
            .setEvidence(PROBE)
            .setSolution("Encode output for the context it lands in before rendering it.")
            .setCweId(79)        # CWE-79 improper neutralization of input
            .setWascId(20)       # WASC-20 improper input handling
            .setMessage(probe_msg)
        )
        # `raise` is a Python keyword, so call the builder's raise() via getattr.
        getattr(alert, "raise")()


def scanNode(sas, msg):
    # No per-node behavior for this rule.
    pass
