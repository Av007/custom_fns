/**
 * CreditDisplay — live client-side recalculation.
 * Mirrors the pricing table from nodes.py so every widget change
 * immediately updates the node's text area without queuing.
 *
 * Pricing source: https://docs.comfy.org/tutorials/partner-nodes/pricing
 */

import { app } from "../../scripts/app.js";

// ── Constants ────────────────────────────────────────────────────────────────

const CREDITS_PER_USD = 211.0;
const PRICING_URL = "https://docs.comfy.org/tutorials/partner-nodes/pricing";

const RESOLUTION_DIMS = {
  "16:9": { "360p": [640, 360],   "480p": [854, 480],   "720p": [1280, 720],  "1080p": [1920, 1080] },
  "9:16": { "360p": [360, 640],   "480p": [480, 854],   "720p": [720, 1280],  "1080p": [1080, 1920] },
  "1:1":  { "360p": [360, 360],   "480p": [480, 480],   "720p": [720, 720],   "1080p": [1080, 1080] },
};

// Mirrors nodes.py PRICING — keep in sync when rates change.
const PRICING = {
  // ── ByteDance Seedance 2.x (Per K tokens) ──────────────────────────────
  "Seedance 2.0 Fast (i2v/t2v)":       { billing: "seedance2",  rate: 1.182,  label: "Seedance 2.0 Fast — image/text→video", vendor: "ByteDance" },
  "Seedance 2.0 Fast (v2v)":           { billing: "seedance2",  rate: 0.696,  label: "Seedance 2.0 Fast — video→video",      vendor: "ByteDance" },
  "Seedance 2.0 (i2v/t2v)":            { billing: "seedance2",  rate: 1.477,  label: "Seedance 2.0 — image/text→video",      vendor: "ByteDance" },
  "Seedance 2.0 (v2v)":                { billing: "seedance2",  rate: 0.907,  label: "Seedance 2.0 — video→video",           vendor: "ByteDance" },
  // ── ByteDance Seedance 1.x (Per 1M tokens, estimated) ─────────────────
  "Seedance 1.0 Lite (i2v/t2v)":       { billing: "per_1m_tok", rate: 379.8,  label: "Seedance 1.0 Lite",                    vendor: "ByteDance" },
  "Seedance 1.0 Pro (i2v/t2v)":        { billing: "per_1m_tok", rate: 527.5,  label: "Seedance 1.0 Pro",                     vendor: "ByteDance" },
  "Seedance 1.0 Pro Fast (i2v/t2v)":   { billing: "per_1m_tok", rate: 211.0,  label: "Seedance 1.0 Pro Fast",                vendor: "ByteDance" },
  "Seedream 4.5 (t2v)":                { billing: "per_1m_tok", rate: 211.0,  label: "Seedream 4.5",                         vendor: "ByteDance" },
  "Seedance 1.5 Pro (no audio)":        { billing: "per_1m_tok", rate: 253.2,  label: "Seedance 1.5 Pro (no audio)",          vendor: "ByteDance" },
  "Seedance 1.5 Pro (with audio)":      { billing: "per_1m_tok", rate: 506.4,  label: "Seedance 1.5 Pro (with audio)",        vendor: "ByteDance" },
  // ── Kling ──────────────────────────────────────────────────────────────
  "Kling v2.1 Master Pro":              { billing: "per_run",    rate: 295.4,  label: "Kling v2.1 Master (Pro)",              vendor: "Kuaishou" },
  "Kling v2.1 Pro":                     { billing: "per_run",    rate: 103.39, label: "Kling v2.1 (Pro)",                     vendor: "Kuaishou" },
  "Kling v2.1 Standard":                { billing: "per_run",    rate: 59.08,  label: "Kling v2.1 (Standard)",                vendor: "Kuaishou" },
  "Kling v1.6 Pro":                     { billing: "per_run",    rate: 103.39, label: "Kling v1.6 (Pro)",                     vendor: "Kuaishou" },
  "Kling v1.6 Standard":                { billing: "per_run",    rate: 59.08,  label: "Kling v1.6 (Standard)",                vendor: "Kuaishou" },
  "Kling v2.6 Pro (no audio)":          { billing: "per_sec",    rate: 14.77,  label: "Kling v2.6 Pro (no audio)",            vendor: "Kuaishou" },
  "Kling v2.6 Pro (with audio)":        { billing: "per_sec",    rate: 29.54,  label: "Kling v2.6 Pro (with audio)",          vendor: "Kuaishou" },
  // ── Google Veo ─────────────────────────────────────────────────────────
  "Veo 2":                              { billing: "per_run",    rate: 105.5,  label: "Google Veo 2",                         vendor: "Google" },
  "Veo 3 Fast (no audio)":             { billing: "per_run",    rate: 168.8,  label: "Google Veo 3 Fast (no audio)",         vendor: "Google" },
  "Veo 3 Fast (with audio)":           { billing: "per_run",    rate: 253.2,  label: "Google Veo 3 Fast (with audio)",       vendor: "Google" },
  "Veo 3 (no audio)":                  { billing: "per_run",    rate: 337.6,  label: "Google Veo 3 (no audio)",              vendor: "Google" },
  "Veo 3 (with audio)":                { billing: "per_run",    rate: 675.2,  label: "Google Veo 3 (with audio)",            vendor: "Google" },
  // ── OpenAI Sora ────────────────────────────────────────────────────────
  "Sora 2 (720p)":                     { billing: "per_sec",    rate: 21.10,  label: "OpenAI Sora 2 — 720p",                 vendor: "OpenAI" },
  "Sora 2 Pro (720p)":                 { billing: "per_sec",    rate: 63.30,  label: "OpenAI Sora 2 Pro — 720p",             vendor: "OpenAI" },
  "Sora 2 Pro (1080p)":                { billing: "per_sec",    rate: 105.50, label: "OpenAI Sora 2 Pro — 1080p",            vendor: "OpenAI" },
  // ── Pika ───────────────────────────────────────────────────────────────
  "Pika 2.2 i2v 5s 720p":             { billing: "per_run",    rate: 42.2,   label: "Pika 2.2 — i2v 5s 720p",              vendor: "Pika" },
  "Pika 2.2 i2v 5s 1080p":            { billing: "per_run",    rate: 94.95,  label: "Pika 2.2 — i2v 5s 1080p",             vendor: "Pika" },
  "Pika 2.2 i2v 10s 720p":            { billing: "per_run",    rate: 126.6,  label: "Pika 2.2 — i2v 10s 720p",             vendor: "Pika" },
  "Pika 2.2 i2v 10s 1080p":           { billing: "per_run",    rate: 211.0,  label: "Pika 2.2 — i2v 10s 1080p",            vendor: "Pika" },
  // ── Minimax ────────────────────────────────────────────────────────────
  "Minimax Hailuo-02 6s 768P":         { billing: "per_run",    rate: 59.08,  label: "Minimax Hailuo-02 — 6s 768P",         vendor: "Minimax" },
  "Minimax Hailuo-02 6s 1080P":        { billing: "per_run",    rate: 103.39, label: "Minimax Hailuo-02 — 6s 1080P",        vendor: "Minimax" },
  // ── Luma ───────────────────────────────────────────────────────────────
  "Luma Ray 2":                        { billing: "per_sec",    rate: 1.93,   label: "Luma Ray 2",                           vendor: "Luma" },
  "Luma Ray Flash 2":                  { billing: "per_sec",    rate: 0.66,   label: "Luma Ray Flash 2",                     vendor: "Luma" },
  // ── Moonvalley ─────────────────────────────────────────────────────────
  "Moonvalley i2v 5s":                 { billing: "per_run",    rate: 316.5,  label: "Moonvalley — i2v 5s",                  vendor: "Moonvalley" },
  "Moonvalley i2v 10s":                { billing: "per_run",    rate: 633.0,  label: "Moonvalley — i2v 10s",                 vendor: "Moonvalley" },
  // ── BFL Flux ───────────────────────────────────────────────────────────
  "Flux Dev":                          { billing: "per_run",    rate: 5.28,   label: "BFL Flux Dev",                         vendor: "BFL" },
  "Flux Pro 1.1":                      { billing: "per_run",    rate: 8.44,   label: "BFL Flux Pro 1.1",                     vendor: "BFL" },
  "Flux Pro 1.1 Ultra":                { billing: "per_run",    rate: 12.66,  label: "BFL Flux Pro 1.1 Ultra",               vendor: "BFL" },
  "Flux Kontext Pro":                  { billing: "per_run",    rate: 8.44,   label: "BFL Flux Kontext Pro",                  vendor: "BFL" },
  "Flux Kontext Max":                  { billing: "per_run",    rate: 16.88,  label: "BFL Flux Kontext Max",                  vendor: "BFL" },
  // ── ElevenLabs ─────────────────────────────────────────────────────────
  "ElevenLabs TTS":                    { billing: "per_run",    rate: 50.64,  label: "ElevenLabs Text-to-Speech",            vendor: "ElevenLabs" },
};

// ── Calculation ──────────────────────────────────────────────────────────────

function seedance2Tokens(outDur, w, h, fps = 24, inDur = 0) {
  return (inDur + outDur) * h * w * fps / 1024.0;
}

function calcCost(model, resolution, aspectRatio, durationS, runs) {
  const entry = PRICING[model];
  if (!entry) return null;

  const dimGroup = RESOLUTION_DIMS[aspectRatio] ?? RESOLUTION_DIMS["16:9"];
  const [w, h]   = dimGroup[resolution] ?? [854, 480];

  let unitCredits;
  switch (entry.billing) {
    case "seedance2":
      unitCredits = seedance2Tokens(durationS, w, h) * entry.rate / 1000.0;
      break;
    case "per_1m_tok":
      unitCredits = seedance2Tokens(durationS, w, h) * entry.rate / 1_000_000.0;
      break;
    case "per_run":
      unitCredits = entry.rate;
      break;
    case "per_sec":
      unitCredits = entry.rate * durationS;
      break;
    default:
      return null;
  }

  const totalCredits = unitCredits * runs;
  const totalUsd     = totalCredits / CREDITS_PER_USD;
  return { unitCredits, totalCredits, totalUsd, w, h, label: entry.label, vendor: entry.vendor };
}

function formatText(model, resolution, aspectRatio, durationS, runs, checkBalance) {
  const r = calcCost(model, resolution, aspectRatio, durationS, runs);
  if (!r) return `Unknown model: ${model}`;
  const lines = [
    `Model     : ${r.label} (${r.vendor})`,
    `Settings  : ${resolution} ${aspectRatio}  ${r.w}×${r.h}  ${durationS}s  ×${runs} run(s)`,
    `Per run   : ${r.unitCredits.toFixed(2)} cr  ($${(r.unitCredits / CREDITS_PER_USD).toFixed(4)})`,
    `Total     : ${r.totalCredits.toFixed(2)} cr  ($${r.totalUsd.toFixed(4)})`,
  ];
  // Balance is fetched server-side at queue time; show a placeholder here.
  lines.push(
    checkBalance
      ? "Balance   : — (will be fetched when queued)"
      : "Balance   : — (check_balance is off)"
  );
  lines.push(`Rate      : 211 cr = $1 USD  |  ${PRICING_URL}`);
  return lines.join("\n");
}

// ── ComfyUI Extension ────────────────────────────────────────────────────────

app.registerExtension({
  name: "credit_tracker.CreditDisplay",

  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== "CreditDisplay") return;

    const proto = nodeType.prototype;
    const origCreated = proto.onNodeCreated;

    proto.onNodeCreated = function () {
      origCreated?.apply(this, arguments);

      const self = this;

      function getWidget(name) {
        return self.widgets?.find((w) => w.name === name);
      }

      // ── Upstream sync ──────────────────────────────────────────────────────
      // ByteDance widget order: 0=model 1=prompt 2=resolution 3=aspect_ratio 4=duration
      const UPSTREAM_IDX = { resolution: 2, aspect_ratio: 3, duration_s: 4 };

      // Track which source nodes have already been patched so we don't double-wrap.
      const _patched = new WeakSet();

      /** Return the node wired to our "trigger" input, or null. */
      function getSourceNode() {
        const inp  = self.inputs?.find((i) => i.name === "trigger");
        if (!inp?.link) return null;
        const link = app.graph.links[inp.link];
        return link ? app.graph.getNodeById(link.origin_id) : null;
      }

      /** Return the widget named `name` from the source node (name-first, then index). */
      function getUpstreamWidget(name) {
        const src = getSourceNode();
        if (!src) return undefined;
        return src.widgets?.find((w) => w.name === name) ?? src.widgets?.[UPSTREAM_IDX[name]];
      }

      /** Copy a value from the source node into our own widget. */
      function syncFromUpstream(name) {
        const up  = getUpstreamWidget(name);
        const own = getWidget(name);
        if (!up || !own) return;
        const val = name === "duration_s" ? parseFloat(up.value) : String(up.value);
        if (own.value !== val) own.value = val;
      }

      // ── Widget value interception ─────────────────────────────────────────
      // ComfyUI combo/dropdown widgets bypass `widget.callback` in many cases
      // and write directly to `widget.value`. We intercept the setter so any
      // write — through the UI, serialisation, or other extensions — triggers
      // an immediate recalculation.
      function interceptWidget(w) {
        if (w._ctIntercepted) return;  // already done
        w._ctIntercepted = true;

        let _v = w.value;
        Object.defineProperty(w, "value", {
          configurable: true,
          enumerable:   true,
          get() { return _v; },
          set(next) {
            if (next !== _v) {
              _v = next;
              // Defer by one tick so LiteGraph finishes its own bookkeeping first
              queueMicrotask(refresh);
            } else {
              _v = next;
            }
          },
        });
      }

      /** Intercept every widget on the source node (once per node). */
      function patchSourceNode() {
        const src = getSourceNode();
        if (!src || _patched.has(src)) return;
        for (const w of src.widgets ?? []) interceptWidget(w);
        _patched.add(src);
      }

      // ── Core refresh ──────────────────────────────────────────────────────
      function refresh() {
        // Lazily intercept source node widgets (handles on-load + new wires).
        patchSourceNode();

        syncFromUpstream("resolution");
        syncFromUpstream("aspect_ratio");
        syncFromUpstream("duration_s");

        const model        = getWidget("model")?.value;
        const resolution   = getWidget("resolution")?.value;
        const aspectRatio  = getWidget("aspect_ratio")?.value;
        const durationS    = parseFloat(getWidget("duration_s")?.value ?? 5);
        const runs         = parseInt(getWidget("runs")?.value ?? 1, 10);
        const checkBalance = getWidget("check_balance")?.value ?? true;

        if (!model || !resolution || !aspectRatio) return;

        const text = formatText(model, resolution, aspectRatio, durationS, runs, checkBalance);

        const textWidget = self.widgets?.find(
          (w) => w.type === "customtext" || w.name === "text"
        );
        if (textWidget) {
          textWidget.value = text;
          self.setDirtyCanvas(true, true);
        }
      }

      // Intercept our own widgets for local changes.
      for (const w of this.widgets ?? []) interceptWidget(w);

      // Re-sync whenever a connection is added or removed.
      const origConnChanged = self.onConnectionsChange;
      self.onConnectionsChange = function (...args) {
        origConnChanged?.apply(this, args);
        queueMicrotask(refresh);
      };

      // Initial render: microtask = immediate paint;
      // setTimeout = after workflow graph is fully loaded (connections resolved).
      queueMicrotask(refresh);
      setTimeout(refresh, 500);
    };
  },
});
