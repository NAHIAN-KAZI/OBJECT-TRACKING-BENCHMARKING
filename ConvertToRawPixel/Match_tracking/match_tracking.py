import json
import numpy as np
from typing import Dict, List, Tuple, Any, Optional

def load_json_data(tracking_path: str, gt_path: str) -> Tuple[List[Dict], List[Dict]]:
    """Load tracking and ground truth JSON data."""
    with open(tracking_path, 'r') as f:
        tracking_data = json.load(f)
    
    with open(gt_path, 'r') as f:
        gt_data = json.load(f)
    
    return tracking_data, gt_data

def calculate_iou(box1: Dict, box2: Dict) -> float:
    """
    Calculate IoU (Intersection over Union) between two bounding boxes.
    Each box has x, y, width, height (where x,y is top-left corner)
    """
    # Calculate coordinates of box corners
    x1_1, y1_1 = box1['x'], box1['y']
    x2_1, y2_1 = x1_1 + box1['width'], y1_1 + box1['height']
    
    x1_2, y1_2 = box2['x'], box2['y']
    x2_2, y2_2 = x1_2 + box2['width'], y1_2 + box2['height']
    
    # Calculate intersection area
    x_left = max(x1_1, x1_2)
    y_top = max(y1_1, y1_2)
    x_right = min(x2_1, x2_2)
    y_bottom = min(y2_1, y2_2)
    
    if x_right < x_left or y_bottom < y_top:
        return 0.0  # No intersection
    
    intersection_area = (x_right - x_left) * (y_bottom - y_top)
    
    # Calculate areas of both boxes
    box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
    box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
    
    # Calculate IoU
    iou = intersection_area / float(box1_area + box2_area - intersection_area)
    return max(0.0, min(1.0, iou))  # Ensure IoU is between 0 and 1

def match_boxes(tracking_objects: List[Dict], gt_objects: List[Dict], 
                iou_threshold: float = 0.1) -> Tuple[Dict[int, int], List[int]]:
    """
    Match tracking objects to ground truth objects based on IoU.
    
    Args:
        tracking_objects: List of tracking objects
        gt_objects: List of ground truth objects
        iou_threshold: Minimum IoU to consider a match
        
    Returns:
        Tuple of (mapping from tracking ID to GT index, list of unmatched tracking IDs)
    """
    # Dictionary to store matched pairs (tracking_id -> gt_index)
    matching = {}
    
    # Set to keep track of already matched ground truth objects indices
    matched_gt_indices = set()
    
    # For each tracking object, find best matching GT object
    for track_obj in tracking_objects:
        track_id = track_obj['id']
        
        # Get first frame box from tracking sequence
        track_first_box = track_obj['sequence'][0]
        
        best_iou = iou_threshold  # Minimum threshold to consider a match
        best_gt_idx = None
        
        # Compare with all GT objects
        for gt_idx, gt_obj in enumerate(gt_objects):
            # Skip if this GT object is already matched
            if gt_idx in matched_gt_indices:
                continue
            
            # Check if labels match
            if track_obj['labels'][0] != gt_obj['labels'][0]:
                continue
                
            # Get first frame box from GT sequence
            gt_first_box = gt_obj['sequence'][0]
            
            # Check if frames are close enough (exact match might be too strict)
            if abs(track_first_box['frame'] - gt_first_box['frame']) > 5:
                continue
                
            # Calculate IoU
            iou = calculate_iou(track_first_box, gt_first_box)
            
            # Update best match if this IoU is better
            if iou > best_iou:
                best_iou = iou
                best_gt_idx = gt_idx
        
        # If a match is found, add to matching and mark GT as matched
        if best_gt_idx is not None:
            matching[track_id] = best_gt_idx
            matched_gt_indices.add(best_gt_idx)
    
    # Find unmatched tracking objects
    all_track_ids = {obj['id'] for obj in tracking_objects}
    matched_track_ids = set(matching.keys())
    unmatched_track_ids = list(all_track_ids - matched_track_ids)
    
    return matching, unmatched_track_ids

def analyze_tracking_data(tracking_path: str, gt_path: str) -> None:
    """
    Analyze tracking data against ground truth to find matches and extra detections.
    """
    # Load data
    tracking_data, gt_data = load_json_data(tracking_path, gt_path)
    
    # Process each video separately
    for tracking_video in tracking_data:
        video_path = tracking_video['video']
        print(f"\nAnalyzing video: {video_path}")
        
        # Find corresponding GT video
        gt_video = next((v for v in gt_data if v['video'] == video_path), None)
        if not gt_video:
            print(f"Warning: No ground truth data found for video {video_path}")
            continue
        
        tracking_objects = tracking_video['box']
        gt_objects = gt_video['box']
        
        # Match tracking objects to ground truth
        matches, unmatched_track_ids = match_boxes(tracking_objects, gt_objects)
        
        # Print matching results
        print(f"Found {len(matches)} matches between tracking and ground truth")
        for track_id, gt_idx in matches.items():
            track_obj = next(obj for obj in tracking_objects if obj['id'] == track_id)
            gt_obj = gt_objects[gt_idx]  # Using index instead of ID
            
            # For the GT object, use its index+1 as a display ID
            gt_display_id = gt_idx + 1
            
            # Calculate IoU for the first frame
            track_first_box = track_obj['sequence'][0]
            gt_first_box = gt_obj['sequence'][0]
            iou = calculate_iou(track_first_box, gt_first_box)
            
            print(f"Tracking ID {track_id} ({track_obj['labels'][0]}) matches Ground Truth #{gt_display_id} ({gt_obj['labels'][0]}) - IoU: {iou:.3f}")
        
        # Print unmatched (extra) tracking objects
        print(f"\nFound {len(unmatched_track_ids)} extra objects in tracking data:")
        for track_id in unmatched_track_ids:
            track_obj = next(obj for obj in tracking_objects if obj['id'] == track_id)
            print(f"Extra tracking object - ID: {track_id}, Label: {track_obj['labels'][0]}, "
                  f"First frame: {track_obj['sequence'][0]['frame']}, "
                  f"Position: ({track_obj['sequence'][0]['x']:.1f}, {track_obj['sequence'][0]['y']:.1f})")
        
        # Check for GT objects that weren't matched
        matched_gt_indices = set(matches.values())
        unmatched_gt_indices = set(range(len(gt_objects))) - matched_gt_indices
        
        print(f"\nGround truth objects with no matching tracking objects: {len(unmatched_gt_indices)}")
        for gt_idx in unmatched_gt_indices:
            gt_obj = gt_objects[gt_idx]
            gt_display_id = gt_idx + 1
            print(f"Unmatched GT object - #{gt_display_id}, Label: {gt_obj['labels'][0]}, "
                  f"First frame: {gt_obj['sequence'][0]['frame']}, "
                  f"Position: ({gt_obj['sequence'][0]['x']:.1f}, {gt_obj['sequence'][0]['y']:.1f})")

if __name__ == "__main__":
    # Replace these with your actual file paths
    tracking_json_path = "tracking.json"
    groundtruth_json_path = "main_groundtruth.json"
    
    analyze_tracking_data(tracking_json_path, groundtruth_json_path)