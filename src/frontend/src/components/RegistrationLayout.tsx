import {Box, Paper, styled} from '@mui/material';
import {Footer} from 'components/Footer';
import {FC} from 'react';
import {Outlet} from 'react-router';

const StyledPageWrapper = styled(Box)({
  minHeight: '100vh',
  display: 'flex',
  flexDirection: 'column',
});

const StyledPaperWrapper = styled(Box)({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  flex: 1,
});

const StyledPaper = styled(Paper)(({theme}) => ({
  width: 350,
  marginTop: theme.spacing(1),
  marginBottom: theme.spacing(1),
  borderRadius: theme.spacing(1),
  gap: theme.spacing(1),
  padding: theme.spacing(2),
  display: 'inline-flex',
  flexWrap: 'wrap',
  justifyContent: 'center',
}));

export const RegistrationLayout: FC = () => (
  <StyledPageWrapper>
    <StyledPaperWrapper>
      <StyledPaper>
        <Outlet />
      </StyledPaper>
    </StyledPaperWrapper>
    <Footer />
  </StyledPageWrapper>
);
