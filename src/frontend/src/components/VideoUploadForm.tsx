import React, { useState, useRef } from 'react';
import { Button, CircularProgress, Snackbar, LinearProgress, Box, Typography, Checkbox } from '@mui/material';
import { Alert } from '@mui/material';

import { apiAddress } from 'constants/apiAddress';

const VideoUploadForm: React.FC = () => {
  const [searchWhileIngestion, setSearchWhileIngestion] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadCompleted, setUploadCompleted] = useState(false);
  const [error, setError] = useState(false);
  const [progress, setProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUpload = () => {
    const file = fileInputRef.current?.files?.[0];

    if (file) {
      const xhr = new XMLHttpRequest();

      xhr.upload.onprogress = (event) => {
        const { loaded, total } = event;
        const progressPercentage = Math.round((loaded / total) * 100);
        setProgress(progressPercentage);
      };

      xhr.onreadystatechange = () => {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            setUploadCompleted(true);
          } else {
            console.error('Upload failed');
            setError(true);
          }
          setUploading(false);
          if (fileInputRef.current) {
            fileInputRef.current.value = ''; // Reset file input
          }
        }
      };


      var url = `${apiAddress}/async/ingestion/upload_and_index_video`
      if (searchWhileIngestion) {
        url += '?search_while_ingestion=true';
      }

      xhr.open('POST', url);
      const formData = new FormData();
      formData.append('video', file, file.name);
      xhr.send(formData);
      setUploading(true);
    }
  };

  const handleAlertClose = () => {
    setUploadCompleted(false);
    setError(false);
  };

  const handleCheckpointChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchWhileIngestion(event.target.checked);
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Загрузка видео в базу
      </Typography>

      <input type="file" accept="video/*" ref={fileInputRef} />

      <Box mt={2}>
        <Checkbox
          checked={searchWhileIngestion}
          onChange={handleCheckpointChange}
        />
        Произвести поиск плагиата после загрузки
      </Box>

      <Box mt={2}>
        <Button variant="contained" color="primary" onClick={handleUpload} disabled={uploading}>
          {uploading ? <CircularProgress size={24} /> : 'Upload'}
        </Button>
      </Box>

      {uploading && (
        <Box mt={2}>
          <LinearProgress variant="determinate" value={progress} color="primary" />
        </Box>
      )}

      <Snackbar
        open={uploadCompleted}
        autoHideDuration={8000}
        onClose={handleAlertClose}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }} // Set anchorOrigin to top-center
        style={{ top: '40px' }} // Adjust the top position as needed
      >
        <Alert severity="success" onClose={handleAlertClose}>
          Видео загружено успешно. Процесс индексации начнется в ближайшее время
        </Alert>
      </Snackbar>

      <Snackbar
        open={error}
        autoHideDuration={8000}
        onClose={handleAlertClose}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }} // Set anchorOrigin to top-center
        style={{ top: '40px' }} // Adjust the top position as needed
      >
        <Alert severity="error" onClose={handleAlertClose}>
          Видео уже существует, удалите предыдущее перед повторной индексацией
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default VideoUploadForm;