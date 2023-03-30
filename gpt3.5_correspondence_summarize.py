import os
import openai
import glob
import json
import util
import sys

from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")


openai.api_key = os.getenv("OPENAI_API_KEY")

def count_tokens(text: str) -> int:
    """count the number of tokens in a string"""
    return len(tokenizer.encode(text))



page_order = json.load(open('group-ui-util/anthony-correspondence-id-sets.json'))

for resource in glob.glob('anthony-correspondence-resources/*.json'):
  print(resource)
  
  data = json.load(open(resource))

  if 'gpt' not in data:
    data['gpt'] = {}

  if 'summarized-gpt3.5' in data['gpt']:
    continue

  full_text = data['full_text']



  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0,
    frequency_penalty=0,
    presence_penalty=0,
    messages=[
          {"role": "system", "content": "You are a helpful assistant that is summarizing and extracting data from letters written to and from Susan B. Anthony. You only answer using the text given to you. You do not make-up additional information, the answer has to be contained in the text provided to you. You will structure your answer in valid JSON, if there are any quote marks in the content escape them as &quot;."},
          {"role": "user", "content": f"""Extract who this letter was sent to and who it was sent from and on what date using value from the text and on what date in the format yyyy-mm-dd and from what city if not possible use "unknown" and summarize the contents in four sentences and summarize the contents in three sentences and and summarize the contents in two sentences and and summarize the contents in one sentence and extract the names of the people mentioned as an array. Use the JSON dictonary keys recipient, sender, dateOrginal, dateFormated, sentFrom, summerized4Sentences, summerized3Sentences, summerized2Sentences, summerized1Sentences, peopleMentioned:
          {full_text}
          """}       
      ]
  )



  escaped_json = response['choices'][0]['message']['content']

  try:
    letter_data = json.loads(escaped_json)
  except:

    print('---fulltext---')
    print(full_text)
    print('--------------')    
    print('---escaped_json---')
    print(escaped_json)
    print('--------------')  


    sys.exit()


  data['gpt']['summarized-gpt3.5'] = letter_data
  json.dump(data,open(resource,'w'),indent=2)



  # if 'correspondence-summarize-4-sentences' in data['gpt']:
  #   continue

  # 

  # response = openai.Completion.create(
  #   model="text-davinci-003",
  #   prompt=f"Using who this letter was sent to, who it was sent from, on what date in the format yyyy-mm-dd, summarize the contents in four sentences, and extract the names of the people mentioned using the dictonary keys recipient, sender, date, contents, peopleMentioned:\n---\n{full_text}\n---\n",
  #   temperature=0.25,
  #   max_tokens=506,
  #   top_p=1,
  #   frequency_penalty=0,
  #   presence_penalty=0
  # )

  # data['gpt']['correspondence-summarize-4-sentences'] = response['choices'][0]
  
  
  json.dump(data,open(resource,'w'),indent=2)

