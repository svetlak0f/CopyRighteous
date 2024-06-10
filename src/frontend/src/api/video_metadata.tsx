import { apiAddress } from "constants/apiAddress";


export const getAllVideosMetadata = async () =>
    await fetch(`${apiAddress}/metadata/video`, {
        method: "GET"})
        .then((response) => response.json())
        .catch((reason) => console.error(reason));


export const getSpecificVideoMetadata = async (video_id: string) =>
    await fetch(`${apiAddress}/metadata/video/${video_id}`, {
        method: "GET"})
        .then((response) => response.json())
        .catch((reason) => console.error(reason));


export const getIndexingVideoMetadata = async () =>
    await fetch(`${apiAddress}/metadata/video/indexing`, {
        method: "GET"})
        .then((response) => response.json())
        .catch((reason) => console.error(reason));


export const deleteVideoMetadata = async (video_id: string) =>
    await fetch(`${apiAddress}/metadata/video/${video_id}`, {
        method: "GET"})
        .then((response) => response.json())
        .catch((reason) => console.error(reason));