from stores.llm.LLMInterface import LLMInterface
from stores.llm.LLMEnums import CohereEnums, DocumentTypeEnums
import cohere
import logging
from typing import List, Union


class CohereProvider(LLMInterface):

    def __init__(
        self,
        api_key: str,
        default_input_max_characters: int = 1000,
        default_generation_max_output_tokens: int = 1000,
        default_generation_temperature: float = 0.1,
    ):
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_mode_id = None
        self.embedding_size = None

        self.enums = CohereEnums

        self.client = cohere.Client(api_key=self.api_key)

        self.logger = logging.getLogger(__name__)

    # set_generation_model method
    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    # set_embedding_model method
    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    # process_text method
    def process_text(self, text: str):
        return text[: self.default_input_max_characters].strip()

    # generate_text method
    def generate_text(
        self,
        prompt: str,
        chat_history: list = [],
        max_output_tokens: int = None,
        temperature: float = None,
    ):

        if not self.client:
            self.logger.error("Cohere client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for Cohere was not set")
            return None

        max_output_tokens = (
            max_output_tokens
            if max_output_tokens
            else self.default_generation_max_output_tokens
        )
        temperature = (
            temperature if temperature else self.default_generation_temperature
        )

        response = self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            message=self.process_text(prompt),
            temperature=temperature,
            max_tokens=max_output_tokens,
        )

        if not response or not response.text:
            self.logger.error("Error while generating text with Cohere")
            return None

        return response.text

    # construct_prompt method
    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "text": prompt,
        }

    # embed_text method
    def embed_text(self, text: Union[str, List[str]], document_type: str = None):
        if not self.client:
            self.logger.error("Cohere client was not set")
            return None

        if isinstance(text, str):
            text = [text]

        if not self.embedding_model_id:
            self.logger.error("Embedding model for Cohere was not set")
            return None

        input_type = CohereEnums.DOCUMENT
        if document_type == DocumentTypeEnums.QUERY:
            input_type = CohereEnums.QUERY

        response = self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text(t) for t in text],
            input_type=input_type,
            embedding_types=["float"],
            truncate="NONE",
        )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error while embedding text with Cohere")
            return None

        return [f for f in response.embeddings.float]
