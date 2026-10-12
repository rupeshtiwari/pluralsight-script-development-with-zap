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

PROBE = "GLOBOxss7marker"
ALERT_NAME = "Globomantics unsafe reflection (custom rule)"


def scan(sas, msg, param, value):
    # Work on a copy, put our probe into the parameter, and send it.
    probe = msg.cloneRequest()
    sas.setParam(probe, param, PROBE)
    sas.sendAndReceive(probe, False, False)

    # If the probe comes back unchanged, the value was reflected without
    # encoding — raise the Globomantics alert on this parameter.
    if PROBE in probe.getResponseBody().toString():
        uri = probe.getRequestHeader().getURI().toString()
        # Raise the custom alert with the classic raiseAlert() API: it attaches
        # the alert to the scanned URL and persists it to ZAP's Alerts tab, the
        # report, and the API — so the finding can be verified and reused.
        sas.raiseAlert(
            2,                       # risk:       0 info 1 low 2 medium 3 high
            2,                       # confidence: 0 fp 1 low 2 medium 3 high
            ALERT_NAME,              # name
            "The parameter value is reflected in the HTML response without "
            "output encoding, so an attacker-supplied script would execute.",
            uri,                     # url the alert is raised against
            param,                   # the vulnerable parameter
            PROBE,                   # attack (the probe we sent)
            "",                      # otherInfo
            "HTML-encode the value before writing it into the response.",
            PROBE,                   # evidence (what we matched in the response)
            79,                      # CWE-79  (Cross-site Scripting)
            20,                      # WASC-20 (Improper Input Handling)
            probe)                   # the message the finding was found on


def scanNode(sas, msg):
    pass
