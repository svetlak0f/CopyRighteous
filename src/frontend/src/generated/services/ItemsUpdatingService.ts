/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_add_item_items__shop__post } from '../models/Body_add_item_items__shop__post';
import type { ImagesLinks } from '../models/ImagesLinks';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ItemsUpdatingService {
    /**
     * Add Item
     * @param shop
     * @param formData
     * @returns any Successful Response
     * @throws ApiError
     */
    public static addItemItemsShopPost(
        shop: string,
        formData: Body_add_item_items__shop__post,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/items/{shop}',
            path: {
                'shop': shop,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Item By Local Id
     * @param shop
     * @param localId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteItemByLocalIdItemsShopLocalIdDelete(
        shop: any,
        localId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/items/{shop}/{local_id}',
            path: {
                'shop': shop,
                'local_id': localId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Change Item Params
     * @param shop
     * @param localId
     * @param itemName
     * @param description
     * @param price
     * @param category
     * @param previewImageLink
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static changeItemParamsItemsShopLocalIdPatch(
        shop: string,
        localId: number,
        itemName?: (string | null),
        description?: (string | null),
        price?: (number | null),
        category?: (number | null),
        previewImageLink?: (string | null),
        requestBody?: (ImagesLinks | null),
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/items/{shop}/{local_id}',
            path: {
                'shop': shop,
                'local_id': localId,
            },
            query: {
                'item_name': itemName,
                'description': description,
                'price': price,
                'category': category,
                'preview_image_link': previewImageLink,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
