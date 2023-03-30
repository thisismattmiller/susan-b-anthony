import glob
import json
import os
import openai
import util
import re
import sys

from transformers import GPT2TokenizerFast
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text: str) -> int:
    """count the number of tokens in a string"""
    return len(tokenizer.encode(text))

openai.api_key = os.getenv("OPENAI_API_KEY")

if len(sys.argv[1:]) != 1:
	print("Pass what dir to work on, or 'all'")

work_on = sys.argv[1:][0]


for file in glob.glob('daybook-and-diaries-1856-1906-daybook-1*/*.json'):

	print(file)
	data = json.load(open(file))

	dir = file.split('/')[-2]
	file_id = int(file.split('/')[-1].replace('.json',''))
	data['id'] = file_id
	data['dir'] = dir


	if work_on != 'all':
		if work_on not in dir:
			print('skipping',dir)
			continue


	if 'full_text' in data:


		if 'gpt' not in data:
			data['gpt'] = {}

		# if 'gpt3.5-daybook-json' in data['gpt']:
		# 	continue
		
		if 'gpt4-daybook-json' in data['gpt']:
			continue

		full_text = util.clean_up_transcribed_text(data['full_text'])

		if len(full_text) < 80:
			continue

		print("WOrking on:",file)

		date = data['item']['date']
		print(date)


		prompt = f"""If the following text contains multiple journal entries, extract each one into an array of valid JSON dictionaries. Each dictionary represents one of the entries, extract the date and the date again in the format yyyy-mm-dd and the city or state it was written in and other geographical locations mentioned that entry and people mentioned that entry and the complete full text of the entry and a one sentence summary of the text, using the JSON keys dateText, dateFormated, cityOrState, geographicalLocations, people, fullText, summaryText: 
		{full_text}
		"""

		response = openai.ChatCompletion.create(
			# model="gpt-3.5-turbo",
			
			model="gpt-4",
			temperature=0,
			frequency_penalty=0,
			presence_penalty=0,
			messages=[
			      {"role": "system", "content": f"You are a helpful assistant that is summarizing and extracting data from a journal written by Susan B. Anthony in {date}. You only answer using the text given to you. You do not make-up additional information, the answer has to be contained in the text provided to you. Each page is a diary entry or financial bookkeeping. You will structure your answer in valid JSON, if there are any quote marks in the content escape them as &quot;."},
			      {"role": "user", "content": prompt}     
			  ]
		)

		escaped_json = response['choices'][0]['message']['content']

		# remove any trailing commas on the dictonary
		escaped_json = re.sub(r'",\n\s*}', '"\n}', escaped_json)
		# remove some bad escaped chars
		escaped_json = re.sub(r'\\xa[0-9]+', '', escaped_json)

		# remove any escapes that are not \n newline escape
		escaped_json = re.sub(r'\\[a-m]', '', escaped_json)
		escaped_json = re.sub(r'\\[o-z]', '', escaped_json)
		escaped_json = re.sub(r'\\[0-9]', '', escaped_json)

		escaped_json = re.sub(r'```(json)?', '', escaped_json)



		if escaped_json == 'There are no journal entries in this text. This is a table of stamp duties and telegraphic dispatch charges.':
			continue

		if "[{}] (There is no journal entry in the provided text)" in escaped_json:
			continue
		if "[{}] (There is no journal entry in the text provided)" in escaped_json:
			continue
		if "There is no journal entry in the provided text. It appears to be financial bookkeeping." in escaped_json:
			continue			
		if "[{}] (empty array as there is no journal entry in the text provided)" in escaped_json:
			continue
		if "[{}] (empty array as there is no valid journal entry in the text)" in escaped_json:
			continue
		if "[{}]" in escaped_json:
			continue
		if "There is no journal entry in the provided text." in escaped_json:
			continue
		if "There are no journal entries in this text" in escaped_json:
			continue
		if "There is no journal entry provided in the text." in escaped_json:
			continue




		# cutt off anything extra at the end of the json
		if '}]' in escaped_json:
			escaped_json = escaped_json.split('}]')[0]
			escaped_json = escaped_json + '}]'


		try:
			daybook_data = json.loads(escaped_json)
			# data['gpt']['gpt3.5-daybook-json'] = daybook_data
			data['gpt']['gpt4-daybook-json'] = daybook_data
		except:

			print('---fulltext---')
			print(full_text)
			print('--------------')    
			print('---escaped_json---')
			print(escaped_json)
			print('---orginal json---')			
			print(response['choices'][0]['message']['content'])
			print('--------------')  
			print(response)

			if response['choices'][0]['finish_reason'] == 'length':

				print("length too long, skipping")
				continue

			if response['choices'][0]['finish_reason'] == 'content_filter':

				print("hit a content_filter error, skipping")
				continue



			sys.exit()


		


		# prompt = f"Using only the text below. Structure the following multiple diary text entries by Susan B Anthony into a valid JSON array of dictionaries extracting the date, the date again in the format yyyy-mm-dd, the city or state it was written in, other geographical locations mentioned that day, people mentioned that day, and the complete full text of the entry and a one sentence summary of the text, using the JSON keys date, dateFormated, cityOrState, geographical, people, and fullText, summaryText:\n\n---\n{full_text}\n---\n"
		# print('----PROMT----')
		# print(prompt)
		# response = openai.Completion.create(
		#   model="text-davinci-003",
		#   prompt=prompt,
		#   temperature=0.0,
		#   max_tokens=4096 - count_tokens(prompt),
		#   top_p=1,
		#   frequency_penalty=0,
		#   presence_penalty=0
		# )
		# print("response['choices'][0]")
		# print(response['choices'][0])

		# text_response=response['choices'][0]['text']

		# print('---------text_response before=========')
		# print(text_response)

		# if response['choices'][0]['finish_reason'] == "length":
		# 	print('daybook-length-too-long')
		# 	data['gpt']['error'] = 'daybook-length-too-long'
		# 	continue

		# if text_response.find('[') == -1:
		# 	data['gpt']['error'] = 'daybook-json'
		# else:



		# 	# trim off any extra (? why) text before the structured data
		# 	if text_response.find('[') > 0:
		# 		text_response = text_response[text_response.find('[')-1:].strip()	

			
		# 	text_response = text_response.replace('\\\\',"")
		# 	text_response = text_response.replace('\\"',"'")
		# 	text_response = text_response.replace('("',"(")
		# 	text_response = text_response.replace('")',")")
		# 	text_response = text_response.replace('"-',"'")



		# 	text_response = text_response.replace('""','')
		# 	text_response = text_response.replace('`','')
		# 	text_response = text_response.replace('JSON:','')
		# 	text_response = text_response.replace('[JSON]','')


			
		# 	text_response = text_response.replace('// etc.','')
		# 	text_response = text_response.replace('// and so on...','')
		# 	text_response = text_response.replace('// ...','')


		# 	text_response = text_response.replace('"cityOrState": ,','"cityOrState": null,')
		# 	text_response = text_response.replace('"dateFormatted": ,','"dateFormatted": null,')
		# 	text_response = text_response.replace('"dateFormated": ,','"dateFormated": null,')
		# 	text_response = text_response.replace('"geographical": ,','"geographical": null,')
		# 	text_response = text_response.replace('"date": ,','"date": null,')
		# 	text_response = text_response.replace('"people": ,','"people": null,')
		# 	text_response = text_response.replace('"dateFormated": ,','"dateFormated": null,')
		# 	text_response = text_response.replace('"fullText": ,','"fullText": null,')
		# 	text_response = text_response.replace('"summaryText":\n','"summaryText": null\n')
		# 	text_response = text_response.replace('"summaryText": \n','"summaryText": null\n')

		# 	text_response=text_response.strip()

		# 	# remove any trailing }, that are there
		# 	text_response = re.sub(r'},\n\s*\n\]', '}]', text_response)			



		# 	# find the fulltext part
		# 	fulltext_searches = re.finditer(r'"fullText"\:(.*)', text_response, re.IGNORECASE)
		# 	fulltext_searches_findall = re.findall(r'"fullText"\:(.*)', text_response, re.IGNORECASE)
		# 	print('-------text_response after replace cleanup')
		# 	print(text_response)
		# 	print('------')
		# 	print("fulltext:")
		# 	print("fulltext_searches",list(fulltext_searches))
		# 	print('fulltext_searches_findall',fulltext_searches_findall)

		# 	if len(list(fulltext_searches_findall)) == 0:
		# 		print("fulltext_search failed, try on next run")
		# 		continue

		# 	for fulltext_search in fulltext_searches_findall:
		# 		print('fulltext_search',fulltext_search)

		# 		if fulltext_search.strip() == 'null,':
		# 			continue

		# 		replace_with = fulltext_search
		# 		replace_with = replace_with.replace("\\",'')
		# 		replace_with = replace_with.replace('"','')
		# 		replace_with = replace_with.replace('\ ','')


		# 		replace_with = f'"{replace_with}",'

		# 		print("Replacing with:",replace_with)

		# 		text_response = text_response.replace(fulltext_search,replace_with)

		# 	print('------text_response post fulltext regex')
		# 	print(text_response)
		# 	# # pull out the geographical key and parse it, if it fails nuke it, its too complicated to parse why a json array could be malformed
		# 	# geo_search = re.search(r'"geographical"\:(.*)', text_response, re.IGNORECASE)

		# 	# geo_text = geo_search.group(1).strip()
		# 	# if geo_text[-1] == ',':
		# 	# 	geo_text = geo_text[0:-1].strip()

			
		# 	# try:
		# 	# 	json.loads(geo_text)
		# 	# except:
		# 	# 	print(text_response)
		# 	# 	print("geographical parse failed, setting it to empty")
		# 	# 	text_response = text_response.replace(geo_search.group(1),'[],')



		# 	print('---------')
		# 	print(text_response)		
		# 	print('---------')
		# 	jsonResponse = json.loads(text_response)			
		# 	data['gpt']['daybook-json'] = jsonResponse

			
	
	json.dump(data,open(file,'w'),indent=2)