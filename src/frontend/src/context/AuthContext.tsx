import {LocalStorageKeys} from 'constants/localStorageKeys';
import {decodeJwt} from 'helpers/decodeJWT';
import {FC, PropsWithChildren, createContext, useContext, useEffect, useState} from 'react';

// TODO: add user type
export interface User {}

interface AuthContextType {
  user: User | null;
  login: (newUser?: User, token?: string | null) => void;
  logout: () => void;
  setJwtToken: (token: string) => void;
}

const AuthContext = createContext<AuthContextType>(null!);

export const AuthProvider: FC<PropsWithChildren> = ({children}) => {
  const valueFromStorage = localStorage.getItem(LocalStorageKeys.USER);
  const initUser = valueFromStorage ? JSON.parse(valueFromStorage) : null;
  const [user, setUser] = useState<User | null>(initUser);

  useEffect(() => {
    const userJson = localStorage.getItem(LocalStorageKeys.USER);
    setUser(userJson !== null ? JSON.parse(userJson) : null);

    const token = localStorage.getItem(LocalStorageKeys.JWT_TOKEN);
    if (token) {
      const decodedToken = decodeJwt(token);

      const isExpired = decodedToken?.exp && Date.now() >= decodedToken.exp * 1000;
      isExpired && logout();
    }
  }, []);

  const setJwtToken = (token: string) => localStorage.setItem(LocalStorageKeys.JWT_TOKEN, token);

  const login = (newUser?: User, token?: string | null) => {
    if (newUser && token) {
      setUser(newUser);
      localStorage.setItem(LocalStorageKeys.USER, JSON.stringify(newUser));
      setJwtToken(token);
    }
  };

  const logout = () => {
    localStorage.removeItem(LocalStorageKeys.JWT_TOKEN);
    localStorage.removeItem(LocalStorageKeys.USER);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{user, login, logout, setJwtToken}}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
