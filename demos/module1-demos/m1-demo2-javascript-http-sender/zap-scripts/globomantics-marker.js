// Globomantics HTTP Sender script (GraalVM JavaScript).
//
// This is an HTTP Sender script: ZAP runs it for every message it sends. The
// action here marks each outbound request with a fixed header and prints a
// named line to the Script Console, so a later Automation Framework run can
// call this same saved script.
//
// Authorized use only: exercised against the local Globomantics training app.

var MARKER_HEADER = "X-Globomantics-Marker";
var MARKER_VALUE  = "GLOBO-DEMO";
var CONSOLE_TAG   = "[globo-marker]";

// Called just before ZAP sends a request. We add the marker header to the
// outbound message and write a fixed marker line to the console.
var ScriptVars = Java.type("org.zaproxy.zap.extension.script.ScriptVars");

function sendingRequest(msg, initiator, helper) {
    msg.getRequestHeader().setHeader(MARKER_HEADER, MARKER_VALUE);
    var line = CONSOLE_TAG + " added " + MARKER_HEADER + ": " + MARKER_VALUE +
               " to " + msg.getRequestHeader().getURI().toString();
    print(line);
    // Keep the exact line ZAP printed, so it can be read back through the API.
    ScriptVars.setGlobalVar("globo.marker.lastLine", line);
}

// Called when ZAP receives a response. This demo only marks outbound
// requests, so there is nothing to do here.
function responseReceived(msg, initiator, helper) {
}
