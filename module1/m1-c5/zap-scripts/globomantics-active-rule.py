# Globomantics custom active-scan rule (ZAP "Active Rules" script, Jython 2.7.2).
#
# WHAT IT DOES
#   During an active scan it sends a distinctive probe into each parameter of a
#   page and checks whether the response reflects it verbatim (no output
#   encoding). On /account/profile the note value is written straight into the
#   HTML body, so an unencoded reflection there would EXECUTE as script — the
#   rule raises a named alert. This is the kind of targeted, house-specific
#   check you write when a built-in rule does not cover your app's exact
#   concern (EO2b).
#
# ZAP calls these two functions on an active-scan script:
#   scanNode(sas, msg)            - once per node (the page being scanned)
#   scan(sas, msg, param, value)  - once per injectable parameter ZAP discovers
#
#   We run the same check from BOTH: scan() handles a parameter ZAP hands us,
#   and scanNode() walks the node's own query parameters itself. Driving the
#   check from scanNode() keeps the rule self-contained — it does not depend on
#   ZAP's parameter discovery for this node — while scan() still works wherever
#   ZAP does enumerate parameters. ZAP de-duplicates identical alerts, so the
#   two paths never produce a double finding.
#
# AUTHOR NOTE (not visible in the recorded clip):
#   The rule also appends a one-line trace to /tmp/globo-rule-trace.log inside
#   the ZAP container at each decision point. That file is the author
#   preflight's ground truth: it proves the rule executed, which parameters it
#   checked, whether it detected the reflection, and whether the raise call
#   succeeded — independent of ZAP's alert store. The trace does nothing on
#   screen; the demo's proof artifact is the named alert in ZAP's Alerts tab.

import sys

PROBE = "GLOBOxss7marker"
ALERT_NAME = "Globomantics unsafe reflection (custom rule)"
DESCRIPTION = ("The parameter value is reflected in the HTML response without "
               "output encoding, so an attacker-supplied script would execute.")
TRACE = "/tmp/globo-rule-trace.log"


def _trace(line):
    # Best-effort author diagnostics. Never let tracing affect the scan.
    try:
        f = open(TRACE, "a")
        f.write(line + "\n")
        f.close()
    except Exception:
        pass


def _raise(sas, probe, param):
    uri = probe.getRequestHeader().getURI().toString()
    try:
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
        # 'raise' is a Python keyword, so call the builder's raise() via getattr.
        getattr(alert, "raise")()
        _trace("raised: newAlert().raise() param=%s" % param)
    except Exception as e:
        _trace("ERROR builder raise: %s" % repr(e))
        # Fall back to the classic many-arg raiseAlert if this build still has it.
        try:
            sas.raiseAlert(2, 2, ALERT_NAME, DESCRIPTION,
                           uri, param, PROBE, "", "", PROBE, 79, 20, probe)
            _trace("raised: classic sas.raiseAlert() param=%s" % param)
        except Exception as e2:
            _trace("ERROR classic raiseAlert: %s" % repr(e2))


def _err(where, param):
    # Trace the current exception. In Jython a Java Throwable may not be a
    # Python Exception, so callers use a bare except and we read exc_info here.
    try:
        _trace("ERROR %s param=%s: %s" % (where, param, repr(sys.exc_info()[1])))
    except Exception:
        _trace("ERROR %s param=%s: <unprintable>" % (where, param))


def _send(sas, probe):
    # Try the known sendAndReceive signatures; builds differ.
    try:
        sas.sendAndReceive(probe, False, False)
        return
    except:  # noqa: E722  (may be a Java Throwable)
        pass
    try:
        sas.sendAndReceive(probe, False)
        return
    except:  # noqa: E722
        pass
    sas.sendAndReceive(probe)


def _check(sas, msg, param):
    # Send our probe in this parameter and raise if it reflects unencoded.
    # Every step is traced and no throwable may escape, so the author preflight
    # can see exactly how far the rule got.
    try:
        probe = msg.cloneRequest()
    except:  # noqa: E722
        _err("clone", param); return
    try:
        sas.setParam(probe, param, PROBE)
    except:  # noqa: E722
        _err("setParam", param); return
    try:
        _send(sas, probe)
    except:  # noqa: E722
        _err("send", param); return
    try:
        code = probe.getResponseHeader().getStatusCode()
        body = probe.getResponseBody().toString()
    except:  # noqa: E722
        _err("readResponse", param); return
    if PROBE in body:
        _trace("reflected: param=%s http=%s" % (param, code))
        _raise(sas, probe, param)
    else:
        _trace("not-reflected: param=%s http=%s len=%d" % (param, code, len(body)))


def scan(sas, msg, param, value):
    _trace("scan: param=%s" % param)
    _check(sas, msg, param)


def scanNode(sas, msg):
    uri = msg.getRequestHeader().getURI().toString()
    _trace("scanNode: %s" % uri)
    try:
        params = msg.getUrlParams()
    except:  # noqa: E722
        _err("getUrlParams", "-")
        return
    for p in params:
        try:
            name = p.getName()
        except:  # noqa: E722
            _err("paramName", "-"); continue
        _trace("scanNode-check: param=%s" % name)
        _check(sas, msg, name)
