# 🔍 Tracking vs Ground Truth Analyzer

This py file is utility to **compare object tracking results with annotated ground truth data**. It helps identify:

- ✅ Matching tracked objects with ground truth
- ❌ Extra tracked objects (false positives)
- ❗ Missed ground truth objects (false negatives)

---

## 📂 File Structure

├── tracking.json # Tracking output file

├── main_groundtruth.json # Ground truth annotations

├── analyze_tracking.py # Main comparison script

└── README.md # Project documentation


---

## 🚀 How to Run

1. Make sure your tracking and ground truth JSON files are named `tracking.json` and `main_groundtruth.json`.
2. Run the analysis script using:

```bash
python analyze_tracking.py
```
## The script will output:

Matched IDs with IoU values

Unmatched tracking objects

Unmatched ground truth objects

## ⚙️ Matching Criteria
IoU threshold: 0.1 (configurable)

Frame difference tolerance: ±5 frames

Matching is label-sensitive: only compares objects with identical labels (e.g., car to car)

## 🛠️ Example Output
```
Analyzing video: /data/upload/1/6378f45d-vehicle-counting.mp4
Found 10 matches between tracking and ground truth
Tracking ID 1 (truck) matches Ground Truth #1 (truck) - IoU: 0.782

Found 6 extra objects in tracking data:
Extra tracking object - ID: 12, Label: car, First frame: 34, Position: (123.4, 567.8)

Ground truth objects with no matching tracking objects: 2
Unmatched GT object - #7, Label: car, First frame: 41, Position: (100.0, 222.2)
```
