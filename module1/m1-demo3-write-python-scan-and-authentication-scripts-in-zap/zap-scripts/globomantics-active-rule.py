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
#   scan(sas, msg, param, value)  - run the active check against one parameter
#   scanNode(sas, msg)            - optional per-node hook (unused here)

PROBE = "GLOBOxss7marker"
ALERT_NAME = "Globomantics unsafe reflection (custom rule)"


def scan(sas, msg, param, value):
    # Work on a copy, put our probe into the parameter, and send it.
    probe = msg.cloneRequest()
    sas.setParam(probe, param, PROBE)
    sas.sendAndReceive(probe, False, False)

    # DIAGNOSTIC (temporary): raise unconditionally to prove the rule runs and
    # its alert persists, isolating that from the reflection-detection path.
    if True:
        uri = probe.getRequestHeader().getURI().toString()
        print("[globo-rule] unsafe reflection on param '%s' at %s" % (param, uri))
        alert = (sas.newAlert()
                 .setRisk(2)          # 0 info, 1 low, 2 medium, 3 high
                 .setConfidence(2)    # 0 fp, 1 low, 2 medium, 3 high
                 .setName(ALERT_NAME)
                 .setDescription("The parameter value is reflected in the "
                                 "response without output encoding.")
                 .setParam(param)
                 .setAttack(PROBE)
                 .setEvidence(PROBE)
                 # Bind the alert to the scanned URL so it attaches to the site
                 # node and persists to the report / Alerts tab even though the
                 # probe message has no saved history reference.
                 .setUri(uri)
                 .setMessage(probe))
        # 'raise' is a Python keyword, so call the builder's raise() via getattr.
        getattr(alert, "raise")()


def scanNode(sas, msg):
    pass
