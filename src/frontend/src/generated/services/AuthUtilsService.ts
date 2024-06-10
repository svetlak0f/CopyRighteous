/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_for_access_token_auth_token_post } from '../models/Body_login_for_access_token_auth_token_post';
import type { Body_register_auth_register_post } from '../models/Body_register_auth_register_post';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class AuthUtilsService {
    /**
     * Login For Access Token
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static loginForAccessTokenAuthTokenPost(
        formData: Body_login_for_access_token_auth_token_post,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Register
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerAuthRegisterPost(
        formData: Body_register_auth_register_post,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/register',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
