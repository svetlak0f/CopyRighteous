/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Item } from '../models/Item';
import type { ItemWithShopID } from '../models/ItemWithShopID';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ItemsRetrievingService {
    /**
     * Get All Items
     * @returns ItemWithShopID Successful Response
     * @throws ApiError
     */
    public static getAllItemsItemsGet(): CancelablePromise<Array<ItemWithShopID>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/items/',
        });
    }
    /**
     * Get Items By Shop
     * @param shop
     * @returns Item Successful Response
     * @throws ApiError
     */
    public static getItemsByShopItemsShopGet(
        shop: string,
    ): CancelablePromise<Array<Item>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/items/{shop}',
            path: {
                'shop': shop,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Item By Shop And Local Id
     * Get specific item by shop and local id
     * @param shop
     * @param localId
     * @returns Item Successful Response
     * @throws ApiError
     */
    public static getItemByShopAndLocalIdItemsShopLocalIdGet(
        shop: string,
        localId: number,
    ): CancelablePromise<Item> {
        return __request(OpenAPI, {
            method: 'GET',
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
}
