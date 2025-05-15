import json
import copy

def filter_tracking_data(tracking_path, gt_path, output_tracking_path, output_gt_path, remove_ids):
    """
    Filter out specified IDs from tracking.json and create new JSON files
    with proper ID mappings.
    
    Args:
        tracking_path: Path to the original tracking.json file
        gt_path: Path to the original groundtruth.json file
        output_tracking_path: Path to save the filtered tracking JSON
        output_gt_path: Path to save the filtered groundtruth JSON
        remove_ids: List of tracking IDs to remove
    """
    # Load the JSON files
    with open(tracking_path, 'r') as f:
        tracking_data = json.load(f)
    
    with open(gt_path, 'r') as f:
        gt_data = json.load(f)
    
    # Create deep copies to avoid modifying the original data
    new_tracking_data = copy.deepcopy(tracking_data)
    new_gt_data = copy.deepcopy(gt_data)
    
    # Create a mapping between tracking IDs and ground truth indices
    # Based on the mapping provided:
    id_mapping = {
        1: 1,  # tracking id 1 > ground truth #1
        2: 2,  # tracking id 2 > ground truth #2
        3: 3,  # tracking id 3 > ground truth #3
        4: 4,  # tracking id 4 > ground truth #4
        8: 5,  # tracking id 8 > ground truth #5
        9: 6,  # tracking id 9 > ground truth #6
        10: 7, # tracking id 10 > ground truth #7
        11: 8, # tracking id 11 > ground truth #8
        14: 9, # tracking id 14 > ground truth #9
        15: 10 # tracking id 15 > ground truth #10
    }
    
    # Process each video in the tracking data
    for video_idx, video in enumerate(new_tracking_data):
        # Filter the box list to remove entries with IDs in remove_ids
        filtered_boxes = []
        new_id_counter = 1  # Start with ID 1 for the filtered dataset
        
        # Get corresponding GT video
        gt_video = next((v for v in new_gt_data if v['video'] == video['video']), None)
        if not gt_video:
            print(f"Warning: No ground truth data found for video {video['video']}")
            continue
        
        # Dictionary to map old IDs to new IDs
        id_remap = {}
        
        # First, find all boxes to keep
        for box in video['box']:
            if box['id'] not in remove_ids:
                id_remap[box['id']] = new_id_counter
                new_id_counter += 1
        
        # Then create filtered boxes with new IDs
        for box in video['box']:
            if box['id'] not in remove_ids:
                # Create a copy of the box with the new ID
                new_box = copy.deepcopy(box)
                new_box['id'] = id_remap[box['id']]
                filtered_boxes.append(new_box)
        
        # Update the video with filtered boxes
        new_tracking_data[video_idx]['box'] = filtered_boxes
        
        # Now update the ground truth with consistent IDs based on the mapping
        new_gt_boxes = []
        gt_id_counter = 1  # Start with ID 1 for ground truth
        
        # Add an ID field to each ground truth box based on mapping
        for i, gt_box in enumerate(gt_video['box']):
            # Add 1 to i because the GT indices are 1-based in the mapping
            gt_idx = i + 1
            
            # Check if this GT box has a corresponding tracking box in our mapping
            if gt_idx in id_mapping.values():
                # Find the tracking ID that maps to this GT index
                tracking_id = next(k for k, v in id_mapping.items() if v == gt_idx)
                
                # Check if that tracking ID is in our filtered set
                if tracking_id in id_remap:
                    # Create a copy of the GT box 
                    new_gt_box = copy.deepcopy(gt_box)
                    # Add an ID field that matches the new tracking ID
                    new_gt_box['id'] = id_remap[tracking_id]
                    new_gt_boxes.append(new_gt_box)
        
        # Update the GT video with the new boxes
        for i, vid in enumerate(new_gt_data):
            if vid['video'] == gt_video['video']:
                new_gt_data[i]['box'] = new_gt_boxes
                break
    
    # Save the new JSON files
    with open(output_tracking_path, 'w') as f:
        json.dump(new_tracking_data, f, indent=2)
    
    with open(output_gt_path, 'w') as f:
        json.dump(new_gt_data, f, indent=2)
    
    print(f"Filtered tracking data saved to {output_tracking_path}")
    print(f"Filtered ground truth data saved to {output_gt_path}")
    print(f"Removed tracking IDs: {remove_ids}")
    print(f"Number of objects in new tracking data: {len(new_tracking_data[0]['box'])}")
    print(f"Number of objects in new ground truth data: {len(new_gt_data[0]['box'])}")

if __name__ == "__main__":
    # File paths
    tracking_path = "tracking.json"
    gt_path = "main_groundtruth.json"
    output_tracking_path = "filtered_tracking.json"
    output_gt_path = "filtered_groundtruth.json"
    
    # IDs to remove from tracking.json
    remove_ids = [5, 6, 7, 12, 13, 16]
    
    # Run the filtering
    filter_tracking_data(tracking_path, gt_path, output_tracking_path, output_gt_path, remove_ids)