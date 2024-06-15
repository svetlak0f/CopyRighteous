import {RegistrationLayout} from 'components/RegistrationLayout';
import {Home} from 'pages/Home';
import {Login} from 'pages/Login';
import {Registration} from 'pages/Registration';
import { Videos } from 'pages/Videos';
import { MatchingJobs } from 'pages/MatchingJobs';
import {FC} from 'react';
import { UploadVideo } from 'pages/UploadVideo';
import {BrowserRouter, Navigate, Route, Routes as RoutesComponent} from 'react-router-dom';
import {ScrollToTop} from 'router/ScrollToTop';
import Header from 'components/Header';
import { MatchingResults } from 'pages/MatchingResults';


export enum Routes {
  Home = '/',
  Videos = '/videos',
  Matching = '/matching',
  UploadVideo = '/upload',
  MatchingResults='/matching_results'
}

export const Router: FC = () => {
  return (
      <BrowserRouter>
        <ScrollToTop />
        <Header />
        <RoutesComponent>
            <Route path={Routes.Home} element={<Home />} />
            <Route path={Routes.Matching} element={<MatchingJobs />} />
            <Route path={Routes.Videos} element={<Videos />} />
            <Route path={Routes.UploadVideo} element={<UploadVideo />} />
            <Route path={Routes.MatchingResults} element={<MatchingResults />} />
          <Route path="*" element={<Navigate to={Routes.Home} replace />} />
        </RoutesComponent>
      </BrowserRouter>
  );
};
