# 📦 Tracking JSON Normalization to Pixel Coordinates

This script converts bounding box coordinates from **normalized format** (0–1 range) to **absolute pixel values** using the full resolution of the video.

---

## 🔁 Purpose

If your tracking predictions are normalized (e.g., values between 0 and 1 relative to video size), this script will **convert them to pixel values** based on the resolution of your source video.

---

## 🧾 Input Format

Each frame in your tracking JSON has this structure:

```json
{
  "x": 0.52,
  "y": 0.25,
  "width": 0.14,
  "height": 0.33
}
```
## After conversion, it becomes:

```
{
  "x": 1996.8,
  "y": 540.0,
  "width": 537.6,
  "height": 712.8
}
```
## ⚙️ Configuration
Input file: predictions_tracking_first_538_normalized.json

Output file: tracking.json

Video resolution used: 3840 x 2160

## To change the resolution, modify:


VIDEO_WIDTH = 3840
VIDEO_HEIGHT = 2160

## 🚀 How to Run
```
python convert_tracking_to_pixels.py
```
Once executed, it creates a new JSON file (tracking.json) with all bounding boxes in pixel units.

## 📂 Project Structure
```
├── predictions_tracking_first_538_normalized.json   # Input: normalized values
├── tracking.json                                    # Output: pixel values
├── convert_tracking_to_pixels.py                    # This script
└── README.md
```
## ✅ Output
You'll see a message like:
```
✅ Saved converted raw pixel JSON to: tracking.json
```

