# Globomantics custom active-scan rule (ZAP "Active Rules" script, Jython 2.7.2).
#
# WHAT IT DOES
#   During an active scan, for each query parameter on a page it sends a
#   distinctive probe and checks whether the response reflects it verbatim.
#   On /account/profile the note value is written into the HTML body without
#   output encoding, so the probe comes back unescaped — a strong indicator of
#   reflected XSS (the value is returned in a way that could let an attacker's
#   markup or script run). Confirming it actually executes is a separate,
#   context-specific step; this rule flags the unencoded reflection and raises
#   a named alert. It is the targeted, house-specific check you write when a
#   built-in rule does not cover your app's exact concern (EO2b).
#
# ZAP calls two functions on an active-scan script:
#   scanNode(sas, msg)            - once per page being scanned
#   scan(sas, msg, param, value)  - once per parameter ZAP decides to inject
#
#   We run the same check from both. The probe is built by cloning the request
#   and rewriting its query string, NOT by calling sas.setParam(): setParam()
#   needs the scanner's per-parameter state, which is only set up inside scan().
#   Editing the request directly works from scanNode() too, so the rule does
#   not depend on how ZAP chooses to enumerate parameters. ZAP de-duplicates
#   identical alerts, so running from both hooks never double-reports.
#
# AUTHOR NOTE (invisible in the recorded clip): the rule appends a short trace
# to /tmp/globo-rule-trace.log in the ZAP container so the author preflight can
# prove what the rule did. It has no effect on screen or on the scan.

import sys

PROBE = "GLOBOxss7marker"
ALERT_NAME = "Globomantics unsafe reflection (custom rule)"
DESCRIPTION = ("The parameter value is reflected in the HTML response without "
               "output encoding. Returning attacker-controlled input unescaped "
               "is a strong indicator of reflected XSS; whether injected script "
               "executes depends on the exact output context and should be "
               "confirmed with a context-specific payload.")
TRACE = "/tmp/globo-rule-trace.log"


def _trace(line):
    try:
        f = open(TRACE, "a")
        f.write(line + "\n")
        f.close()
    except Exception:
        pass


def _probe_request(msg, target):
    # Clone the request (keeps headers, including the authenticated session
    # cookie) and put our probe into the target parameter.
    probe = msg.cloneRequest()
    pairs = []
    for p in msg.getUrlParams():
        value = PROBE if p.getName() == target else p.getValue()
        pairs.append("%s=%s" % (p.getName(), value))
    uri = probe.getRequestHeader().getURI()
    uri.setQuery("&".join(pairs))
    probe.getRequestHeader().setURI(uri)
    return probe


def _raise(sas, probe, param):
    alert = (sas.newAlert()
             .setRisk(2)          # 0 info 1 low 2 medium 3 high
             .setConfidence(2)    # 0 fp 1 low 2 medium 3 high
             .setName(ALERT_NAME)
             .setDescription(DESCRIPTION)
             .setParam(param)
             .setAttack(PROBE)
             .setEvidence(PROBE)
             .setCweId(79)        # Cross-site Scripting
             .setWascId(20)       # Improper Input Handling
             .setMessage(probe))
    # 'raise' is a reserved word in Python, so call the builder's raise() method
    # indirectly.
    getattr(alert, "raise")()
    _trace("raised: param=%s" % param)


def _check(sas, msg, param):
    # A bare except keeps a per-parameter error from silently killing the rule,
    # and records it so the author preflight can see what happened.
    try:
        probe = _probe_request(msg, param)
        sas.sendAndReceive(probe, False, False)
        if PROBE in probe.getResponseBody().toString():
            _trace("reflected: param=%s" % param)
            _raise(sas, probe, param)
        else:
            _trace("not-reflected: param=%s" % param)
    except:  # noqa: E722  (Jython: a Java Throwable is not a Python Exception)
        _trace("ERROR param=%s: %s" % (param, repr(sys.exc_info()[1])))


def scan(sas, msg, param, value):
    _check(sas, msg, param)


def scanNode(sas, msg):
    for p in msg.getUrlParams():
        _check(sas, msg, p.getName())
