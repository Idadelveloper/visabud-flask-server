# visabud-flask-server
Handles requests to openAPI's chatGPT model about visa enquiries


### Installation
1. Create a Python virtual environment and activate it
2. Clone this repository and install all requirements in `requirements.txt`
3. Rename `example.env` to `.env` and add your OpenAI API key
4. Run `python main.py` on your terminal. The server is running on `http://127.0.0.1:5000`


### API Usage
There is one endpoint - `/enquire`
There are 2 parameters to include in the request body:
- `question`: Current question you intend asking
- `history`: A list of of strings of the previous questions and answers

#### Sample json request body (with no history)
```json
{
    "question": "I want to apply for a tourist visa to visit London for 3 months. How much will the visa application cost? Also what can I do to obtain a visa?",
    "history": []
}
```

#### Sample json request body (with history)
```json
{
    "question": "Please provide me with steps and some tips to submit a successful application",
    "history": [
        "user:I want to apply for a tourist visa to visit London for 3 months. How much will the visa application cost? Also what can I do to obtain a visa?",
        "ai:The cost to apply for a Standard Visitor visa to the UK, which includes London, is £100 for up to 6 months. The steps to obtain it are as follows:\n\n1. Apply online before you travel to the UK.\n2. Attend an appointment at a visa application centre.\n3. You must meet the eligibility requirements and only do permitted activities.\n4. Depending on your nationality, you may not need a visa to visit the UK. You can check if you need a visa before you apply.\n\nPlease note that the earliest you can apply is 3 months before you travel."
    ]
}
```