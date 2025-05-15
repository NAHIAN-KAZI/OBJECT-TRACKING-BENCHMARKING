# 📐 Ground Truth Percent-to-Pixel Converter

This script converts bounding box coordinates from **percentage format** (relative to video resolution) to **absolute pixel values** in a ground truth JSON file.

---

## 🧾 Input Format

Each object in your JSON contains `sequence` data like:

```json
{
  "x": 25.0,       // Percent of width
  "y": 10.0,       // Percent of height
  "width": 20.0,   // Percent of width
  "height": 30.0   // Percent of height
}
```
The script converts these into absolute pixel values based on the given resolution.

## ⚙️ Configuration
Input file: groundtruth_all.json

Output file: main_groundtruth.json

Resolution used: 3840x2160 (modifiable)

## To change resolution, edit these lines in the script:

resolution_width = 3840
resolution_height = 2160

## 🚀 How to Use

python convert_groundtruth_to_pixels.py
After execution, a new file main_groundtruth.json will be created with all bounding boxes in pixel units.

## 📂 Files

├── groundtruth_all.json         # Input JSON (percent values)

├── main_groundtruth.json        # Output JSON (pixel values)

├── convert_groundtruth_to_pixels.py  # This script

└── README.md
