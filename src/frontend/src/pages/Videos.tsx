import { Box } from '@mui/system';
import { Margin } from '@mui/icons-material';
import VideoDataGrid from 'components/VideoDataGrid';

export const Videos = () => {
  return (
    <Box sx={{ margin: '2rem' }}>
      <h1>Видео Индекс</h1>
      <VideoDataGrid />
    </Box>
  );
};