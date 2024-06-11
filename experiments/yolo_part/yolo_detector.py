from dataclasses import dataclass
import cv2
import numpy as np
from tqdm import tqdm
from ultralytics import YOLO
from ..vectorizer import AbstractVideoVectorizer


@dataclass
class Segment:
    start: int
    length: int
    vectors: np.array


class YoloDetector:

    def __init__(self, video_vectorizer: AbstractVideoVectorizer,
                 model_path: str, device: str = "cuda", inference_batch_size: int = 16):
        self.video_vectorizer = video_vectorizer
        self.device = device
        self.model = YOLO(model_path)
        self.batch_size = inference_batch_size

    def process_video_frames(self, video_path):

        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        detections = []
        frames_batch = []
        write_segment = False

        for frame_num in tqdm(range(1, total_frames + 1)):

            ret, frame = cap.read()
            frames_batch.append(frame)

            if (frame_num % self.batch_size == 0) | (frame_num == total_frames):

                results = self.model.predict(frames_batch, verbose=False, device=self.device)

                for idx, segment in enumerate(results):
                    try:
                        x1, y1, x2, y2 = segment.boxes.xyxy[0]
                    except:
                        write_segment = False
                        continue

                    detected_area = frames_batch[idx][int(y1):int(y2), int(x1):int(x2)]
                    vector = self.video_vectorizer.process_frame(detected_area)

                    if write_segment:
                        detections[-1].vectors = np.concatenate((detections[-1].vectors, vector), axis=0)
                        detections[-1].length += 1
                    else:
                        detections.append(Segment(frame_num - self.batch_size + idx + 1, 0,
                                                  np.zeros((1, 1000), dtype=np.float32)))
                        detections[-1].vectors[0] = vector
                        write_segment = True

                frames_batch = []

        cap.release()

        return detections
