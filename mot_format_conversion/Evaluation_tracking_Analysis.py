import pandas as pd
import matplotlib.pyplot as plt
import json
import os

def load_mot_file(file_path):
    """
    Load MOT file into a DataFrame.
    Columns: frame, id, x, y, w, h, conf, class, x3d, y3d
    """
    df = pd.read_csv(file_path, header=None)
    df.columns = ["frame", "id", "x", "y", "w", "h", "conf", "class", "x3d", "y3d"]
    return df

def evaluate_per_frame(gt_df, pred_df, max_frame=None):
    """
    Calculate precision, recall, and MOTA over time (frame-by-frame).
    """
    all_frames = sorted(gt_df['frame'].unique())
    results = []

    for frame in all_frames:
        gt_frame = gt_df[gt_df['frame'] == frame]
        pred_frame = pred_df[pred_df['frame'] == frame]

        TP = min(len(gt_frame), len(pred_frame))
        FP = max(0, len(pred_frame) - TP)
        FN = max(0, len(gt_frame) - TP)

        precision = TP / (TP + FP) if (TP + FP) else 0
        recall = TP / (TP + FN) if (TP + FN) else 0
        mota = 1 - (FN + FP) / len(gt_frame) if len(gt_frame) else 0

        results.append({
            "frame": frame,
            "TP": TP,
            "FP": FP,
            "FN": FN,
            "precision": precision,
            "recall": recall,
            "mota": mota
        })

    return pd.DataFrame(results)

def plot_metric_over_time(results_df, output_dir):
    """
    Save plots of precision, recall, and MOTA over time.
    """
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(12, 4))

    # Precision
    plt.plot(results_df["frame"], results_df["precision"], label="Precision", color="blue")
    # Recall
    plt.plot(results_df["frame"], results_df["recall"], label="Recall", color="orange")
    # MOTA
    plt.plot(results_df["frame"], results_df["mota"], label="MOTA", color="green")

    plt.xlabel("Frame")
    plt.ylabel("Score")
    plt.title("Tracking Metrics Over Time")
    plt.legend()
    plt.grid(True)

    plot_path = os.path.join(output_dir, "metrics_over_time.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"[✓] Saved plot: {plot_path}")

def save_summary_to_csv_json(results_df, output_dir):
    csv_path = os.path.join(output_dir, "framewise_summary.csv")
    json_path = os.path.join(output_dir, "framewise_summary.json")

    results_df.to_csv(csv_path, index=False)
    results_df.to_json(json_path, orient="records", indent=2)

    print(f"[✓] Saved CSV: {csv_path}")
    print(f"[✓] Saved JSON: {json_path}")

if __name__ == "__main__":
    tracking_file = "mot_output/6378f45d-vehicle-counting_tracking.txt"
    gt_file = "mot_output/6378f45d-vehicle-counting_gt.txt"
    output_dir = "mot_analysis_output"

    gt_df = load_mot_file(gt_file)
    pred_df = load_mot_file(tracking_file)

    results_df = evaluate_per_frame(gt_df, pred_df)
    plot_metric_over_time(results_df, output_dir)
    save_summary_to_csv_json(results_df, output_dir)
