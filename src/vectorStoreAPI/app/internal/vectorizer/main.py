from torchvision import models, transforms
import numpy as np
import torch
from tqdm import tqdm

import cv2


model = models.resnet152(pretrained=True)
model.eval()

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def process_image(input_batch):

    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    with torch.no_grad():
        output = model(input_batch)

    return output

def process_video(video, batch_size):

    cap = cv2.VideoCapture(video)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    result = np.zeros((total_frames, 1000))
    batch_frames = []

    for frame_num in tqdm(range(1, total_frames+1), desc='Processing video'):
        
        ret, frame = cap.read()
        input_tensor = preprocess(frame)
        batch_frames.append(input_tensor)
        batch = torch.stack(batch_frames)
        
        if frame_num % batch_size == 0:
            tn = process_image(batch).cpu().numpy()
            result[frame_num-batch_size:min(frame_num, total_frames+1)] = tn
            batch_frames = []

    cap.release()

    return result