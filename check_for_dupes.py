import glob
import json

check={}
for file in glob.glob('daybook-and-diaries-1856-1906-daybook-1*/*.json'):

	data = json.load(open(file))
	if 'full_text' in data:
		if data['full_text'] in check:
			print("Dupe!!!",file)
			print(data['full_text'])
			print(check[data['full_text']])
		else:
			check[data['full_text']] = file


		print(data['full_text'])
		print('-----')