import logging
from pathlib import Path
from pyllamacpp.model import Model
import re
from ooai.types import ChatEngine, Message


class GPT4All(ChatEngine):
    def __init__(self, model_path=Path("./models/gpt4all-model.bin")):
        super().__init__()
        self.model = Model(
            ggml_model=str(model_path), n_ctx=512, log_level=logging.WARNING
        )

    def predict(self, messages: list[Message]) -> Message:
        prompt = "".join(f"> {m.role}:\n{m.content}\n" for m in messages)
        prompt += "> assistant:\n"
        # [note] available gpt params: https://github.com/nomic-ai/pyllamacpp/blob/2058910c5b83f5078480f005f7d7d7ccd051b6f1/pyllamacpp/constants.py#L64
        result = self.model.generate(prompt=prompt, n_predict=55)
        result = result.strip()
        # annoyingly the result includes the prompt,
        # result = result.split("> assistant:\n")[-1]
        xs = re.split(r"^> (\w+):$", result, flags=re.MULTILINE)
        xs = xs[1:]
        assert len(xs) % 2 == 0, "expected an even number of results"
        reconstructed_messages = [
            Message(role=role, content=content) for (role, content) in zip(*([iter(xs)] * 2), strict=True)  # type: ignore
        ]
        new_messages = reconstructed_messages[len(messages) :]
        assert len(new_messages) == 1, "made multiple messages"
        new_message = new_messages[0]
        assert new_message.role == "assistant", "bad role"
        return new_message


if __name__ == "__main__":
    r = GPT4All().predict(
        [
            Message.system("you are a question answering assistant"),
            Message.user("Who won the world series in 2020?"),
            Message.assistant("The Los Angeles Dodgers won the World Series in 2020."),
            Message.user("where was it played?"),
        ]
    )
    print(r.content)
