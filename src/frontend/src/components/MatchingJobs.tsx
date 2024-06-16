import React, { useEffect, useState } from 'react';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import ErrorIcon from '@mui/icons-material/Error';
import InfoIcon from '@mui/icons-material/Info';
import { Link } from 'react-router-dom';

import { deleteVideoMetadata } from 'api/video_metadata';
import { getAllMatchingJobs } from 'api/jobs';

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

const JobsDataGrid: React.FC = () => {
  const [data, setData] = useState<JobData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isDeleteConfirmationOpen, setIsDeleteConfirmationOpen] = useState(false);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      const response = await getAllMatchingJobs();
      const updatedData = response.map((video: object, index: number) => ({
        ...video,
        id: index + 1,
      }));
      setData(updatedData);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching video metadata:', error);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const renderDeleteButton = (params: GridRenderCellParams) => {
    const results = params.row.results as JobResults[];
    if (results && results.length > 0){
      return (
        <Button
          variant="contained"
          color="secondary"
          startIcon={<InfoIcon />}
          component={Link}
          to={`/matching_results?job_id=${params.row.job_id}`}
          disabled={isLoading}
        >
          Детали
        </Button>
      )
    }
};

  const renderStatusIcon = (params: GridRenderCellParams) => {
    const status = params.row.status as string;
    const results = params.row.results as JobResults[];
    if (results && results.length > 0) {
      return <ErrorIcon style={{marginTop: '15px', color: 'red' }} />;
    }
    if (status === 'Done') {
      return <CheckCircleIcon style={{marginTop: '15px', color: 'green' }} />;
    }
    if (status === 'In progress'){
      return <CircularProgress size={20} style={{ marginRight: '10px' }} />
    }
    return null;
  };

  const columns: GridColDef[] = [
    { field: 'job_id', headerName: 'Matching  JobID', width: 300},
    { field: 'query_video_id', headerName: 'ID анализируемого видео', width: 250 },
    { field: 'status', headerName: 'Статус', width: 100 },
    { field: 'started_at', headerName: 'Время начала анализа', width: 300 },
    { field: 'finished_at', headerName: 'Время окончания анализа', width: 300 },
    {
      field: 'status_icon',
      headerName: '',
      width: 60,
      renderCell: renderStatusIcon,
    },
    {
      field: 'details',
      headerName: 'Детали',
      width: 140,
      renderCell: renderDeleteButton,
    },
  ];


  
  return (
    <div style={{ height: 800, width: '100%' }}>
      <DataGrid rows={data} columns={columns} initialState={{
    sorting: {
      sortModel: [{ field: 'started_at', sort: 'desc' }],
    },
  }} />

      <Dialog open={isDeleteConfirmationOpen} onClose={() => setIsDeleteConfirmationOpen(false)}>
        <DialogContent>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <CircularProgress size={20} style={{ marginRight: '10px' }} />
            <span>Удаление ...</span>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default JobsDataGrid;