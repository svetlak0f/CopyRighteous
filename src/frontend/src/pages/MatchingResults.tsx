import { Box } from '@mui/system';
import VideoComparison from 'components/VideoComparison';

export const MatchingResults = () => {
  return (
    <Box sx={{ margin: '2rem' }}>
      <h1>Работы анализа видео</h1>
        <VideoComparison />
    </Box>
  );
};