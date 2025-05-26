# 📊 Object Tracking Benchmarking & Evaluation Suite

This repository is a comprehensive pipeline for evaluating object tracking systems using annotated ground truth data, visual assets, and multiple utilities to convert, normalize, analyze, and score tracking outputs. It supports formats used in real-world video analysis and the **MOT Challenge evaluation protocol**.

---

## 📁 Project Overview

| Module | Description |
|--------|-------------|
| 🔍 **Tracking vs Ground Truth Analyzer** | Compares tracking outputs with annotated ground truth (label-sensitive IoU matching). |
| 📐 **Ground Truth Percent-to-Pixel Converter** | Converts % values in annotation files into absolute pixel coordinates. |
| 🧭 **Tracking JSON Normalization to Pixels** | Converts normalized (0–1) tracker outputs to absolute pixel coordinates. |
| 🎯 **MOT Tracking Evaluation Pipeline** | Converts data to MOT format and computes MOTA, Precision, Recall, TP/FP/FN over frames. |

---

## 📽️ Sample Video

A sample video is provided for benchmarking and testing the tracking pipeline.

⬇️ Download in Google Colab using:

```python
%cd {HOME}
!wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1pz68D1Gsx80MoPg-_q-IbEdESEmyVLm-' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1pz68D1Gsx80MoPg-_q-IbEdESEmyVLm-" -O vehicle-counting.mp4 && rm -rf /tmp/cookies.txt
```
# 📈 Evaluation Output
Matched/Unmatched objects

Frame-wise analysis

Per-object IoU reports

MOT Metrics: MOTA, Precision, Recall

# 🧠 Notes
Matching is label-sensitive (e.g., car to car)

All converters assume 3840×2160 resolution by default (modifiable in each script)

Ensure file names (tracking.json, main_groundtruth.json) match expected formats for each utility
