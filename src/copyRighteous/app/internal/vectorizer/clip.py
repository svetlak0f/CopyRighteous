from torchvision import models, transforms
import numpy as np
import torch
from tqdm import tqdm
from datetime import timedelta

from PIL import Image
import requests
from transformers import AutoProcessor, AutoTokenizer, CLIPModel

from abc import ABC, abstractmethod
from .main import AbstractVideoVectorizer

import cv2


class ClipVectorizer(AbstractVideoVectorizer):

    
    def __init__(self, device: str, inference_batch_size: int = 16, embedding_size=512):
        self.device = torch.device(device)
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
        self.batch_size = inference_batch_size
        self.embedding_size = embedding_size

        self.processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.model.to(self.device)


    def process_batch(self, batch: list[np.ndarray]):
        inputs = self.processor(images=batch, return_tensors="pt").to(self.device)
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)

            return image_features.cpu().detach().numpy()

    def process_video(self, video_path: str) -> tuple[np.ndarray, int, timedelta, int]:
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        seconds = round(total_frames / fps) 
        video_time = timedelta(seconds=seconds) 

        result = np.zeros((total_frames, self.embedding_size), dtype=np.float32)
        batch_frames = []

        for frame_num in tqdm(range(1, total_frames+1), desc='Processing video'):
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR) 
            batch_frames.append(frame)
            batch = np.stack(batch_frames)
            
            if frame_num % self.batch_size == 0:
                tn = self.process_batch(batch)
                result[frame_num-self.batch_size:min(frame_num, total_frames+1)] = tn
                batch_frames = []

        # if len(batch_frames) != 0:
        #     tn = self.process_batch(batch)
        #     result[frame_num-self.batch_size:min(frame_num, total_frames+1)] = tn
        #     batch_frames = []

        cap.release()

        return result, total_frames, video_time, fps

    
    def process_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR) 
        inputs = self.processor(images=frame, return_tensors="pt").to(self.device)
        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)

            return image_features.cpu().detach().numpy()