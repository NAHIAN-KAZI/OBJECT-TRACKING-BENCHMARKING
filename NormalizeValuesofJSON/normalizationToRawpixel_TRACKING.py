import json

# ---- Video dimensions (from your VideoInfo) ----
VIDEO_WIDTH = 3840
VIDEO_HEIGHT = 2160

# ---- Input and Output paths ----
input_json_path = "predictions_tracking_first_538_normalized.json"  # Change this if needed
output_json_path = "tracking.json"

# ---- Load existing JSON ----
with open(input_json_path, "r") as f:
    data = json.load(f)

# ---- Convert all boxes to raw pixel coordinates ----
for item in data:
    for box_entry in item["box"]:
        for frame_box in box_entry["sequence"]:
            frame_box["x"] = frame_box["x"] * VIDEO_WIDTH
            frame_box["y"] = frame_box["y"] * VIDEO_HEIGHT
            frame_box["width"] = frame_box["width"] * VIDEO_WIDTH
            frame_box["height"] = frame_box["height"] * VIDEO_HEIGHT

# ---- Save to new JSON ----
with open(output_json_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Saved converted raw pixel JSON to: {output_json_path}")
