import json
import os
import numpy as np
from typing import Dict, List, Any

def convert_to_mot_format(tracking_path: str, gt_path: str, output_dir: str):
    """
    Convert tracking and ground truth JSON files to MOT format text files.
    
    MOT format:
    <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <x>, <y>, <z>
    
    Where:
    - frame: Frame number (1-based)
    - id: Object ID
    - bb_left: x-coordinate of the top-left corner of the bounding box
    - bb_top: y-coordinate of the top-left corner of the bounding box
    - bb_width: Width of the bounding box
    - bb_height: Height of the bounding box
    - conf: Confidence score (1 for ground truth, detection score for detections)
    - x, y, z: Not used in 2D tracking (set to -1)
    
    Args:
        tracking_path: Path to the tracking JSON file
        gt_path: Path to the ground truth JSON file
        output_dir: Directory to save output MOT text files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load JSON files
    with open(tracking_path, 'r') as f:
        tracking_data = json.load(f)
    
    with open(gt_path, 'r') as f:
        gt_data = json.load(f)
    
    # Process each video
    for tracking_video in tracking_data:
        video_path = tracking_video['video']
        video_name = os.path.basename(video_path).split('.')[0]
        
        # Find corresponding GT video
        gt_video = next((v for v in gt_data if v['video'] == video_path), None)
        if not gt_video:
            print(f"Warning: No ground truth data found for video {video_path}")
            continue
        
        # Create output file paths
        tracking_output = os.path.join(output_dir, f"{video_name}_tracking.txt")
        gt_output = os.path.join(output_dir, f"{video_name}_gt.txt")
        
        # Convert tracking data to MOT format
        tracking_lines = []
        
        # Process each object in tracking data
        for track_obj in tracking_video['box']:
            obj_id = track_obj['id']
            obj_class = track_obj['labels'][0]
            
            # Process each frame in the object's sequence
            for frame_data in track_obj['sequence']:
                if not frame_data.get('enabled', True):
                    continue  # Skip disabled frames
                
                frame_num = frame_data['frame']
                
                # Extract bounding box information
                x = frame_data['x']
                y = frame_data['y']
                width = frame_data['width']
                height = frame_data['height']
                
                # MOT format: <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <x>, <y>, <z>
                # For tracking predictions, set confidence to 1.0
                confidence = 1.0
                
                # Get class ID (1 for car, 2 for truck, etc.)
                class_id = 1 if obj_class.lower() == 'car' else 2  # Assuming car=1, truck=2
                
                # Create MOT format line
                line = f"{frame_num},{obj_id},{x},{y},{width},{height},{confidence},{class_id},-1,-1\n"
                tracking_lines.append((frame_num, line))
        
        # Sort by frame number
        tracking_lines.sort(key=lambda x: x[0])
        
        # Write tracking data to file
        with open(tracking_output, 'w') as f:
            for _, line in tracking_lines:
                f.write(line)
        
        # Convert ground truth data to MOT format
        gt_lines = []
        
        # Process each object in ground truth data
        for gt_obj in gt_video['box']:
            obj_id = gt_obj.get('id', -1)  # Use -1 if ID not present
            obj_class = gt_obj['labels'][0]
            
            # Process each frame in the object's sequence
            for frame_data in gt_obj['sequence']:
                if not frame_data.get('enabled', True):
                    continue  # Skip disabled frames
                
                frame_num = frame_data['frame']
                
                # Extract bounding box information
                x = frame_data['x']
                y = frame_data['y']
                width = frame_data['width']
                height = frame_data['height']
                
                # MOT format: <frame>, <id>, <bb_left>, <bb_top>, <bb_width>, <bb_height>, <conf>, <x>, <y>, <z>
                # For ground truth, set confidence to 1.0
                confidence = 1.0
                
                # Get class ID (1 for car, 2 for truck, etc.)
                class_id = 1 if obj_class.lower() == 'car' else 2  # Assuming car=1, truck=2
                
                # Create MOT format line
                line = f"{frame_num},{obj_id},{x},{y},{width},{height},{confidence},{class_id},-1,-1\n"
                gt_lines.append((frame_num, line))
        
        # Sort by frame number
        gt_lines.sort(key=lambda x: x[0])
        
        # Write ground truth data to file
        with open(gt_output, 'w') as f:
            for _, line in gt_lines:
                f.write(line)
        
        print(f"Converted tracking data saved to {tracking_output}")
        print(f"Converted ground truth data saved to {gt_output}")
        
        # Return the generated file paths
        return tracking_output, gt_output

def interpolate_mot_data(input_mot_path: str, output_mot_path: str, max_frame: int = None):
    """
    Interpolate MOT data to fill in missing frames for each object.
    
    Args:
        input_mot_path: Path to the input MOT format text file
        output_mot_path: Path to save the interpolated MOT data
        max_frame: Maximum frame number to interpolate up to (optional)
    """
    # Read input MOT file
    data = []
    with open(input_mot_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            data.append({
                'frame': int(parts[0]),
                'id': int(parts[1]),
                'x': float(parts[2]),
                'y': float(parts[3]),
                'width': float(parts[4]),
                'height': float(parts[5]),
                'conf': float(parts[6]),
                'class': int(parts[7]),
                'x3d': float(parts[8]),
                'y3d': float(parts[9])
            })
    
    # Group data by object ID
    objects = {}
    for entry in data:
        obj_id = entry['id']
        if obj_id not in objects:
            objects[obj_id] = []
        objects[obj_id].append(entry)
    
    # Sort each object's entries by frame
    for obj_id in objects:
        objects[obj_id].sort(key=lambda x: x['frame'])
    
    # If max_frame not specified, use the maximum frame number in the data
    if max_frame is None:
        max_frame = max(entry['frame'] for entry in data)
    
    # Interpolate missing frames for each object
    interpolated_data = []
    for obj_id, entries in objects.items():
        # Get the first and last frame for this object
        first_frame = entries[0]['frame']
        last_frame = entries[-1]['frame']
        
        # Dictionary to map frame numbers to entries
        frame_map = {entry['frame']: entry for entry in entries}
        
        # Interpolate for each frame
        for frame in range(first_frame, last_frame + 1):
            if frame in frame_map:
                # Frame exists, use the original data
                interpolated_data.append(frame_map[frame])
            else:
                # Find the closest frames before and after
                prev_frame = max([f for f in frame_map.keys() if f < frame], default=None)
                next_frame = min([f for f in frame_map.keys() if f > frame], default=None)
                
                if prev_frame is not None and next_frame is not None:
                    # Interpolate between prev and next frames
                    prev_entry = frame_map[prev_frame]
                    next_entry = frame_map[next_frame]
                    
                    # Linear interpolation factor
                    alpha = (frame - prev_frame) / (next_frame - prev_frame)
                    
                    # Interpolate values
                    x = prev_entry['x'] + alpha * (next_entry['x'] - prev_entry['x'])
                    y = prev_entry['y'] + alpha * (next_entry['y'] - prev_entry['y'])
                    width = prev_entry['width'] + alpha * (next_entry['width'] - prev_entry['width'])
                    height = prev_entry['height'] + alpha * (next_entry['height'] - prev_entry['height'])
                    
                    # Create interpolated entry
                    interpolated_data.append({
                        'frame': frame,
                        'id': obj_id,
                        'x': x,
                        'y': y,
                        'width': width,
                        'height': height,
                        'conf': prev_entry['conf'],  # Use same confidence
                        'class': prev_entry['class'],  # Use same class
                        'x3d': -1,
                        'y3d': -1
                    })
    
    # Sort by frame and then by ID
    interpolated_data.sort(key=lambda x: (x['frame'], x['id']))
    
    # Write interpolated data to output file
    with open(output_mot_path, 'w') as f:
        for entry in interpolated_data:
            line = f"{entry['frame']},{entry['id']},{entry['x']},{entry['y']},{entry['width']},{entry['height']},{entry['conf']},{entry['class']},{entry['x3d']},{entry['y3d']}\n"
            f.write(line)
    
    print(f"Interpolated MOT data saved to {output_mot_path}")
    print(f"Number of frames interpolated: {len(interpolated_data) - len(data)}")

if __name__ == "__main__":
    # File paths
    tracking_path = "filtered_tracking.json"
    gt_path = "filtered_groundtruth.json"
    output_dir = "mot_output"
    
    # Convert JSON to MOT format
    tracking_mot, gt_mot = convert_to_mot_format(tracking_path, gt_path, output_dir)
    
    # Optionally interpolate the MOT data to fill in missing frames
    # This is useful for smooth visualization and evaluation
    interpolated_tracking = os.path.join(output_dir, "interpolated_tracking.txt")
    interpolated_gt = os.path.join(output_dir, "interpolated_gt.txt")
    
    interpolate_mot_data(tracking_mot, interpolated_tracking)
    interpolate_mot_data(gt_mot, interpolated_gt)