from qdrant_client import models, QdrantClient
from stores.vectordb.VectorDBInterface import VectorDBInterface
from stores.vectordb.VectorDBEnums import DistanceMethodEnums
import logging
from typing import List
from models.db_schemes import RetrievedDocument


class QdrantDBProvider(VectorDBInterface):

    def __init__(
        self,
        db_client: str,
        distance_method: str,
        default_vector_size: int = 786,
        index_threshold: int = 100,
    ):
        self.client = None
        self.db_client = db_client
        self.distance_method = distance_method
        self.default_vector_size= default_vector_size
        self.index_thrtehold= index_threshold

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE

        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger("uvicorn")

    # connect method
    async def connect(self):
        self.client = QdrantClient(path=self.db_client)

    # disconnect method
    async def disconnect(self):
        self.client = None

    # is_collection_existed method
    async def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)

    # list_all_collections method
    async def list_all_collections(self) -> List:
        return self.client.get_collections()

    # get_collection_info method
    async def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)

    # delete_collection method
    async def delete_collection(self, collection_name: str):
        if self.is_collection_existed(collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        else:
            self.logger.error("Collection does not exist")
            return None

    # create_collection method
    async def create_collection(
        self, collection_name: str, embedding_size: int, do_reset: bool = False
    ):
        if do_reset:
            _ = self.delete_collection(collection_name=collection_name)

        if not self.is_collection_existed(collection_name=collection_name):
            self.logger.info(f"Creating new Qdrant collection: {collection_name}")

            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method,
                ),
            )

            return True

        return False

    # insert_one method
    async def insert_one(
        self,
        collection_name: str,
        text: str,
        vector: list,
        metadata: dict = None,
        record_id: str = None,
    ):
        if not self.is_collection_existed(collection_name=collection_name):
            self.logger.error(
                f"Can not insert new record to non-existed collection: {collection_name}"
            )
            return False

        try:
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=[record_id],
                        vecotr=vector,
                        payload={
                            "text": text,
                            "metadata": metadata,
                        },
                    )
                ],
            )
        except Exception as e:
            self.logger.error(f"Error while inserting batch: {e}")
            return False

        return True

    # insert_many method
    async def insert_many(
        self,
        collection_name: str,
        texts: list,
        vectors: list,
        metadata: list = None,
        record_ids: list = None,
        batch_size: int = 50,
    ):

        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(0, len(texts)))

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadat = metadata[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]

            batch_records = [
                models.Record(
                    id=batch_record_ids[x],
                    vector=batch_vectors[x],
                    payload={
                        "text": batch_texts[x],
                        "metadata": batch_metadat[x],
                    },
                )
                for x in range(len(batch_texts))
            ]

            try:
                _ = self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_records,
                )

            except Exception as e:
                self.logger.error(f"Error while inserting batch: {e}")
                return False

        return True

    # search_by_vector method
    async def search_by_vector(
        self, collection_name: str, vector: list, limit: int = 5
    ):

        results = self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit,
        )
        if not results or len(results) == 0:
            return None

        return [
            RetrievedDocument(
                **{
                    "score": result.score,
                    "text": result.payload["text"],
                }
            )
            for result in results
        ]
