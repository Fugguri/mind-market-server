

from llama_index import SimpleDirectoryReader, GPTListIndex, GPTVectorStoreIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
import gradio as gr
import sys
import os
import mics._openai as _openai
_openai.api_key = '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'

os.environ["OPENAI_API_KEY"] = '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'


def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 0.5
    chunk_size_limit = 600

    prompt_helper = PromptHelper(
        max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=OpenAI(
        temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()
    index = GPTVectorStoreIndex(
        documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.storage_context.persist()
    return index


index = construct_index("docs")


def chatbot(input_text):
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    # index = GPTVectorStoreIndex.load_from_disk('index.json')
    # response = index.query(input_text, response_mode="compact")
    print(response)
    return response.response


iface = gr.Interface(fn=chatbot,
                     inputs=gr.inputs.Textbox(
                         lines=7, label="Enter your text"),
                     outputs="text",
                     title="Custom-trained AI Chatbot")

iface.launch(share=True)
