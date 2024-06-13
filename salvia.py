import os
import gc
import torch
import json
from transformers import BitsAndBytesConfig
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext  #Vector store index is for indexing the vector
from llama_index.llms.huggingface import HuggingFaceLLM
from langchain.embeddings.huggingface import HuggingFaceEmbeddings


lang_pack = os.environ["LANG"]
print(os.listdir())
documents = SimpleDirectoryReader(f'{lang_pack}/knowledge_base').load_data()
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 700,
#     chunk_overlap  = 50,
# )
#docs_after_split = text_splitter.split_documents(documents)

docs_after_split[0]
model_params = json.load(open('params.json'))[f'{lang_pack}']
system_prompt = model_params["PROMPT"]

def load_model():
    if torch.cuda.is_available():
        quantization_config = BitsAndBytesConfig(load_in_4bit=True,
                                                 llm_int8_threshold=200.0)
        quantization_kwargs = {"torch_dtype": torch.float16 , "quantization_config":quantization_config}
    else:
        quantization_kwargs = {"offload_folder":"offload"}

    return HuggingFaceLLM(
        context_window=4096,
        max_new_tokens=256,
        generate_kwargs={"temperature": 0.01, "do_sample": False},
        system_prompt=system_prompt,
        tokenizer_name=model_params['LLM'],
        model_name=model_params['LLM'],
        device_map="cuda",
        # loading model in 8bit for reducing memory
        model_kwargs=quantization_kwargs
    )


def load_embedding():
    embed_model= HuggingFaceEmbeddings(model_name=model_params['EMBEDDING'])
    return embed_model


def load_context(llm, embedding):
    
    return ServiceContext.from_defaults(
    chunk_size=1024,
    llm=llm,
    embed_model=embedding
)


llm = load_model()
embedding = load_embedding()
context = load_context(llm, embedding)

del llm
del embedding
import gc
gc.collect()

index = VectorStoreIndex.from_documents(documents, service_context=context)
#vectorstore = FAISS.from_documents(docs_after_split, huggingface_embeddings)
# query = """What were the trends in median household income across
#            different states in the United States between 2021 and 2022."""  
#          # Sample question, change to other questions you are interested in.
# relevant_documents = vectorstore.similarity_search(query)
# print(f'There are {len(relevant_documents)} documents retrieved which are relevant to the query. Display the first one:\n')
# print(relevant_documents[0].page_content)
#retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

query_engine = index.as_query_engine(streaming=True, verbose=True, similarity_top_k=1)


