import logging
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from datetime import datetime
from ooai.types import (
    ChatEngine,
    Choice,
    CompletionRequest,
    CompletionResponse,
    Message,
)
from ooai.gpt4all import GPT4All

logger = logging.getLogger("ooai")

app = FastAPI()

engine = GPT4All()


@app.post("/chat/completions")
def handle_chat_completions(body: CompletionRequest):
    # [todo] this isn't quite the right thing to do because uvicorn can start multiple worker processes
    # so you want the engine object to be load-balanced
    if body.model != "gpt4all":
        raise HTTPException(
            status_code=400, detail="Invalid model: needs to be 'gpt4all'"
        )
    try:
        result = engine.predict(body.messages)
    except Exception as e:
        logger.exception("engine threw")
        raise HTTPException(status_code=500)

    return CompletionResponse(
        id=str(uuid4()),
        object="idk",
        created=datetime.utcnow(),
        choices=[Choice(index=0, message=result, finish_reason="stop")],
        usage=None,
    )


"""
run this with
uvicorn ooai.app:app --reload

there will be a docs page at http://localhost:????/docs
"""
