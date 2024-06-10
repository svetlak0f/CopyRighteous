import { apiAddress } from 'constants/apiAddress';

export const asyncSendVideoToIndexing = async (search_while_ingestion: boolean, item_data:FormData) =>
    await fetch(`${apiAddress}/async/ingestion/upload_and_index_video?search_while_ingestion=${search_while_ingestion}`, {
        method: 'POST',
        body: item_data,
    })
    .then((response) => response.ok ? response.ok : false)
    .catch((reason) => console.error(reason));