import pandas as pd
import cv2
import os
import numpy as np
import torch
import json
import re

def read_segments_from_json(file_path, video_id):

    """
    JSONファイルから指定された動画IDの時間区間を取得

    :param file_path: JSONファイルのパス
    :param video_id: 対象の動画ID
    :return: 時間区間リスト（例: [[90, 102], [114, 127]]）
    """
    segments = []
    
    if not os.path.exists(file_path):
        print(f"Could not open file: {file_path}")
        return segments

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error: {e}")
        return segments

    for item in data:
        if item.get("Youtube Video ID") == video_id:
            time_stamp_str = item.get("Time Stamp")
            
            if time_stamp_str and isinstance(time_stamp_str, str):
                match = re.match(r"(\d+)-(\d+)", time_stamp_str)
                if match:
                    start = int(match.group(1))
                    end = int(match.group(2))
                    segments.append([start, end])
    
    return segments

def extract_frames_per_segment(video_path, output_dir, segments):
    """
    10枚の画像を抽出
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Could not open video file:", video_path)
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    os.makedirs(output_dir, exist_ok=True)

    for i, (start, end) in enumerate(segments):
        start_frame = int(start * fps)
        end_frame = int(end * fps)

        if end_frame >= total_frames:
            end_frame = total_frames - 1

        frame_indices = np.linspace(start_frame, end_frame, num=10, dtype=int)

        frame_count = 1
        for frame_idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if ret:
                # セグメント番号 (i+1) とフレーム番号 (frame_count) をファイル名に使用
                output_path = os.path.join(output_dir, f"{i+1}_{frame_count}.jpg")
                cv2.imwrite(output_path, frame)
                frame_count += 1
            else:
                print("Could not open video file:", video_path)

    cap.release()
    print(f"Frame extraction completed for video: {os.path.basename(video_path)}")

def process_all_videos_in_directory(video_dir, json_file, output_base_dir):

    if not os.path.isdir(video_dir):
        print(f"Video directory not found: {video_dir}")
        return

    print(f"Video directory: {video_dir}")
    print(f"Input file: {json_file}")
    print("-" * 50)
    
    for video_file in os.listdir(video_dir):
        if video_file.endswith(".mp4"):
            video_path = os.path.join(video_dir, video_file)
            video_id = os.path.splitext(video_file)[0]
            segments = read_segments_from_json(json_file, video_id)
            output_dir = os.path.join(output_base_dir, video_id)
            extract_frames_per_segment(video_path, output_dir, segments)
            
    print("-" * 50)
    print("Processing completed")

json_file = "~/youcook2_segments.json"
video_dir = "~/" # 動画を保存したディレクトリ
output_base_dir = "~/" # 画像の保存先

process_all_videos_in_directory(video_dir, json_file, output_base_dir)