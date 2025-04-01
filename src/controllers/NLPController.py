from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from typing import List
from stores.llm.LLMEnums import DocumentTypeEnums
import json


class NLPController(BaseController):

    def __init__(self, vectordb_client, generation_client, embedding_client):
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client

    # create_collection_name method
    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()

    # reset_vectordb_collection method
    def reset_vectordb_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)

    # get_vectordb_collection_info method
    def get_vectordb_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(
            collection_name=collection_name
        )

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__),
        )

    # index_into_vectordb method
    def index_into_vectordb(
        self,
        project: Project,
        chunks: List[DataChunk],
        chunks_ids: List[int],
        do_reset: bool = False,
    ):
        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: manage items
        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]
        vectors = [
            self.embedding_client.embed_text(
                text=text, document_type=DocumentTypeEnums.DOCUMENT.value
            )
            for text in texts
        ]

        # step3: create collection if not exists
        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )
        # step4: insert into vector db
        _ = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
            record_ids=chunks_ids,
        )

        return True

    def search_vectordb_collection(self, project: Project, text: str, limit: int = 10):

        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: get text embedding vector
        vector = self.embedding_client.embed_text(
            text=text,
            document_type=DocumentTypeEnums.QUERY.value,
        )

        if not vector or len(vector) == 0:
            return False

        # step3: do semantic search
        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit,
        )

        if not results:
            return False

        return json.loads(
            json.dumps(results, default=lambda x: x.__dict__),
        )
