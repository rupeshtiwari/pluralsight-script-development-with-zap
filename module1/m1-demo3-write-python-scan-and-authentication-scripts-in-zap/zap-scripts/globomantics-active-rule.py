# Globomantics custom active-scan rule (ZAP "Active Rules" script, Jython 2.7.2).
#
# WHAT IT DOES
#   For each parameter ZAP scans, it sends a distinctive probe value and checks
#   whether the response reflects that probe verbatim (no output encoding). If it
#   does, the rule raises a custom Globomantics alert (EO2b).
#
# ZAP calls:  scan(sas, msg, param, value)  and  scanNode(sas, msg)

PROBE = "GLOBOxss7marker"
ALERT_NAME = "Globomantics unsafe reflection (custom rule)"
DESC = ("The parameter value is reflected in the response without output "
        "encoding, so attacker-controlled markup reaches the page.")
SOLN = "Encode output for the context it lands in before rendering it."


def _log(line):
    # print() goes to the Script Console; also append to a file the author
    # tooling can read from the container for diagnosis.
    print(line)
    try:
        f = open("/tmp/globo-rule.log", "a")
        f.write(line + "\n")
        f.close()
    except Exception:
        pass


def _raise(sas, param, url, msg):
    try:
        sas.raiseAlert(2, 2, ALERT_NAME, DESC, url, param, PROBE, "", SOLN,
                       PROBE, 79, 20, msg)
        _log("[globo-rule] RAISED via raiseAlert param=%s" % param)
        return
    except Exception as e1:
        _log("[globo-rule] raiseAlert failed (%s); trying newAlert" % e1)
    try:
        b = (sas.newAlert().setRisk(2).setConfidence(2).setName(ALERT_NAME)
             .setDescription(DESC).setParam(param).setAttack(PROBE)
             .setEvidence(PROBE).setMessage(msg))
        getattr(b, "raise")()
        _log("[globo-rule] RAISED via newAlert param=%s" % param)
    except Exception as e2:
        _log("[globo-rule] BOTH raise paths failed param=%s: %s" % (param, e2))


def scan(sas, msg, param, value):
    probe_msg = msg.cloneRequest()
    sas.setParam(probe_msg, param, PROBE)
    sas.sendAndReceive(probe_msg, False, False)

    body = probe_msg.getResponseBody().toString()
    status = probe_msg.getResponseHeader().getStatusCode()
    found = PROBE in body
    _log("[globo-rule] param=%s status=%s reflected=%s len=%s"
         % (param, status, found, len(body)))

    if found:
        _raise(sas, param, probe_msg.getRequestHeader().getURI().toString(), probe_msg)


def scanNode(sas, msg):
    pass
