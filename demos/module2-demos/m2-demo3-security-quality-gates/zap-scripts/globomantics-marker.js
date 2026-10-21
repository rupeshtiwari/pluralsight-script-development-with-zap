// Globomantics HTTP Sender script (GraalVM JavaScript).
//
// This is the SAME marker script authored in Module 1 Demo 2, carried forward here as a
// prerequisite: Module 2's quality-gate Automation Framework plan loads it by name so every
// request the gate scan sends is stamped with the marker header. It is NOT the artifact this
// clip teaches (that is ci/gate-plan.yaml); it ships ready so the gate never breaks.
//
// Authorized use only: exercised against the local Globomantics training app.

var MARKER_HEADER = "X-Globomantics-Marker";
var MARKER_VALUE  = "GLOBO-DEMO";
var CONSOLE_TAG   = "[globo-marker]";

var ScriptVars = Java.type("org.zaproxy.zap.extension.script.ScriptVars");

// Called just before ZAP sends a request. We add the marker header to the
// outbound message and write a fixed marker line to the console.
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
