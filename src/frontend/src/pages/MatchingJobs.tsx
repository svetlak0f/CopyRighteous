import { Box } from '@mui/system';
import { Margin } from '@mui/icons-material';
import JobsDataGrid from 'components/MatchingJobs';
import ActiveJobsDataGrid from 'components/ActiveMatchingJobs';
import { Button } from '@mui/material';
import { Link } from 'react-router-dom';
import { apiAddress } from 'constants/apiAddress';
import FileDownloadIcon from '@mui/icons-material/FileDownload';

export const MatchingJobs = () => {
  return (
    <Box sx={{ margin: '2rem' }}>
      <h1>Работы анализа видео</h1>
      <h2>Активные задания</h2>
      <ActiveJobsDataGrid />
      <h2>Все задания</h2>
      <h3> <Button
          variant="contained"
          color="secondary"
          startIcon={<FileDownloadIcon />}
          component={Link}
          to={`${apiAddress}/metadata/matching_jobs/submission_file`}>
          Выгрузить все задания
        </Button></h3>
      <JobsDataGrid />
    </Box>
  );
};