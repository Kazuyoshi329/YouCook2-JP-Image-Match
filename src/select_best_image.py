import os
import json
import torch
from PIL import Image
from torchvision import transforms
from transformers import CLIPProcessor, CLIPModel

device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

with open("~/clip_input_annotations.json", "r") as f:
    data = json.load(f)

output = []
video_counters = {}

for item in data:
    text = item["text"]
    reference = item["reference"]
    video_id = item["movie_name"]
    
    if video_id not in video_counters:
        video_counters[video_id] = 1
    index = video_counters[video_id]

    dir_path = f"/~/{video_id}" # 画像を保存したディレクトリを追記
    candidates = [f"{index}_{i}.jpg" for i in range(1, 11)] 
    candidate_paths = [os.path.join(dir_path, c) for c in candidates if os.path.exists(os.path.join(dir_path, c))]

    if not candidate_paths:
        print(f"[Warning] No images found for {video_id}, index {index}")
        video_counters[video_id] += 1
        continue

    # CLIPで類似度を計算
    images = [Image.open(img_path).convert("RGB") for img_path in candidate_paths]
    inputs = processor(text=[text]*len(images), images=images, return_tensors="pt", padding=True).to(device)
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    scores = logits_per_image.squeeze().tolist()

    # 最もスコアの高い画像を選択
    best_idx = scores.index(max(scores))
    best_image_path = os.path.abspath(candidate_paths[best_idx]) 

    output.append({
        "text": text,
        "movie_name": video_id,
        "reference": reference,
        "selected_image": best_image_path
    })

    video_counters[video_id] += 1

with open("~/", "w") as f: # 出力ファイルの指定
    json.dump(output, f, ensure_ascii=False, indent=2)
