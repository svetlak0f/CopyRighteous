import pandas as pd
from datetime import timedelta
from qdrant_client.models import ScoredPoint

from ...schemas.video import MatchingData


def smooth_sequences(df, max_skip=1, min_length=2):
    sequences = []
    current_sequence = []
    skip_count = 0
    
    for i, row in df.iterrows():
        if not current_sequence:
            current_sequence.append(row.to_dict())
        else:
            if row['video_id'] == current_sequence[-1]['video_id']:
                current_sequence.append(row.to_dict())
                skip_count = 0
            else:
                if skip_count < max_skip:
                    skip_count += 1
                    current_sequence.append(row.to_dict())
                else:
                    filtered_sequence = [seq for seq in current_sequence if seq['video_id'] == current_sequence[0]['video_id']]
                    if len(filtered_sequence) >= min_length:
                        sequences.append(filtered_sequence)
                    current_sequence = [row.to_dict()]
                    skip_count = 0
    
    # Final check for the last sequence
    filtered_sequence = [seq for seq in current_sequence if seq['video_id'] == current_sequence[0]['video_id']]
    if len(filtered_sequence) >= min_length:
        sequences.append(filtered_sequence)
    
    return sequences

def frame_to_time(frame, frame_rate):
    return timedelta(seconds=frame/frame_rate)

# Calculate mean score for each sequence
def calculate_mean_score(sequence):
    mean_score = sum(item['score'] for item in sequence) / len(sequence)
    return mean_score

def process_matching_results(results: list[ScoredPoint], max_skip=10, min_length=100, frame_rate=10) -> list[MatchingData]:
    results = list(map(lambda x: x.model_dump(), results))

    df = pd.json_normalize(results)
    df["query_video_frame"] = list(range(len(df)))
    # Extract necessary columns
    df['frame'] = df['payload.frame']
    df['video_id'] = df['payload.video_id']

    # Sort by frame number
    df = df.sort_values(by='query_video_frame').reset_index(drop=True)

    sequences = smooth_sequences(df, max_skip, min_length)
    matching_results = list()
    for seq in sequences:
        mean_score = calculate_mean_score(seq)

        query_start_frame = seq[0]['query_video_frame']
        query_end_frame = seq[-1]['query_video_frame']
        query_start_time = frame_to_time(query_start_frame, frame_rate)
        query_end_time = frame_to_time(query_end_frame, frame_rate)

        match_start_frame = seq[0]['frame']
        match_end_frame = seq[-1]['frame']
        match_start_time = frame_to_time(match_start_frame, frame_rate)
        match_end_time = frame_to_time(match_end_frame, frame_rate)

        matching_results.append(MatchingData(
                                        query_start_frame=query_start_frame,
                                        query_end_frame=query_end_frame,
                                        query_start_time=str(query_start_time),
                                        query_end_time=str(query_end_time),

                                        match_video_id=seq[0]["video_id"],
                                        match_start_frame=match_start_frame,
                                        match_end_frame=match_end_frame,
                                        match_start_time=str(match_start_time),
                                        match_end_time=str(match_end_time),

                                        similarity_score=mean_score
                                    )
                                )
        
        return matching_results



    

