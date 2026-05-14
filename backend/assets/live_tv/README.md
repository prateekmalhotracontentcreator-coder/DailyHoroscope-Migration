# Live TV Assets

Place the Temple-provided Sai Baba source video in:

- `backend/assets/live_tv/sai_baba/`

Route note:

- Fixed player mount: public home page `(/)` via `Landing.jsx`
- Do not mount the panel on authenticated `/home`

Generate the website-ready asset and active manifest with:

```bash
python3 backend/scripts/generate_live_tv_video.py \
  --video-path backend/assets/live_tv/sai_baba/source.mp4 \
  --title "LIVE Sai Baba Arti | Om Sai Ram | EverydayHoroscope" \
  --description "Watch Sai Baba Arti live on EverydayHoroscope. Visit https://www.everydayhoroscope.in/live-sai-baba-arti" \
  --duration 3600 \
  --upload
```

Outputs land in:

- `backend/assets/live_tv/output/`

Active website metadata is written to:

- `backend/assets/live_tv/output/active_live_tv.json`
