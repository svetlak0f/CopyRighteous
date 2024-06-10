export interface DecodedTokenData {
  username?: string;
  exp?: number;
  iat?: number;
}

export const decodeJwt = (token: string | null): DecodedTokenData | null => {
  if (token) {
    const [, payloadB64] = token.split('.');
    const {username, exp, iat} = JSON.parse(atob(payloadB64));

    return {username, exp, iat};
  }

  return null;
};
