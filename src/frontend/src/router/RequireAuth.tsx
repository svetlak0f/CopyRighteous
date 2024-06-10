import {useAuth} from 'context/AuthContext';
import {FC} from 'react';
import {Navigate, useLocation} from 'react-router-dom';
import {Routes} from 'router';

interface RequireAuthProps {
  component: JSX.Element;
}

export const RequireAuth: FC<RequireAuthProps> = ({component}) => {
  const {user} = useAuth();
  const location = useLocation();

  if (!user) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    return <Navigate to={Routes.Login} state={{from: location}} replace />;
  }

  return component;
};
