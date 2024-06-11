from torchvision import models, transforms
import numpy as np
import torch
from tqdm import tqdm
from datetime import timedelta

from abc import ABC, abstractmethod

import cv2



class AbstractVideoVectorizer(ABC):
    @abstractmethod
    def process_video(self, video_path: str) -> np.ndarray:
        pass

    @abstractmethod
    def process_frame(self, frame) -> np.ndarray:
        pass
    


class ResnetVectorizer(AbstractVideoVectorizer):

    preprocess = transforms.Compose([
                                    transforms.ToTensor(),
                                    transforms.Resize(256),
                                    transforms.CenterCrop(224),
                                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                                ])
    
    def __init__(self, device: str, inference_batch_size: int = 16):
        self.device = torch.device(device)
        self.model = models.resnet152(pretrained=True)
        self.batch_size = inference_batch_size

        self.model.eval()
        self.model.to(self.device)


    def process_batch(self, batch):
        batch = batch.to(self.device)
        with torch.no_grad():
            output = self.model(batch).cpu().numpy()

        return output

    def process_video(self, video_path: str) -> tuple[np.ndarray, int, timedelta, int]:
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        seconds = round(total_frames / fps) 
        video_time = timedelta(seconds=seconds) 

        result = np.zeros((total_frames, 1000), dtype=np.float32)
        batch_frames = []

        for frame_num in tqdm(range(1, total_frames+1), desc='Processing video'):
            ret, frame = cap.read()
            input_tensor = self.preprocess(frame)
            batch_frames.append(input_tensor)
            batch = torch.stack(batch_frames)
            
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
        input_tensor = self.preprocess(frame).unsqueeze(0)
        output = self.process_batch(input_tensor)
        return output