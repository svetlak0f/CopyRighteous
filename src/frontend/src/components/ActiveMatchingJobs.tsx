import React, { useEffect, useState } from 'react';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';

import { deleteVideoMetadata } from 'api/video_metadata';
import { getActiveMatchingJobs } from 'api/jobs';

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

const ActiveJobsDataGrid: React.FC = () => {
  const [data, setData] = useState<JobData[]>([]);

  const fetchData = async () => {
    try {
      const response = await getActiveMatchingJobs();
      const updatedData = response.map((video: object, index: number) => ({
        ...video,
        id: index + 1,
      }));
      setData(updatedData);
    } catch (error) {
      console.error('Error fetching video metadata:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);



  const renderStatusIcon = (params: GridRenderCellParams) => {
    const status = params.row.status as string;
    if (status === 'Done') {
      return <CheckCircleIcon style={{ color: 'green' }} />;
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
    // {
    //   field: 'delete',
    //   headerName: 'Удалить',
    //   width: 140,
    //   renderCell: renderDeleteButton,
    // },
  ];

  if (data.length == 0){
    return (<h3>Нет активных заданий</h3>)
  }

  return (
    <div style={{ height: 300, width: '100%' }}>
      <DataGrid rows={data} columns={columns} />
    </div>
  );
};

export default ActiveJobsDataGrid;