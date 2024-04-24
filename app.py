from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import requests
import pandas as pd

app = Flask(__name__)
CORS(app) 


# GPT credentials
#openai.api_key = "***"
conversation_history = []
conversation_history.append({"role": "system", "content": "You are a helpful assistant."})

#Data file
filename = 'secure.csv'  
column_name = 'id'  
df = pd.read_csv(filename)
column_data = df[column_name].drop_duplicates().tolist()

pagesize=5
site="stackoverflow"
    
    
@app.route('/problems', methods=['GET'])
def direct():
    
    page = request.args.get('page', default=1, type=int)
    print(page)
    question_id = getquestion_id(page)
    qn_list=getquestion(question_id)
    question={
    "title":qn_list[0],
    "body":qn_list[1]
    }
    question_body = question["body"]
    so_answer= getso_answer(question_id)
    gpt_answer = getGPT_answer(question["title"], question["body"])
    analysis = get_analysis(question_body, so_answer,gpt_answer)
    response_data = {
    "id": question_id,
    "left": so_answer,
    "right": gpt_answer,
    "title": question["title"],
    "body": question["body"],
    "analysis": analysis
    }
    
    return jsonify(response_data)

def getquestion_id(page):
    #get question_id from answer_id
    question_id = column_data[page-1]
    url = f'https://stackoverflow.com/a/{question_id}'
    response = requests.get(url, allow_redirects=True)
    final_url = response.url
    question_id = final_url.split('/')[4]
    return question_id

def getquestion(question_id):
    print(question_id)
    qn = f"https://api.stackexchange.com/2.2/questions/{question_id}?site=stackoverflow&filter=!9_bDE(fI5"
    response = requests.get(qn)
    data = response.json()['items']
    #print("\n Title: ", data[0]['title'])
    #get body of qn
    qn_body = f"https://api.stackexchange.com/2.2/questions/{question_id}?&site=stackoverflow&filter=withbody"
    qn_body = requests.get(qn_body)
    qn_body = qn_body.json()['items'] if qn_body.status_code == 200 else []
    #print("\n Question: ", qn_body[0]['body'])
    return [data[0]['title'], qn_body[0]['body']]

def getso_answer(question_id):
    
    answer_body = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers?order=desc&sort=votes&site={site}&pagesize={pagesize}&filter=withbody"  
    answer_body = requests.get(answer_body)
    answer_body = answer_body.json()['items'] if answer_body.status_code == 200 else []
    #print("\n Answer: ", answer_body[0]['body'])
    return answer_body[0]['body']

def getGPT_answer(title, question):
    
    content = f"Title: {title}\n Question: {question}."


    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # This specifies the model you're using
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": content}
    ]
    )
    
    return response.choices[0].message['content'].strip()

def get_analysis(question_body, so_answer, gpt_answer):
    
    content = f"""given a question and two answers, answer1 and answer2, give me an answer of which is better in terms of security, vulnerability, bugs etc... Say "StackOverFlow answer is better" if Answer1 is better, else say "Chat GPT answer is better' if Answer2. 
    Also give a 1 sentence answr on why it is better.
    
    Question:
    {question_body}
    
    Answer1:
    {so_answer}
    
    Answer2:
    {gpt_answer}
    """
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # This specifies the model you're using
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": content}
    ]
    )

    answer = response.choices[0].message['content'].strip()
    print(answer)
    return answer


if __name__ == '__main__':
    app.run(debug=True)
