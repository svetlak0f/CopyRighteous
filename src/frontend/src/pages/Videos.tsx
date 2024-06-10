import React, { useEffect, useState } from 'react';
import VideoDataGrid from 'components/VideoDataGrid';
import { getAllVideosMetadata } from 'api/video_metadata';

export const Videos = () => {
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
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

    fetchData();
  }, []);

  return (
    <div>
      <h1>Video Data</h1>
      {isLoading ? (
        <div>Loading...</div>
      ) : (
        <VideoDataGrid data={data} />
      )}
    </div>
  );
};