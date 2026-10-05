# Globomantics scripted authentication (ZAP "Authentication" script, Jython 2.7.2).
#
# WHAT IT DOES
#   Logs in to the Globomantics app by submitting the username to POST /login,
#   exactly as the app's own form does. ZAP then reuses the session cookie the
#   login returns for every follow-up request, so scans run as a logged-in user
#   (EO2c). The "logged-in indicator" you configure in the ZAP context (text
#   that appears only when authenticated, e.g. "Signed in as") tells ZAP the
#   session is valid.
#
# ZAP calls these functions:
#   authenticate(helper, paramsValues, credentials) -> the login HttpMessage
#   getRequiredParamsNames()     -> context params ZAP must supply
#   getOptionalParamsNames()     -> optional context params
#   getCredentialsParamsNames()  -> per-user credential fields

from org.apache.commons.httpclient import URI
from org.parosproxy.paros.network import HttpRequestHeader, HttpHeader
from java.net import URLEncoder
from java.lang import String
from jarray import array


def authenticate(helper, paramsValues, credentials):
    login_url = paramsValues.get("Login URL")
    username = credentials.getParam("username")
    print("[globo-auth] logging in as '%s' via %s" % (username, login_url))

    # Build the same form POST the Globomantics login form sends.
    body = "username=" + URLEncoder.encode(username, "UTF-8")
    msg = helper.prepareMessage()
    msg.setRequestHeader(
        HttpRequestHeader(HttpRequestHeader.POST, URI(login_url, False), HttpHeader.HTTP11)
    )
    msg.getRequestHeader().setHeader(
        HttpHeader.CONTENT_TYPE, "application/x-www-form-urlencoded"
    )
    msg.setRequestBody(body)
    msg.getRequestHeader().setContentLength(msg.getRequestBody().length())

    # Send it; ZAP captures the Set-Cookie session for later requests.
    helper.sendAndReceive(msg)
    print("[globo-auth] login response: %s" % msg.getResponseHeader().getStatusCode())
    return msg


def getRequiredParamsNames():
    return array(["Login URL"], String)


def getOptionalParamsNames():
    return array([], String)


def getCredentialsParamsNames():
    return array(["username"], String)
