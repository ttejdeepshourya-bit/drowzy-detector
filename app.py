"""
=============================================================================
AI-Based Driver Drowsiness Detection System
Single-File Complete Solution: Backend + HTML + CSS + JavaScript
=============================================================================
Requirements satisfied:
1. Backend + Frontend (HTML, CSS, JS) combined in a SINGLE self-contained file.
2. 100% Free: ZERO paid APIs, zero third-party cloud accounts.
3. Fully compatible with:
   - Vercel Serverless Deployment (exports 'app' and 'handler' variables)
   - Local Python execution (run: 'py app.py' to launch local web app)
   - Real-time webcam face & eye landmark tracking using MediaPipe & EAR.
=============================================================================
"""

import sys
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

# Complete, self-contained Single-Page Application (HTML + CSS + JavaScript)
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>AI Driver Drowsiness Detection System</title>
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🚗</text></svg>">
  
  <!-- 100% Free MediaPipe CDN (No paid APIs) -->
  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js" crossorigin="anonymous"></script>

  <style>
    :root {
      --bg: #0b0f19;
      --card: #151d2f;
      --border: #23304a;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --success: #10b981;
      --danger: #ef4444;
      --warning: #f59e0b;
      --text: #f8fafc;
      --muted: #94a3b8;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    body {
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      padding: 1.5rem;
    }
    .container {
      max-width: 1300px;
      margin: 0 auto;
    }
    header {
      margin-bottom: 1.5rem;
    }
    h1 {
      font-size: 2rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      margin-bottom: 0.5rem;
    }
    .badges {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin-bottom: 1rem;
    }
    .badge {
      display: inline-block;
      padding: 0.25rem 0.75rem;
      font-size: 0.8rem;
      font-weight: 600;
      border-radius: 9999px;
      background: rgba(59, 130, 246, 0.15);
      color: #60a5fa;
      border: 1px solid rgba(59, 130, 246, 0.3);
    }
    .badge-aiml {
      background: rgba(168, 85, 247, 0.15);
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.3);
    }
    .badge-free {
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .disclaimer {
      background: #0f172a;
      border-left: 4px solid var(--warning);
      padding: 0.75rem 1rem;
      border-radius: 6px;
      font-size: 0.82rem;
      color: #cbd5e1;
      margin-bottom: 1.5rem;
    }

    /* 4 KPI Metric Cards */
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }
    .metric-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.2rem;
      text-align: center;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .metric-lbl {
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted);
      margin-bottom: 0.3rem;
    }
    .metric-val {
      font-size: 1.85rem;
      font-weight: 700;
    }

    /* Layout */
    .main-grid {
      display: grid;
      grid-template-columns: 320px 1fr;
      gap: 1.5rem;
    }
    @media (max-width: 900px) {
      .main-grid {
        grid-template-columns: 1fr;
      }
    }

    /* Controls Sidebar */
    .sidebar {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.2rem;
      height: fit-content;
    }
    .sidebar h2 {
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 1rem;
    }
    .btn-group {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.6rem;
      margin-bottom: 1.2rem;
    }
    button {
      padding: 0.75rem 1rem;
      border: none;
      border-radius: 8px;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .btn-start {
      background: var(--primary);
      color: white;
    }
    .btn-start:hover:not(:disabled) {
      background: var(--primary-hover);
    }
    .btn-stop {
      background: #334155;
      color: #e2e8f0;
    }
    .btn-stop:hover:not(:disabled) {
      background: #475569;
    }
    button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    .control-item {
      margin-bottom: 1.2rem;
    }
    .control-item label {
      display: flex;
      justify-content: space-between;
      font-size: 0.85rem;
      color: #cbd5e1;
      margin-bottom: 0.4rem;
    }
    .control-item input[type="range"] {
      width: 100%;
      accent-color: var(--primary);
    }
    .checkbox-item {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      font-size: 0.88rem;
      color: #cbd5e1;
      margin-bottom: 0.8rem;
      cursor: pointer;
    }
    .checkbox-item input {
      accent-color: var(--primary);
      width: 16px;
      height: 16px;
    }

    /* Video area & HUD */
    .video-container {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.2rem;
      position: relative;
    }
    .alert-banner {
      padding: 0.85rem 1.2rem;
      border-radius: 8px;
      font-size: 1.1rem;
      font-weight: 700;
      text-align: center;
      margin-bottom: 1rem;
      transition: all 0.3s;
    }
    .alert-banner.safe {
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .alert-banner.drowsy {
      background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%);
      color: white;
      border: 2px solid #ef4444;
      animation: pulse-red 1.2s infinite;
    }
    .alert-banner.idle {
      background: #0f172a;
      color: var(--muted);
      border: 1px solid var(--border);
    }
    @keyframes pulse-red {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.88; transform: scale(1.01); }
    }
    .canvas-wrapper {
      position: relative;
      width: 100%;
      max-width: 640px;
      margin: 0 auto;
      border-radius: 8px;
      overflow: hidden;
      background: #000;
      aspect-ratio: 4/3;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    video {
      display: none;
    }
    canvas {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transform: scaleX(-1);
    }
    .idle-placeholder {
      position: absolute;
      text-align: center;
      color: var(--muted);
      padding: 1rem;
    }

    /* Telemetry Chart & Event Logs */
    .telemetry-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.2rem;
      margin-top: 1.5rem;
    }
    .telemetry-card h3 {
      font-size: 1.05rem;
      font-weight: 600;
      margin-bottom: 0.8rem;
    }
    #earChart {
      width: 100%;
      height: 140px;
      background: #0b0f19;
      border-radius: 6px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      margin-top: 0.8rem;
    }
    th, td {
      padding: 0.5rem 0.8rem;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }
    th {
      color: var(--muted);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.75rem;
    }
  </style>
</head>
<body>

  <div class="container">
    <header>
      <h1>🚗 AI Driver Drowsiness Detection System</h1>
      <div class="badges">
        <span class="badge">Google MediaPipe Face Mesh</span>
        <span class="badge badge-aiml">Eye Aspect Ratio (EAR)</span>
        <span class="badge badge-free">100% Free & Open Source</span>
        <span class="badge">Zero Paid APIs</span>
      </div>
      <div class="disclaimer">
        <strong>⚠️ Educational Prototype Notice:</strong> This project is created for B.Tech CSE AIML academic presentation and demonstration purposes. It is not an automotive safety certified device. Never operate software while driving.
      </div>
    </header>

    <!-- 4 KPI Metrics -->
    <div class="metrics-grid">
      <div class="metric-card">
        <div class="metric-lbl">Eye State</div>
        <div class="metric-val" id="metricEye" style="color: var(--muted);">❓ IDLE</div>
      </div>
      <div class="metric-card">
        <div class="metric-lbl">Live Average EAR</div>
        <div class="metric-val" id="metricEar" style="color: var(--primary);">0.00</div>
      </div>
      <div class="metric-card">
        <div class="metric-lbl">Total Alerts</div>
        <div class="metric-val" id="metricAlerts" style="color: var(--text);">🚨 0</div>
      </div>
      <div class="metric-card">
        <div class="metric-lbl">System Status</div>
        <div class="metric-val" id="metricStatus" style="color: var(--muted);">STOPPED</div>
      </div>
    </div>

    <!-- Main Workspace -->
    <div class="main-grid">
      <!-- Sidebar Controls -->
      <div class="sidebar">
        <h2>🎛️ System Controls</h2>
        <div class="btn-group">
          <button id="btnStart" class="btn-start" onclick="startMonitoring()">▶️ Start</button>
          <button id="btnStop" class="btn-stop" onclick="stopMonitoring()" disabled>⏹️ Stop</button>
        </div>

        <div class="control-item">
          <label>
            <span>EAR Threshold</span>
            <span id="threshVal" style="color: var(--primary); font-weight:700;">0.24</span>
          </label>
          <input type="range" id="earThreshInput" min="0.15" max="0.35" step="0.01" value="0.24" oninput="updateSettings()">
        </div>

        <div class="control-item">
          <label>
            <span>Sustained Duration</span>
            <span id="durVal" style="color: var(--primary); font-weight:700;">1.5s</span>
          </label>
          <input type="range" id="durationInput" min="0.5" max="3.5" step="0.1" value="1.5" oninput="updateSettings()">
        </div>

        <label class="checkbox-item">
          <input type="checkbox" id="chkAudio" checked>
          <span>Enable Audio Alert Beep</span>
        </label>

        <label class="checkbox-item">
          <input type="checkbox" id="chkContours" checked>
          <span>Show Eye Landmarks</span>
        </label>

        <button onclick="resetCounters()" style="width: 100%; margin-top: 1rem; background: #1e293b; color: #94a3b8; font-size: 0.85rem;">
          🔄 Reset Alert Counter
        </button>

        <div style="margin-top: 1.5rem; font-size: 0.8rem; color: var(--muted); line-height: 1.4;">
          <strong>💡 Presentation Tip:</strong><br/>
          1. Click <strong>Start</strong> to activate webcam.<br/>
          2. Blink naturally: System stays <em>Normal</em>.<br/>
          3. Close eyes for &gt; 1.5s: System triggers <em>Drowsiness Alert</em> with warning sound!
        </div>
      </div>

      <!-- Live Video Feed -->
      <div class="video-container">
        <div id="statusBanner" class="alert-banner idle">
          ⏸️ System Idle. Click <strong>'▶️ Start'</strong> to begin real-time eye tracking.
        </div>

        <div class="canvas-wrapper">
          <video id="webcam" playsinline></video>
          <canvas id="outputCanvas" width="640" height="480"></canvas>
          <div id="idleMsg" class="idle-placeholder">
            <span style="font-size: 3rem;">📷</span><br/>
            Camera feed is inactive.<br/>Click <strong>'Start'</strong> in the sidebar.
          </div>
        </div>
      </div>
    </div>

    <!-- Live EAR Telemetry -->
    <div class="telemetry-card">
      <h3>📈 Live Eye Aspect Ratio (EAR) Telemetry Signal</h3>
      <canvas id="earChart"></canvas>
    </div>

    <!-- Session Alert History -->
    <div class="telemetry-card">
      <h3>📑 Drowsiness Alert Session Log</h3>
      <table id="logTable">
        <thead>
          <tr>
            <th>Time</th>
            <th>Event</th>
            <th>EAR</th>
            <th>Duration</th>
          </tr>
        </thead>
        <tbody id="logBody">
          <tr>
            <td colspan="4" style="color: var(--muted); text-align: center;">No alerts recorded yet.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <script>
    // State Variables
    let isRunning = false;
    let camera = null;
    let faceMesh = null;
    let earThreshold = 0.24;
    let timeThresholdSeconds = 1.5;
    let closedStartTime = null;
    let isDrowsy = false;
    let totalAlerts = 0;
    let earHistory = [];
    const MAX_HISTORY = 120;
    let lastBeepTime = 0;

    // MediaPipe 468 Landmark Indices for Eye Aspect Ratio:
    // [P1, P2, P3, P4, P5, P6]
    const LEFT_EYE = [33, 160, 158, 133, 153, 144];
    const RIGHT_EYE = [362, 385, 387, 263, 373, 380];
    const LEFT_CONTOUR = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246];
    const RIGHT_CONTOUR = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398];

    const videoElement = document.getElementById("webcam");
    const canvasElement = document.getElementById("outputCanvas");
    const canvasCtx = canvasElement.getContext("2d");
    const chartCanvas = document.getElementById("earChart");
    const chartCtx = chartCanvas.getContext("2d");

    // Free Web Audio Synthesizer (Zero external files, zero paid APIs)
    let audioCtx = null;
    function playBeep() {
      const now = Date.now();
      if (now - lastBeepTime < 900) return;
      lastBeepTime = now;

      try {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();

        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(1400, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.35);
      } catch (e) {
        console.warn("Audio warning beep notice:", e);
      }
    }

    function dist(p1, p2) {
      return Math.hypot((p1.x - p2.x) * 640, (p1.y - p2.y) * 480);
    }

    // Mathematical Eye Aspect Ratio (EAR) Formulation
    function calculateEAR(points, landmarks) {
      const p1 = landmarks[points[0]];
      const p2 = landmarks[points[1]];
      const p3 = landmarks[points[2]];
      const p4 = landmarks[points[3]];
      const p5 = landmarks[points[4]];
      const p6 = landmarks[points[5]];

      const v1 = dist(p2, p6);
      const v2 = dist(p3, p5);
      const h = dist(p1, p4);

      if (h === 0) return 0.0;
      return (v1 + v2) / (2.0 * h);
    }

    function updateSettings() {
      earThreshold = parseFloat(document.getElementById("earThreshInput").value);
      timeThresholdSeconds = parseFloat(document.getElementById("durationInput").value);
      document.getElementById("threshVal").innerText = earThreshold.toFixed(2);
      document.getElementById("durVal").innerText = timeThresholdSeconds.toFixed(1) + "s";
    }

    function resetCounters() {
      totalAlerts = 0;
      closedStartTime = null;
      isDrowsy = false;
      earHistory = [];
      document.getElementById("metricAlerts").innerText = "🚨 0";
      document.getElementById("logBody").innerHTML = '<tr><td colspan="4" style="color: var(--muted); text-align: center;">No alerts recorded yet.</td></tr>';
    }

    function onResults(results) {
      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

      const statusBanner = document.getElementById("statusBanner");
      const metricEye = document.getElementById("metricEye");
      const metricEar = document.getElementById("metricEar");
      const showContours = document.getElementById("chkContours").checked;
      const enableAudio = document.getElementById("chkAudio").checked;

      if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {
        const landmarks = results.multiFaceLandmarks[0];

        const earLeft = calculateEAR(LEFT_EYE, landmarks);
        const earRight = calculateEAR(RIGHT_EYE, landmarks);
        const earAvg = (earLeft + earRight) / 2.0;

        if (showContours) {
          drawContour(LEFT_CONTOUR, landmarks, isDrowsy ? "#ef4444" : "#10b981");
          drawContour(RIGHT_CONTOUR, landmarks, isDrowsy ? "#ef4444" : "#10b981");
        }

        const now = Date.now();
        if (earAvg < earThreshold) {
          // Eyes Closed
          metricEye.innerText = "😴 CLOSED";
          metricEye.style.color = "var(--danger)";

          if (!closedStartTime) closedStartTime = now;
          const closedDuration = (now - closedStartTime) / 1000.0;

          if (closedDuration >= timeThresholdSeconds) {
            if (!isDrowsy) {
              isDrowsy = true;
              totalAlerts++;
              document.getElementById("metricAlerts").innerText = `🚨 ${totalAlerts}`;
              logEvent("Drowsiness Alert", earAvg, closedDuration);
            }
            statusBanner.className = "alert-banner drowsy";
            statusBanner.innerText = "⚠️ WARNING: PROLONGED EYE CLOSURE DETECTED! WAKE UP!";
            if (enableAudio) playBeep();
          } else {
            statusBanner.className = "alert-banner safe";
            statusBanner.innerText = `Eyes closing (${closedDuration.toFixed(1)}s)...`;
          }
        } else {
          // Eyes Open
          closedStartTime = null;
          isDrowsy = false;
          metricEye.innerText = "👁️ OPEN";
          metricEye.style.color = "var(--success)";
          statusBanner.className = "alert-banner safe";
          statusBanner.innerText = "🟢 Driver Attentive — Normal Eye Aspect Ratio Detected.";
        }

        metricEar.innerText = earAvg.toFixed(2);
        metricEar.style.color = earAvg < earThreshold ? "var(--danger)" : "var(--primary)";
        earHistory.push(earAvg);
        if (earHistory.length > MAX_HISTORY) earHistory.shift();

      } else {
        metricEye.innerText = "❓ NO FACE";
        metricEye.style.color = "var(--muted)";
        metricEar.innerText = "0.00";
        statusBanner.className = "alert-banner safe";
        statusBanner.style.color = "var(--warning)";
        statusBanner.innerText = "⚠️ Notice: No face detected in frame. Please align with webcam.";
        closedStartTime = null;
        isDrowsy = false;
      }

      canvasCtx.restore();
      drawChart();
    }

    function drawContour(indices, landmarks, color) {
      canvasCtx.beginPath();
      canvasCtx.strokeStyle = color;
      canvasCtx.lineWidth = 2;
      for (let i = 0; i < indices.length; i++) {
        const pt = landmarks[indices[i]];
        const x = pt.x * canvasElement.width;
        const y = pt.y * canvasElement.height;
        if (i === 0) canvasCtx.moveTo(x, y);
        else canvasCtx.lineTo(x, y);
      }
      canvasCtx.closePath();
      canvasCtx.stroke();
    }

    function drawChart() {
      const w = chartCanvas.width = chartCanvas.offsetWidth;
      const h = chartCanvas.height = 140;
      chartCtx.clearRect(0, 0, w, h);

      // Threshold line
      const threshY = h - (earThreshold / 0.5) * h;
      chartCtx.strokeStyle = "#ef4444";
      chartCtx.setLineDash([4, 4]);
      chartCtx.lineWidth = 1.5;
      chartCtx.beginPath();
      chartCtx.moveTo(0, threshY);
      chartCtx.lineTo(w, threshY);
      chartCtx.stroke();
      chartCtx.setLineDash([]);

      // EAR curve
      if (earHistory.length < 2) return;
      chartCtx.strokeStyle = "#38bdf8";
      chartCtx.lineWidth = 2.5;
      chartCtx.beginPath();
      const step = w / (MAX_HISTORY - 1);
      for (let i = 0; i < earHistory.length; i++) {
        const x = i * step;
        const y = h - Math.min(1.0, (earHistory[i] / 0.5)) * h;
        if (i === 0) chartCtx.moveTo(x, y);
        else chartCtx.lineTo(x, y);
      }
      chartCtx.stroke();
    }

    function logEvent(event, ear, duration) {
      const timeStr = new Date().toLocaleTimeString();
      const tbody = document.getElementById("logBody");
      if (totalAlerts === 1) tbody.innerHTML = "";
      const row = `<tr>
        <td>${timeStr}</td>
        <td style="color: var(--danger); font-weight:700;">${event}</td>
        <td>${ear.toFixed(3)}</td>
        <td>${duration.toFixed(1)}s</td>
      </tr>`;
      tbody.insertAdjacentHTML("afterbegin", row);
    }

    async function startMonitoring() {
      document.getElementById("btnStart").disabled = true;
      document.getElementById("btnStop").disabled = false;
      document.getElementById("idleMsg").style.display = "none";
      document.getElementById("metricStatus").innerText = "ACTIVE";
      document.getElementById("metricStatus").style.color = "var(--success)";

      if (!faceMesh) {
        faceMesh = new FaceMesh({
          locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`
        });
        faceMesh.setOptions({
          maxNumFaces: 1,
          refineLandmarks: true,
          minDetectionConfidence: 0.5,
          minTrackingConfidence: 0.5
        });
        faceMesh.onResults(onResults);
      }

      camera = new Camera(videoElement, {
        onFrame: async () => {
          if (isRunning) await faceMesh.send({ image: videoElement });
        },
        width: 640,
        height: 480
      });

      isRunning = true;
      await camera.start();
    }

    function stopMonitoring() {
      isRunning = false;
      if (camera) camera.stop();
      document.getElementById("btnStart").disabled = false;
      document.getElementById("btnStop").disabled = true;
      document.getElementById("idleMsg").style.display = "block";
      document.getElementById("metricStatus").innerText = "STOPPED";
      document.getElementById("metricStatus").style.color = "var(--muted)";
      document.getElementById("statusBanner").className = "alert-banner idle";
      document.getElementById("statusBanner").innerText = "⏸️ System Idle. Click '▶️ Start' to resume monitoring.";
    }
  </script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Backend HTTP Request Handler (Vercel Serverless & Local Python Web Server)
# ---------------------------------------------------------------------------
class DrowsinessHTTPHandler(BaseHTTPRequestHandler):
    """
    HTTP Handler serving the self-contained AI Driver Drowsiness Detection System.
    Compatible with Vercel Serverless Functions and Python http.server.
    """

    def do_GET(self):
        """Serve the complete frontend on any GET request."""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode("utf-8"))

    def log_message(self, format, *args):
        """Clean custom console logger."""
        sys.stdout.write(f"[HTTP SERVER] {self.address_string()} - {format % args}\n")
        sys.stdout.flush()


# Top-level exports required by Vercel's Python Serverless Runtime
handler = DrowsinessHTTPHandler
app = DrowsinessHTTPHandler
application = DrowsinessHTTPHandler


# ---------------------------------------------------------------------------
# Local Execution Entrypoint (Run with: py app.py)
# ---------------------------------------------------------------------------
def run_local_server(port: int = 8000):
    """Starts the local web server and opens the browser."""
    server_address = ("", port)
    httpd = HTTPServer(server_address, DrowsinessHTTPHandler)
    url = f"http://localhost:{port}"

    print("=" * 70)
    print(" [AI] DRIVER DROWSINESS DETECTION SYSTEM ")
    print(" Complete Single-File Solution (Backend + HTML + CSS + JS)")
    print(" 100% Free - Zero Paid APIs - Google MediaPipe Face Mesh")
    print("=" * 70)
    print(f"[SUCCESS] Server active at: {url}")
    print("[INFO] Press Ctrl+C in this terminal to stop the server.")
    print("=" * 70)

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped by user.")
        httpd.server_close()


if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run_local_server(port=port)
