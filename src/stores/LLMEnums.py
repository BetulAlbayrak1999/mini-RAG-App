from enum import Enum


class LLMEnums(Enum):
    OPENAAI = "OPENAI"
    COHERE = "COHERE"


class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class CohereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"


class DocumentTypeEnums(Enum):
    DOCUMENT = "document"
    QUERY = "query"
