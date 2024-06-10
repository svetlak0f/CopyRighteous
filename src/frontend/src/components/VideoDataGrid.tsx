import React from 'react';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import DeleteIcon from '@mui/icons-material/Delete';
import Button from '@mui/material/Button';

interface VideoData {
  video_id: string;
  uploaded_at: string;
  indexed_at: string;
  status: string;
  frames_count: number;
  video_time: string;
  framerate: number;
}

interface VideoDataGridProps {
  data: VideoData[];
}

const VideoDataGrid: React.FC<VideoDataGridProps> = ({ data }) => {
  const handleDelete = (videoId: string) => {
    const confirmed = window.confirm(`Are you sure you want to delete ${videoId}?`);
    if (confirmed) {
      // Perform delete operation
    }
  };

  const renderDeleteButton = (params: GridRenderCellParams) => (
    <Button
      variant="contained"
      color="secondary"
      startIcon={<DeleteIcon />}
      onClick={() => handleDelete(params.row.video_id as string)}
       // Add condition to enable/disable the delete button
    >
      Delete
    </Button>
  );

  const columns: GridColDef[] = [
    { field: 'video_id', headerName: 'Video ID', width: 200 },
    { field: 'uploaded_at', headerName: 'Uploaded At', width: 200 },
    { field: 'indexed_at', headerName: 'Indexed At', width: 200 },
    { field: 'status', headerName: 'Status', width: 120 },
    { field: 'frames_count', headerName: 'Frames Count', width: 150 },
    { field: 'video_time', headerName: 'Video Time', width: 150 },
    { field: 'framerate', headerName: 'Frame Rate', width: 120 },
    {
      field: 'delete',
      headerName: 'Delete',
      width: 140,
      renderCell: renderDeleteButton,
    },
  ];

  return (
    <div style={{ height: 400, width: '100%' }}>
      <DataGrid rows={data} columns={columns} />
    </div>
  );
};

export default VideoDataGrid;