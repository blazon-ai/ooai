# OOAI


## Dev

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e .
# start the dev server
uvicorn ooai.app:app --reload
```

You need to get the model and pre-process it.
For convenience I've checked in the `tokenizer.model` which is taken from [this huggingface repo](https://huggingface.co/decapoda-research/llama-7b-hf/tree/main).

```sh
mkdir models
cd models
wget https://the-eye.eu/public/AI/models/nomic-ai/gpt4all/gpt4all-lora-quantized.bin
pyllamacpp-convert-gpt4all gpt4all-lora-quantized.bin tokenizer.model gpt4all-model.bin
```