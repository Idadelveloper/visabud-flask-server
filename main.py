import os
import ast
from dotenv import load_dotenv
import openai

from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify

import json
import requests


app = Flask(__name__)
CORS(app)

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_content(response):
    json_object = response["choices"][0]
    answer = json_object["message"]["content"]
    return answer 

def suggest_visa(content):
    need_visa_question = content + " Do I need a visa? Give me a one-letter yes (Y) or no (N) answer"
    messages = [
        {"role": "system", "content": need_visa_question},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    need_visa = get_content(response)

    if need_visa == "Y":
        visa_explain_question = content + ". Tell me the name of the visa I need without any explaination"
    else:
        visa_explain_question = content + ". Explain why I don't need a visa"
    messages = [
            {"role": "system", "content": visa_explain_question},
        ]
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )
    visa_explain = get_content(response)
    # print(need_visa_question, visa_explain_question)
    # print([True, visa_explain])
    if need_visa == "Y":
        return {
            'need_visa' : True,
            'explain': visa_explain
        }
    else:
        return {
            'need_visa' : False,
            'explain': visa_explain
        }



# p1 = "My country of origin is USA. My country of destination is Canada. My reason of travel is to visit a friend. "
# p2 = "My country of origin is Cameroon. My country of destination is Canada. My reason of travel is to visit a friend. "
# print(suggest_visa(p1))
# print(suggest_visa(p2))

@app.route("/init", methods=["POST"])
def init():
    data = request.json
    initial_context = "You are a kind helpful assistant chatbot. Your job is to assist people applying for visa to travel abroad."
    context = initial_context + data['info']
    res = suggest_visa(context)
    return jsonify(res)

@app.route("/questions", methods=["POST"])
def questions():
    context = request.json.get("context")
    context += " What personal information do you need from me to be able to assist me? Provide a list of questions. If I have already provided an answer to a question (e.g purpose of my visit), do not ask again. Do not ask any identifying questions like my name, date of birth or passport number. Do not ask about criminal or medical history. Think about the requirements for the specific visa and common pitfalls that cause visas to be rejected when generating the questions. Be specific as possible; for example, instead of asking if I have enough funds, ask how much money my bank statement has, or instead of asking if I have  documents to prove my ties, ask me questions that can be used to determine my ties (e.g marital status, number of kids, property, employment status, whether I'm travelling alone or not). Research about the supporting documents and immigration regulations for this specific visa type and use as a guide for the questions, making sure to ask questions only relevant to this visa type. If a question isn't relevant, do not ask it. No questions about application formalities like application forms, feed, passport photos. Response should be a list of questions in Python array format"
    
    messages = [
    {
        "role": "system",
        "content": context,
    },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    questions = get_content(response)
    questions = ast.literal_eval(questions)
    first_text = "You have provided some information. I'll ask a few questions to help you. Type anything to get started."
    response = {"first": first_text, "answer": questions}
    return jsonify(response)

@app.route("/suggestions", methods=["POST"])
def suggestions():
    data = request.json
    questions = data["questions"]
    answers = data["answers"]
    context = "Here is a Python list of question-answer pairs in the form 'question: answer', which provide context on my personal background:\n"
    length = min(len(questions), len(answers))
    for i in range(length):
        context += questions[i] + ": " + answers[i] + " \n"
    context += "Research about the requirements and official immigrations regulations/rules (of the country I'm applying for) for the specific visa I'm applying for. List out  these immigration rules, and alongside each rule, either tell me how my background satisfies this rule or suggest supporting documents that might make my application stronger. If my personal background shows that my visa is likely to be rejected due to not fufilling an immigration rule, let me know. Make suggestions of supporting documents based on my background provided in the question-answer pairs"
    
    messages = [
    {
        "role": "system",
        "content": context,
    },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    response = get_content(response)
    response = {"answer": response}
    return jsonify(response)

@app.route("/cover", methods=["POST"])
def cover():
    data = request.json
    questions = data["questions"]
    answers = data["answers"]
    context = "Here is a Python list of question-answer pairs in the form 'question: answer', which provide context on my personal background:\n"
    length = min(len(questions), len(answers))
    for i in range(length):
        context += questions[i] + ": " + answers[i] + " \n"
    context += "Research about the requirements and official immigrations regulations/rules (of the country I'm applying for) for the specific visa I'm applying for. Use this information and my personal background information to generate a visa cover letter for me that specifies the purpose of my visit and specifies how I satisfy the immigration rules. This letter should convince the visa offer that I am genuine and reduce the chance of a visa rejection"
    
    messages = [
    {
        "role": "system",
        "content": context,
    },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    response = get_content(response)
    response = {"answer": response}
    return jsonify(response)

app.run(debug=True)
