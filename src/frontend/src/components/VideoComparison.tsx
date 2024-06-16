import React, { useEffect, useState } from 'react';
import { Box, Typography, Grid, Paper } from '@mui/material';
import { getSpecificMatchingJobByJobID } from 'api/jobs';
import { useSearchParams } from "react-router-dom";
import ReactPlayer from 'react-player';
import { Divider } from "@mui/material";
import { apiAddress } from 'constants/apiAddress';

interface VideoData {
  startFrame: number;
  endFrame: number;
  startTime: string;
  endTime: string;
  videoUrl: string;
  confidence_score: number;
}

interface JobResults {
  query_start_frame: number;
  query_end_frame: number;
  query_start_time: string;
  query_end_time: string;
  match_video_id: string;
  match_start_frame: number;
  match_end_frame: number;
  match_start_time: string;
  match_end_time: string;
  similarity_score: number;
}

interface VideoPlayerProps {
  videoData: VideoData;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ videoData }) => {
  return (
    <Box sx={{ padding: 2 }}>
      <ReactPlayer
        controls
        url={`${apiAddress}/media/videos/${videoData.videoUrl}`}
      />
      <Typography>{`Время начала: ${videoData.startTime}`}</Typography>
      <Typography>{`Время конца: ${videoData.endTime}`}</Typography>
    </Box>
  );
};

const VideoComparison: React.FC = () => {
  const [videoData, setVideoData] = useState<{ query: VideoData[], match: VideoData[] }>({ query: [], match: [] });
  const [searchParams] = useSearchParams();
  const [searchVideoID, setSearchVideoID] = useState<string>("")

  const job_id = String(searchParams.get("job_id") as string);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const search_job_metadata = await getSpecificMatchingJobByJobID(job_id);
        console.log(search_job_metadata);

        const queryData: VideoData[] = search_job_metadata.results.map((result: JobResults) => ({
          startFrame: result.query_start_frame,
          endFrame: result.query_end_frame,
          startTime: result.query_start_time,
          endTime: result.query_end_time,
          videoUrl: `${search_job_metadata.query_video_id}.mp4`,
          confidence_score: result.similarity_score
        }));

        const matchData: VideoData[] = search_job_metadata.results.map((result: JobResults) => ({
          startFrame: result.match_start_frame,
          endFrame: result.match_end_frame,
          startTime: result.match_start_time,
          endTime: result.match_end_time,
          videoUrl: `${result.match_video_id}.mp4`
        }));

        setVideoData({ query: queryData, match: matchData });
        setSearchVideoID(search_job_metadata.query_video_id)
      } catch (error) {
        console.error('Error fetching video data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <Box sx={{ padding: 4 }}>
      <Typography variant="h4" sx={{ marginBottom: 3 }}>Мэтчинг для видео {searchVideoID}</Typography>
      {videoData.query.length && videoData.match.length ? (
        videoData.query.map((queryVideo, index) => (
          <>
          <Grid container spacing={4} key={index} alignItems="flex-start" sx={{ marginBottom: 5, marginTop: 1 }}>
            <Grid item xs={6}>
              <Paper elevation={5} sx={{ padding: 3, height:550 }}>
                <Typography variant="h5" sx={{ marginBottom: 2 }}>Видео из запроса</Typography>
                <VideoPlayer videoData={queryVideo} />
              </Paper>
            </Grid>
            <Grid item xs={6}>
              <Paper elevation={5} sx={{ padding: 3, height:550 }}>
                <Typography variant="h5" sx={{ marginBottom: 2 }}>Найденное видео: {videoData.match[index].videoUrl}</Typography>
                <VideoPlayer videoData={videoData.match[index]} />
                <Typography variant="h6" sx={{ marginTop: 2 }}>Скор похожести: {queryVideo.confidence_score}</Typography>
              </Paper>
            </Grid>
          </Grid>
          <Divider sx={{ borderBottomWidth: '5px'}}/>
          </>
        ))
      ) : (
        <Typography>Загрузка...</Typography>
      )}
    </Box>
  );
};

export default VideoComparison