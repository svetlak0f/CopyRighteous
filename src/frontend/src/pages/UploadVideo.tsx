import { Box } from '@mui/system';
import VideoUploadForm from 'components/VideoUploadForm';
import VideoMatchUploadForm from 'components/VideoMatchUploadForm';

export const UploadVideo = () => {
  return (
    <Box sx={{ margin: '2rem' }}>
        <VideoUploadForm />
        <br />
        <VideoMatchUploadForm />
    </Box>
  );
};