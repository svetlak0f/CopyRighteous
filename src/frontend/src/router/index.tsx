import {RegistrationLayout} from 'components/RegistrationLayout';
import {Home} from 'pages/Home';
import {Login} from 'pages/Login';
import {Registration} from 'pages/Registration';
import {FC} from 'react';
import {BrowserRouter, Navigate, Route, Routes as RoutesComponent} from 'react-router-dom';
import {ScrollToTop} from 'router/ScrollToTop';


export enum Routes {
  Home = '/',
  Login = '/login',
  Registration = '/registration',
}

export const Router: FC = () => {
  return (
      <BrowserRouter>
        <ScrollToTop />
        <RoutesComponent>
          <Route element={<RegistrationLayout />}>
            <Route path={Routes.Home} element={<Home />} />
            <Route path={Routes.Login} element={<Login />} />
            <Route path={Routes.Registration} element={<Registration />} />
          </Route>
          <Route path="*" element={<Navigate to={Routes.Home} replace />} />
        </RoutesComponent>
      </BrowserRouter>
  );
};
