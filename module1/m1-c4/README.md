# Write a JavaScript security script in ZAP

Use a JavaScript **HTTP Sender** script to add a request marker and print an identifiable console message. Prove the result in ZAP rather than relying only on a successful Terminal command.

> **Authorized target:** Only the local Globomantics training application. Do not use this workflow against systems without authorization.

## Applications and exact locations

| Application | Open / navigate | Why it is on screen |
|---|---|---|
| macOS Terminal | Repository root, then `module1/m1-c4` | Run the exact numbered commands and see the checks |
| ZAP GUI (Webswing) | [http://localhost:8080/zap/](http://localhost:8080/zap/) | Show the **Scripts** tree, script editor and Script Console; inspect HTTP History / request details when available |
| Local Globomantics app | [http://localhost:8000/](http://localhost:8000/) | Authorized target; the probe runs against its `/greet` endpoint through the ZAP proxy |
| Script source file | [zap-scripts/globomantics-marker.js](zap-scripts/globomantics-marker.js) | Exact source used by the demo; optionally open in VS Code **only for showing source** |

**Recording focus:** Terminal + ZAP GUI are sufficient. VS Code is optional for displaying source, not for executing it. The GUI runs on port **8080**; the ZAP API / proxy used by the Terminal scripts runs on port **8090**. Both refer to the same ZAP container. An HTTP request generated in Terminal may appear in ZAP's history; a console line must be checked in the **actual Script Console**, not inferred from a Terminal expectation.

## Setup — before recording

From the **repository root**, install the environment once if not already installed:

```bash
./env-setup/setup-macos.sh
```

Then start Clip 4 from the repository root:

```bash
cd module1/m1-c4
./scripts/demo_up.sh
```

**Wait** for the healthy `Up` result. Open [ZAP GUI](http://localhost:8080/zap/) in a full-screen browser view and locate its **Scripts** area; keep a Terminal window ready at `module1/m1-c4`. Make Terminal text large and readable. Each command block below is run **in this directory**, not from the repository root. Use a clean full-screen recording; hide browser tabs and unnecessary UI.

> **Important choreography:** The committed JavaScript already exists on disk, and Step 1's helper **loads and enables that file via the ZAP API**. Steps 2–4 require that same enabled registration and do not silently reload it. The demonstrator does not need to create a second copy in the GUI or type code live. Show the loaded script in the ZAP Scripts tree/editor. Do not claim the GUI was used to author the file when the API loaded it. The ZAP script engine name is detected at runtime and can differ from the display string shown in examples.

## Learning-objective and proof map

| Step | Objective | Terminal proof | ZAP GUI proof |
|---|---|---|---|
| 1 | EO2a | Script loaded successfully | Script named `globomantics-marker` appears under HTTP Sender, with source visible |
| 2 | EO2a | Captured outgoing request includes marker | Request header shown in ZAP History/request view |
| 3 | EO2a | Fresh proxied request triggers the script | Actual `[globo-marker]` line in Script Console output |
| 4 | EO2a | Script registration type and enabled state | Registered script remains visible under HTTP Sender |

**Source reference (VS Code, Step 1):** `zap-scripts/globomantics-marker.js` — `sendingRequest()` lines 16–20, `responseReceived()` lines 24–25.

## Five-minute timing allocation

Recording budget: **5:00**.

| Segment | Duration | Running total |
|---------|----------|---------------|
| Setup and problem | 0:25 | 0:25 |
| Step 1 — read the source, load, show in ZAP | 1:40 | 2:05 |
| Step 2 — marker on a real request | 0:55 | 3:00 |
| Step 3 — live Script Console output | 0:50 | 3:50 |
| Step 4 — saved registration | 0:50 | 4:40 |
| Wrap-up | 0:20 | 5:00 |

## Step 1: Load and inspect the HTTP Sender script (EO2a)

**Goal:** Explain what the JavaScript hook does, then demonstrate that ZAP has loaded the exact script file.

**Application and location:** Start in **ZAP GUI** at [http://localhost:8080/zap/](http://localhost:8080/zap/) → **Scripts** → **HTTP Sender**. Then switch focus to **Terminal** in `module1/m1-c4`.

**Show before running (VS Code, source only):** Open [`zap-scripts/globomantics-marker.js`](zap-scripts/globomantics-marker.js) and focus on `sendingRequest(msg, initiator, helper)` (lines 16–20) — the `setHeader` call and the `print` statement — and the empty `responseReceived` (lines 24–25). This is the code to explain:

```javascript
var MARKER_HEADER = "X-Globomantics-Marker";
var MARKER_VALUE  = "GLOBO-DEMO";
var CONSOLE_TAG   = "[globo-marker]";

function sendingRequest(msg, initiator, helper) {
    msg.getRequestHeader().setHeader(MARKER_HEADER, MARKER_VALUE);
    print(CONSOLE_TAG + " added " + MARKER_HEADER + ": " + MARKER_VALUE +
          " to " + msg.getRequestHeader().getURI().toString());
}

function responseReceived(msg, initiator, helper) {
}
```

**Execute in Terminal:**

```bash
./scripts/demo_step.sh 1
```

**Expected Terminal evidence:** The command identifies `globomantics-marker`, the HTTP Sender type and detected JavaScript engine, the marker header `X-Globomantics-Marker: GLOBO-DEMO`, and a PASS confirming that it loaded in ZAP.

**Switch back to ZAP GUI:** Expand **Scripts → HTTP Sender**, select `globomantics-marker`, and show the source/editor and enabled state. The actual tree wording may depend on the ZAP GUI version.

**Explain to learners:** `sendingRequest` is invoked before ZAP sends a request. The header is attached to messages that pass through this active HTTP Sender script; it does **not** automatically modify requests made directly to the application without ZAP.

**Highlight:** `sendingRequest` → `setHeader` → loaded script name. Remove or move each callout as the focus changes.

**Proof:** Source file + successful load + script visible in ZAP. Do not stop at the Terminal PASS alone.

## Step 2: Prove the marker on an outbound request (EO2a)

**Goal:** Show a request really passed through ZAP and acquired the marker header.

**Application and location:** **Terminal** in `module1/m1-c4`; then **ZAP GUI** at [http://localhost:8080/zap/](http://localhost:8080/zap/) → **History** (or the equivalent request-message view).

**Execute in Terminal:**

```bash
./scripts/demo_step.sh 2
```

**Expected Terminal evidence:** A GET request to a unique `http://app:8000/greet?name=marker-...` URL and a captured request header:

```text
X-Globomantics-Marker: GLOBO-DEMO
```

**Switch to ZAP GUI:** Find the recent `/greet?name=marker-<unique-id>` request in **History**. Select it, open the **Request** message details, and show the `X-Globomantics-Marker` header. If the GUI history is crowded, locate the exact request by URL rather than selecting an unrelated message.

**Explain to learners:** The header in the outgoing HTTP message demonstrates execution of the script on real proxied traffic. Merely seeing the source file or script registration does not establish that it ran.

**Highlight:** The GET request line, then the exact marker header in the request. Show one focus at a time.

**Proof:** Terminal-captured request header; ideally the identical header in ZAP's selected request. If that GUI message cannot be located, the Terminal check remains the recorded proof—do not claim a GUI proof you did not show.

## Step 3: Verify actual Script Console output (EO2a)

**Goal:** Confirm the script reports what it changed, with a recognizable marker and URL.

**Application and location:** **ZAP GUI** at [http://localhost:8080/zap/](http://localhost:8080/zap/) → **Scripts** → select `globomantics-marker` → **Script Console** output pane. Then **Terminal** in `module1/m1-c4`.

**Before running:** Bring the ZAP Script Console into view and find or clear the old output where practical. This makes the next line clearly attributable to the new request.

**Execute in Terminal:**

```bash
./scripts/demo_step.sh 3
```

**Expected behavior:** The command sends a fresh, uniquely identified probe through ZAP. The script's `print` statement should emit a line like:

```text
[globo-marker] added X-Globomantics-Marker: GLOBO-DEMO to http://app:8000/greet?name=marker-<unique-id>
```

**Switch back to ZAP GUI:** Inspect the **actual** Script Console output and highlight the fresh `[globo-marker]` line. The exact URL in the line is determined by the request ZAP processed.

**Critical evidence distinction:** The Step 3 Terminal helper prints an **expected console-line format** and checks that the source contains `print` and a marked request exists. It does **not** independently retrieve the Script Console's live output. Only the visible ZAP console establishes that the log line was emitted.

**Explain to learners:** The fixed `[globo-marker]` prefix helps an operator distinguish this script's output from other console messages. The URL shows which request was marked.

**Highlight:** The fresh console output line—not the helper's `Console line (seen in ZAP's Script Console)` label.

**Proof:** Actual Script Console line in ZAP. Do not assert console-output verification solely from the Terminal PASS.

## Step 4: Confirm saved script identity and enabled state (EO2a)

**Goal:** Confirm the script has a stable registration that can be reused in later automation.

**Application and location:** **Terminal** in `module1/m1-c4`, then **ZAP GUI** → **Scripts → HTTP Sender**.

**Execute in Terminal:**

```bash
./scripts/demo_step.sh 4
```

**Expected Terminal evidence:**

| Registration field | Expected value |
|---|---|
| Name | `globomantics-marker` |
| Type | `httpsender` |
| Engine | Detected JavaScript engine; read the actual output |
| Enabled | `true` |
| Repository source path | `module1/m1-c4/zap-scripts/globomantics-marker.js` |
| Path mounted inside ZAP | `/zap-scripts/globomantics-marker.js` |

**Switch back to ZAP GUI:** Select the registered script under **HTTP Sender** and show its name and enabled state. The script is loaded by the API from the mounted path; the helper's displayed repository path is not a separate API verification of the registration path.

**Explain to learners:** A stable script name, correct script type and enabled state make the script reusable. This step verifies the registration in the running ZAP instance; it does **not** prove persistence after destroying or rebuilding the container.

**Highlight:** Script name, type, and enabled status. Do not introduce an Automation Framework configuration screen here.

**Proof:** The live ZAP registration returned by the helper plus the visible script entry in the GUI.

## Preflight and teardown (outside the four teaching beats)

From `module1/m1-c4`, run:

```bash
./scripts/preflight_check.sh
```

**Expected result:** `5 checks passed, 0 failed`. A plain-text log is saved under `module1/m1-c4/logs/preflight-*.log`. The five checks include readiness and the four scripted checks. Steps 2 and 3 each use a fresh request ID; stale history entries cannot satisfy their header check. **This does not replace visually confirming the Script Console output in Step 3.**

After recording, stop the demo stack:

```bash
./scripts/demo_down.sh
```

## Recording quality gate

- Preserve the exact order: **source and load → marked request → live console output → saved registration**
- Display **which application** is active for every beat; Terminal and ZAP GUI are the primary recording surfaces
- When showing a ZAP pane, include its full URL above or in the README: [http://localhost:8080/zap/](http://localhost:8080/zap/)
- Use full-screen capture, mobile-readable text, one callout target at a time, and clean cuts instead of typing corrections
- Do not claim manual GUI authoring when the script is actually loaded by `demo_step.sh 1`
- Do not claim that the script affects traffic bypassing ZAP or that the script survived a container rebuild
- Do not claim the Terminal preflight captures the live Script Console line
- Keep the demonstrated target limited to the local Globomantics training app

**End state:** The learner has seen the exact JavaScript hook, a modified real request, the emitted console message, and the enabled HTTP Sender registration.
