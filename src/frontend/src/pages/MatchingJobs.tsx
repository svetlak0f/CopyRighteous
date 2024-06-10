import { Box } from '@mui/system';
import { Margin } from '@mui/icons-material';
import JobsDataGrid from 'components/MatchingJobs';
import ActiveJobsDataGrid from 'components/ActiveMatchingJobs';

export const MatchingJobs = () => {
  return (
    <Box sx={{ margin: '2rem' }}>
      <h1>Работы анализа видео</h1>
      <h2>Активные задания</h2>
      <ActiveJobsDataGrid />
      <h2>Все задания</h2>
      <JobsDataGrid />
    </Box>
  );
};