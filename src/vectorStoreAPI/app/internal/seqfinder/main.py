import pandas as pd
from datetime import timedelta
from qdrant_client.models import ScoredPoint
from typing import Optional

from ...schemas.video import MatchingData, MatchingJobData


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

def process_matching_results(results: list[ScoredPoint], max_skip=12, min_length=100, frame_rate=10, input_offset: Optional[int] = None) -> list[MatchingData]:
    results = list(map(lambda x: x.model_dump(), results))

    df = pd.json_normalize(results)
    if input_offset:
        df["query_video_frame"] = list(range(input_offset, input_offset + len(df)))
    else:
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
        match_end_frame = match_start_frame + (query_end_frame - query_start_frame)
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



    

def generate_submission_dataframe(matching_data: MatchingData, id_piracy: str) -> pd.DataFrame:
    data = {
        "id_piracy": [id_piracy],
        "segment1": [f"{matching_data.query_start_frame // 10}-{matching_data.query_end_frame // 10}"],
        "id_licence": [matching_data.match_video_id],
        "segment2": [f"{matching_data.match_start_frame // 10}-{matching_data.match_end_frame // 10}"]
    }
    df = pd.DataFrame(data)
    return df


def convert_matching_job_to_sumbission(matching_job: MatchingJobData) -> pd.DataFrame:
    sumbmissions = list()
    for result in matching_job.results:
        sumbmissions.append(generate_submission_dataframe(result, id_piracy=matching_job.query_video_id))
    
    return pd.concat(sumbmissions, axis=0, ignore_index=True)