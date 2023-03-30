import glob
import json
from collections import Counter

# all_salutation = []
all_pages = []
for x in range(1,228):

	file = f'anthony-correspondence/{x}.json'
	print(f'doing {file}')
	data = json.load(open(file))


	if 'full_text' in data:
		text = data['gpt']['correspondence-headers']['text']

		# remove anything before the JSON {
		text = '{' + text.split('{')[1]

		response= json.loads(text)
		# print(response['date'], '-----', response['salutation']) 

		# all_salutation.append(response['salutation'])



		all_pages.append({
			'id':x,
			'img': data['page'][0]['url'],
			'date':response['date'],
			'salutation' : response['salutation'],
			'text': data['full_text']

		})

print(all_pages)

json.dump(all_pages,open('group-ui-util/anthony-correspondence.json','w'),indent=2)

# print(dict(sorted(Counter(all_salutation).items(), key=lambda item: item[1])))

