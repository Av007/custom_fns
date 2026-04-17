# Credit Display — ComfyUI Plugin

Shows the estimated cost of a video generation **before** you click Run, checks your live balance, and can optionally block the workflow if you can't afford it.

## Example output

```
Model     : Seedance 2.0 Fast — image/text→video (ByteDance)
Settings  : 480p 16:9  854×480  5.0s  ×1 run(s)
Per run   : 56.78 cr  ($0.27)
Total     : 56.78 cr  ($0.27)
Balance   : 1024.00 cr  ($4.85)
After run : 967.22 cr  ($4.58)
Status    : OK
Rate      : 211 cr = $1 USD
```

Updates instantly as you change any dropdown — no workflow run needed.

## Supported vendors

ByteDance (Seedance 2.0 / 1.x, Seedream), Kuaishou (Kling), Google (Veo 2/3), OpenAI (Sora 2), Pika, Minimax, Luma, Moonvalley, BFL (Flux), ElevenLabs.

Full price list: <https://docs.comfy.org/tutorials/partner-nodes/pricing>

## Install (server admin)

```
cd ComfyUI/custom_nodes
git clone https://github.com/Av007/custom_fns.git custom_fns
```

Restart ComfyUI. To update prices later: `git pull` in the same folder and restart.

## Add to a workflow

1. Right-click canvas → **Add Node → utils/cost → Credit Display**
2. Pick Model, Resolution, Aspect Ratio, Duration, Runs to match your paid node
3. Add **Show Text** (from ComfyUI Custom Scripts) and wire `cost_text` into its `text` input

## Notes

- Estimates only. Actual spend appears in **Settings → Credits → Credit History**.
- Balance is fetched from your local ComfyUI only — no third-party calls.
- Turn on **block\_if\_insufficient** to stop the workflow before any paid node runs.
- No external Python dependencies.

---

*Source: <https://github.com/Av007/custom_fns>*
