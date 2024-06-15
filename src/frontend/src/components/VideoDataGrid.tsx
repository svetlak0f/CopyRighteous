import React, { useEffect, useState } from 'react';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';

import { getAllVideosMetadata } from 'api/video_metadata';
import { deleteVideoMetadata } from 'api/video_metadata';

interface VideoData {
  video_id: string;
  uploaded_at: string;
  indexed_at: string;
  status: string;
  frames_count: number;
  video_time: string;
  framerate: number;
}

const VideoDataGrid: React.FC = () => {
  const [data, setData] = useState<VideoData[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [deleteVideoId, setDeleteVideoId] = useState('');
  const [isDeleteConfirmationOpen, setIsDeleteConfirmationOpen] = useState(false);

  const fetchData = async () => {
    try {
      setIsLoading(true);
      const response = await getAllVideosMetadata();
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

  const handleDelete = async (videoId: string) => {
    const confirmed = window.confirm(`Are you sure you want to delete ${videoId}?`);
    if (confirmed) {
      setIsLoading(true);
      setDeleteVideoId(videoId);
      setIsDeleteConfirmationOpen(true);
      try {
        // Perform delete operation
        const result = await deleteVideoMetadata(videoId);
        fetchData();
      } catch (error) {
        console.error('Error deleting video metadata:', error);
      } finally {
        setIsLoading(false);
        setIsDeleteConfirmationOpen(false);
      }
    }
  };

  const renderDeleteButton = (params: GridRenderCellParams) => (
    <Button
      variant="contained"
      color="secondary"
      startIcon={<DeleteIcon />}
      onClick={() => handleDelete(params.row.video_id as string)}
      disabled={isLoading}
    >
      Delete
    </Button>
  );

  const renderStatusIcon = (params: GridRenderCellParams) => {
    const status = params.row.status as string;
    if (status === 'Indexed') {
      return <CheckCircleIcon style={{ marginTop: '15px', color: 'green' }} />;
    }
    if (status === 'Indexing'){
      return <CircularProgress size={20} style={{ marginRight: '10px' }} />
    }
    if (status === 'Plagiary found'){
      return <ErrorIcon style={{ marginTop: '15px', color:"red" }} />
    }
    return null;
  };

  const columns: GridColDef[] = [
    { field: 'video_id', headerName: 'Video ID', width: 200 },
    { field: 'uploaded_at', headerName: 'Загружено', width: 250 },
    { field: 'indexed_at', headerName: 'Индексировано', width: 250 },
    { field: 'status', headerName: 'Статус', width: 120 },
    { field: 'frames_count', headerName: 'Количество кадров', width: 150 },
    { field: 'video_time', headerName: 'Продолжительность видео', width: 200 },
    { field: 'framerate', headerName: 'Частота кадров', width: 120 },
    {
      field: 'status_icon',
      headerName: '',
      width: 60,
      renderCell: renderStatusIcon,
    },
    {
      field: 'delete',
      headerName: 'Удалить',
      width: 140,
      renderCell: renderDeleteButton,
    },
  ];

  return (
    <div style={{ height: 800, width: '100%' }}>
      <DataGrid rows={data} columns={columns}   initialState={{
    sorting: {
      sortModel: [{ field: 'uploaded_at', sort: 'desc' }],
    },
  }}/>

      <Dialog open={isDeleteConfirmationOpen} onClose={() => setIsDeleteConfirmationOpen(false)}>
        <DialogContent>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <CircularProgress size={20} style={{ marginRight: '10px' }} />
            <span>Удаление видео {deleteVideoId}...</span>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default VideoDataGrid;