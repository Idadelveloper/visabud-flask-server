# visabud-flask-server
Handles requests to openAPI's chatGPT model about visa enquiries


### Installation
1. Create a Python virtual environment and activate it
2. Clone this repository and install all requirements in `requirements.txt`
3. Rename `example.env` to `.env` and add your OpenAI API key
4. Run `python main.py` on your terminal. The server is running on `http://127.0.0.1:5000`


### API Usage
There is multiple endpoints, all of which call OpenAI's GPT-3.5-Turbo model:
- `/questions`: Generates questions based on the user's country of origin and destination. These question are asked to the user one at a time in the chat interface
- `/suggestions`: Identifies weakpoints in the user's profile and suggests supporting document that can be used to strengthen their application
- `/cover`: Generates a custom visa cover letter based on the user's personal information. 
