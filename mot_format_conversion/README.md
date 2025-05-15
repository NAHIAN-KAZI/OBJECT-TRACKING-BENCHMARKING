# 🎯 MOT Tracking Evaluation Pipeline

This project converts tracking and ground truth JSON files into **MOT Challenge format**, interpolates missing frames, and evaluates tracking performance with per-frame **precision**, **recall**, and **MOTA** metrics.

---

## 🧰 Components

### `main_MOTConvert.py`

- Converts `filtered_tracking.json` and `filtered_groundtruth.json` to MOT format.
- Saves outputs as:
  - `mot_output/<video_name>_tracking.txt`
  - `mot_output/<video_name>_gt.txt`
- Optionally interpolates missing frames for smoother evaluation.

### `Evaluation_tracking_Analysis.py`

- Loads the MOT format files.
- Computes frame-by-frame:
  - `True Positives (TP)`
  - `False Positives (FP)`
  - `False Negatives (FN)`
  - `Precision`, `Recall`, `MOTA`
- Saves:
  - 📊 `framewise_summary.csv`  
  - 📄 `framewise_summary.json`  
  - 🖼️ `metrics_over_time.png`

---

## 🚀 How to Use

1. **Convert to MOT Format**:
   ```bash
   python main_MOTConvert.py
   ```
2. **Run Evaluation**:
   ```bash
   python Evaluation_tracking_Analysis.py
   ```
## 📂 Output Directory Structure
```bash
   .
├── filtered_tracking.json
├── filtered_groundtruth.json
├── mot_output/
│   ├── <video>_tracking.txt
│   ├── <video>_gt.txt
│   ├── interpolated_tracking.txt
│   └── interpolated_gt.txt
├── mot_analysis_output/
│   ├── framewise_summary.csv
│   ├── framewise_summary.json
│   └── metrics_over_time.png
```

## 🧠 Notes

- Class IDs are mapped: car = 1, truck = 2

- 3D coordinates (x3d, y3d) are unused: set as -1

- Interpolation improves evaluation by filling gaps between tracked frames
