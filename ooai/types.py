from abc import ABC, abstractmethod
from datetime import datetime
from typing import Literal, Optional, Union
from pydantic import BaseModel, Field


class Message(BaseModel):
    """OpenAI chat message.

    ref: https://platform.openai.com/docs/guides/chat
    """

    role: Literal["system", "user", "assistant"]
    content: str

    @classmethod
    def user(cls, content: str) -> "Message":
        return cls(role="user", content=content)

    @classmethod
    def system(cls, content: str) -> "Message":
        return cls(role="system", content=content)

    @classmethod
    def assistant(cls, content: str) -> "Message":
        return cls(role="assistant", content=content)


class CompletionRequest(BaseModel):
    """Request body for OpenAI completion API.

    ref: https://platform.openai.com/docs/api-reference/chat/create
    """

    model: str = Field("gpt4all")
    """ ID of the model to use.
    See [model compatibility page](model endpoint compatibility).
    As of 2022-04-06 these are
    	gpt-4, gpt-4-0314, gpt-4-32k, gpt-4-32k-0314, gpt-3.5-turbo, gpt-3.5-turbo-0301

    We also support gpt4all
    """
    messages: list[Message]

    # temperature: float = Field(1.0, le=2.0, ge=0.0)

    # stream: bool = Field(False)

    # top_p: float = Field(1.0, ge=0.0, le=1.0)
    # n: int = Field(1, ge=1, le=100)
    # stop: Optional[Union[str, list[str]]] = Field(None)
    # max_tokens: Optional[int] = Field(None)
    # presence_penalty: float = Field(0.0, ge=-2.0, le=2.0)
    # frequency_penalty: float = Field(0.0, ge=-2.0, le=2.0)
    # logit_bias: Optional[dict] = Field(None)

    # user: Optional[str] = Field(None)
    """ Unique identifer representing your end-user. """


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: Optional[Literal["stop", "length", "content_filter"]]


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionResponse(BaseModel):
    id: str
    object: str
    created: datetime
    choices: list[Choice]
    usage: Optional[Usage]  # [todo] not optional?


class ChatEngine(ABC):
    @abstractmethod
    def predict(self, messages: list[Message]) -> Message:
        ...
