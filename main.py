import os
from dotenv import load_dotenv
import openai

import pickle
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI


from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from flask import Flask, request,jsonify
import json
import requests


app = Flask(__name__)

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


urls = [
    'https://www.gov.uk/guidance/immigration-rules/immigration-rules-appendix-v-visitor',
    'https://www.gov.uk/standard-visitor',
    'https://www.gov.uk/standard-visitor/apply-standard-visitor-visa'
]


loaders = UnstructuredURLLoader(urls=urls)
data = loaders.load()

# Text Splitter
text_splitter = CharacterTextSplitter(separator='\n',
                                      chunk_size=1000,
                                      chunk_overlap=200)


docs = text_splitter.split_documents(data)

embeddings = OpenAIEmbeddings()

vectorStore_openAI = FAISS.from_documents(docs, embeddings)


@app.route("/enquire", methods=["POST"])
def enquire():
    data = request.json
    question = data.get("question")
    question = str(question)
    history = data.get("history")
    history = list(history)

    llm=ChatOpenAI(temperature=0, model_name='gpt-4')
    memory = ConversationSummaryMemory(llm=llm,memory_key="chat_history",return_messages=True)
    for text in history:
        if text.startswith("user"):
            memory.chat_memory.add_user_message(text[5:])
        if text.startswith("ai"):
            memory.chat_memory.add_ai_message(text[3:])
        

    with open("data/faiss_store_openai.pkl", "rb") as f:
        VectorStore = pickle.load(f)


    retriever = VectorStore.as_retriever()
    messages=[
        SystemMessage(
            content="You are a chatbot. Your role and purpose is to provide people with personalized information on what they need in order to obtain a visa to any place they want to travel to.\n- You will do this by going through the travel requirements provided by the sources given to you and in case the chat history does not have all the information you need, you will ask them to give more information as a follow up question\n- You should not generalize or assume anything. Ask a follow up question for any information you do not have.\n- You can also suggest tips for them to boost their application looking at their background. They do not have to ask. You can ask them extra follow-up questions to gather more information so that you can provide them with more information.\n- In the end, you can provide them with a detailed overview or checklist of what they need in order obtain a visa to their intended place of travel successfully\n- In case one of the visa application requirements is a cover letter, you can help generate a cover letter\n- In general, do your best to provide the user with accurate information with regards to them applying and obtaining a travel visa\n\nIf there is a chat history below, respond to the question below as a follow up question based on the context provided by the chat history. Otherwise, start a conversation based on the rules above\nQuestion:{question}\nChat History: {chat_history}"
        )
        ]
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

    answer = qa(question, messages)
    print(answer)
    ans = answer["answer"]

    user = f"user:{question}"
    ai = f"ai:{ans}"
    history.append(user)
    history.append(ai)

    response = {"answer": ans, "history": history}

    return jsonify(response)


app.run()