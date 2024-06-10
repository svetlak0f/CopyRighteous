import { apiAddress } from "constants/apiAddress";


export const getAllMatchingJobs = async () =>
    await fetch(`${apiAddress}/metadata/matching_jobs`, {
        method: "GET"})
        .then((response) => response.json())
        .catch((reason) => console.error(reason));


export const getActiveMatchingJobs = async () =>
    await fetch(`${apiAddress}/metadata/matching_jobs/active`, {
        method: "GET"})
        .then((response) => response.json())
        .catch((reason) => console.error(reason));


export const getSpecificMatchingJobByJobID = async (job_id: string) =>
    await fetch(`${apiAddress}/metadata/matching_jobs/${job_id}`, {
        method: "GET"})
        .then((response) => response.json())
        .catch((reason) => console.error(reason));


export const getSpecificMatchingJobByVideoID = async (video_id: string) =>
    await fetch(`${apiAddress}/metadata/matching_jobs/by_video/${video_id}`, {
        method: "GET"})
        .then((response) => response.json())
        .catch((reason) => console.error(reason));