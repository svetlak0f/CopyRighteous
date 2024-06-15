import React, { useEffect, useState } from 'react';
import { Box, Typography } from '@mui/material';
import { getSpecificMatchingJobByJobID } from 'api/jobs';
import ReactPlayer from 'react-player'

interface VideoComparisonProps {
  queryVideoId: string;
  matchVideoId: string;
}

interface VideoData {
  startFrame: number;
  endFrame: number;
  startTime: string;
  endTime: string;
  videoUrl: string;
}

interface JobResults{
    query_start_frame: number;
    query_end_frame: number;
    query_start_time: string;
    query_end_time: string;
    match_video_id: string;
    match_start_frame: number;
    match_end_frame: number;
    match_start_time: string;
    match_end_time: string;
    similarity_score: number
}

interface JobData {
    job_id: string;
    query_video_id: string;
    status: string;
    started_at: string;
    finished_at: number;
    results: JobResults[]
}

const job_id = "87752e3b-ca05-461d-9cbc-602328e2d553"

const VideoComparison: React.FC = ({ }) => {
  const [queryVideoData, setQueryVideoData] = useState<VideoData | null>(null);
  const [matchVideoData, setMatchVideoData] = useState<VideoData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const search_job_metadata = await getSpecificMatchingJobByJobID(job_id)
        console.log(search_job_metadata)

        setQueryVideoData({
          startFrame: search_job_metadata.results[0].query_start_frame,
          endFrame: search_job_metadata.results[0].query_end_frame,
          startTime: search_job_metadata.results[0].query_start_time,
          endTime: search_job_metadata.results[0].query_end_time,
          videoUrl: `${search_job_metadata.results[0].query_video_id}.mp4`,
        });

        setMatchVideoData({
          startFrame: search_job_metadata.results[0].match_start_frame,
          endFrame: search_job_metadata.results[0].match_end_frame,
          startTime: search_job_metadata.results[0].match_start_time,
          endTime: search_job_metadata.results[0].match_end_time,
          videoUrl: `${search_job_metadata.results[0].match_video_id}.mp4`,
        });
      } catch (error) {
        console.error('Error fetching video data:', error);
      }
    };

    fetchData();
  }, []);

  const calculateSeekTime = (startTime: string, startFrame: number) => {
    const seconds = startFrame / 10; // Assuming 10 frames per second
    const startTimeInSeconds = parseInt(startTime.split(':')[2]);
    return startTimeInSeconds + seconds;
  };

  return (
    <Box>
      {queryVideoData && matchVideoData ? (
        <>
          <Typography variant="h5">Видео из запроса</Typography>
          <ReactPlayer controls url={`http://127.0.0.1:8000/media/videos/${queryVideoData.videoUrl}`}
            seek={calculateSeekTime(queryVideoData.startTime, queryVideoData.startFrame)} />
          <Typography>{`Время начала: ${queryVideoData.startTime}`}</Typography>
          <Typography>{`Время конца: ${queryVideoData.endTime}`}</Typography>

          <Typography variant="h5">Найденное видео</Typography>
          <ReactPlayer controls url={`http://127.0.0.1:8000/media/videos/${matchVideoData.videoUrl}`} 
                    seek={calculateSeekTime(matchVideoData.startTime, matchVideoData.startFrame)}/>
          <Typography>{`Время начала: ${matchVideoData.startTime}`}</Typography>
          <Typography>{`Время конца: ${matchVideoData.endTime}`}</Typography>
        </>
      ) : (
        <Typography>Загрузка...</Typography>
      )}
    </Box>
  );
};

export default VideoComparison;