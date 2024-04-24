import openai
import requests
import pandas as pd

#openai.api_key = "***"

filename = 'secure.csv'  
column_name = 'id'  
df = pd.read_csv(filename)
column_data = df[column_name].drop_duplicates().tolist()
column_data = column_data[:50]

pagesize=5
site="stackoverflow"


def getquestion_id(page):
    #get question_id from answer_id
    question_id = column_data[page]
    url = f'https://stackoverflow.com/a/{question_id}'
    response = requests.get(url, allow_redirects=True)
    final_url = response.url
    question_id = final_url.split('/')[4]
    return question_id

def getquestion(question_id):
    # print(question_id)
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
    
    content = f"""given a question and two answers, answer1 and answer2, give me a one word answer of which is better in terms of security, vulnerabiliity, bugs etc. 
    No explanation. just say 1 or 2 based on best answer.
    
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
    return answer
   

SO_count=0
GPT_count=0
for page in range(len(column_data)):
    # print(page)
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
    if analysis== "1":
        SO_count+=1
    elif analysis=="2":
        GPT_count+=1
    
    print("Question ID:", question_id, " - Winner: " , "StackOverFlow" if analysis== "1" else "Chat GPTGPT")
print()
print("Number of times StackOverFlow answer was better = ", SO_count)
print("Number of times Chat GPT answer was better = ", GPT_count)




