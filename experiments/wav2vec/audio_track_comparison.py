import torch
import torchaudio
import numpy as np
import moviepy.editor as mp
from transformers import Wav2Vec2Processor, Wav2Vec2Model

# Load the Wav2Vec2 processor and model
def define_model(device="cuda"):
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")
    model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base")
    model.eval().to(device)
    return model

# Preprocess audio arrays
def preprocess_audio(audio_array):
    audio_tensor = torch.tensor(audio_array.T)  # Transpose for torchaudio
    return audio_tensor

# Calculate similarity between two audio arrays
def calculate_audio_similarity(audio_array1, audio_array2, device='cuda'):
    audio_tensor1 = preprocess_audio(audio_array1)
    audio_tensor2 = preprocess_audio(audio_array2)

    # Extract embeddings
    with torch.no_grad():
        features1 = model(audio_tensor1.to(device)).last_hidden_state.mean(dim=1)
        features2 = model(audio_tensor2.to(device)).last_hidden_state.mean(dim=1)

    print(features1.shape, features2.shape)
    # Calculate similarity score (e.g., cosine similarity)
    similarity_scores = torch.nn.functional.cosine_similarity(features1, features2, dim=0)

    # Take the mean of the similarity scores
    similarity_score = similarity_scores.mean().item()
    return similarity_score

# Extract audio fragments from video
def extract_audio_fragments(video_path, start_time, end_time, frame_ps):
    video_clip = mp.VideoFileClip(video_path).subclip(start_time, end_time)
    audio_clip = video_clip.audio
    audio_array = audio_clip.to_soundarray(fps=frame_ps)
    audio_array = np.array(audio_array, dtype=np.float32)
    return audio_array

# Compare video fragments by getting similarity score
def compare_video_fragments(video1, video2, starttime1, 
                            endtime1, starttime2, endtime2, 
                            fps=16000, device='cuda'):
    fragment1 = extract_audio_fragments(video1, starttime1, endtime1, fps)
    fragment2 = extract_audio_fragments(video2, starttime2, endtime2, fps)
    similarity_score = calculate_audio_similarity(fragment1, fragment2)
    return similarity_score
