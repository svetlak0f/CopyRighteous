import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { AppBar, Tab, Tabs, Typography } from '@mui/material';
import { Routes } from 'router';

const Header: React.FC = () => {
  const location = useLocation();

  // Get the current path from the location object
  const currentPath = location.pathname;

  // Custom styles for the tabs
  const tabStyles = {
    color: '#CCCCCC',
    fontWeight: 600,
  };

  // Custom active tab styles
  const activeTabStyles = {
    ...tabStyles,
    color: '#FFFFFF', // Change the active text color here
  };

  return (
    <AppBar position="static">
      <Typography variant="h6" style={{ marginLeft: '1rem' }}>
        CopyRighteous
      </Typography>
      <Tabs value={currentPath} variant="fullWidth">
        <Tab
          label="Видео"
          value={Routes.Videos}
          component={Link}
          to={Routes.Videos}
          style={currentPath === Routes.Videos ? activeTabStyles : tabStyles}
        />
        <Tab
          label="Матчинг"
          value={Routes.Matching}
          component={Link}
          to={Routes.Matching}
          style={currentPath === Routes.Matching ? activeTabStyles : tabStyles}
        />
        <Tab
          label="Загрузка видео"
          value={Routes.UploadVideo}
          component={Link}
          to={Routes.UploadVideo}
          style={currentPath === Routes.UploadVideo ? activeTabStyles : tabStyles}
        />
      </Tabs>
    </AppBar>
  );
};

export default Header;