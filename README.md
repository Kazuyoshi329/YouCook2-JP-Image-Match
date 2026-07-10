# YouCook2-JP-Image-Match

We extend the original YouCook2-JP dataset and release a tool to create a multimodal dataset that includes image inputs. 
" 私たちは元のYouCook2-JPを拡張し、画像も入力とするためのマルチモーダルなデータセットの作成が可能なプログラムを公開します。 "

## Copyright and Disclaimer (著作権と免責事項)
We do not own the copyrights of the raw videos, English captions, and annotations in YouCook2. For the use of data in YouCook2, please refer to their official website for details on the dataset contents, usage, and copyright information.
(YouCook2の生動画、英語キャプション、注釈の著作権は当社が所有していません。データ利用の詳細については、YouCook2の公式ウェブサイトをご参照ください。)

---

## Repository Structure (リポジトリの構成)
- data/
  - youcook2_segments.json (Formatted from youcookii_annotations_trainval.json)
  - clip_input_annotations.json (Formatted from youcookii_translations_ja_train.json)
- src/
  - extract_frames.py (Extracts 10 frames per segment)
  - select_best_image.py (Selects the best keyframe using CLIP)

---

## Pipeline Overview (プログラムの説明)

The dataset generation pipeline consists of the following two steps:
(データセット生成の流れは、以下の2つのステップで構成されています。)

### Step 1: Frame Extraction (フレームの抽出)
Using src/extract_frames.py, the script extracts 10 frames evenly from each segment duration based on data/youcook2_segments.json.
(src/extract_frames.py を使用し、data/youcook2_segments.json に基づいて各セグメントの区間から均等に10枚のフレームを抽出します。)

- Input: data/youcook2_segments.json (Contains Youtube Video ID, Video URL, Time Stamp, ID., Sentence)

### Step 2: Keyframe Selection via CLIP (CLIPによる最適な1枚の選出)
Using src/select_best_image.py, OpenAI's CLIP model evaluates the 10 extracted frames and selects the most relevant single frame for each sentence. 
(src/select_best_image.py を使用し、CLIPモデルを用いて抽出された10枚の画像の中から英文に最も最適な1枚を選出します。)

The input for this step is data/clip_input_annotations.json (formatted from the YouCook2-JP dataset).
(このステップの入力は、YouCook2-JPデータを成形した data/clip_input_annotations.json です。)

- Output: A new path to the best frame will be appended to the data as "selected_image" (e.g., "~/GLd3aX16zBg/1_7.jpg").
(実行後、最適な画像のパスが "selected_image" としてデータに追加されます。)

---

## Important Notes (留意事項)

- Missing Videos (欠損動画について): While most videos can be downloaded from the official YouCook2 website, some videos are missing. You will need to download those missing videos directly from YouTube yourself.
  (多くの動画はYouCook2のサイトからダウンロードできますが、一部含まれていない動画があるため、不足分は自身でYouTubeからダウンロードする必要があります。)
- Video Formats (動画形式の混同について): The downloaded videos may contain both .mp4 and .mkv formats. Please ensure all videos are converted into .mp4 format before running the scripts.
  (ダウンロードした動画には .mp4 と .mkv が混在しているため、実行前に .mp4 形式に変換してください。)
- Path Configuration (パスの書き換えについて): Please modify the directory paths in the scripts to match your local environment where the downloaded videos are stored.
  (ダウンロードした動画を置くフォルダのパスに合わせて、プログラム内の該当箇所を適宜書き換えて利用してください。)

---

## References (参考文献)

@misc{YouCook2_JP_Image_Match,
  title        = {YouCook2-JP-Image-Match},
  author       = {○○○○},
  howpublished = {\url{https://github.com/~}},
  year         = {2026}
}
