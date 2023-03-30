import glob
import json

total =0
complete = 0
count={}
for file in glob.glob('daybook-and-diaries-1856-1906-daybook-1*/*.json'):

	data = json.load(open(file))
	if 'full_text' in data:



		dir = file.split('/')[-2]
		if dir not in count:
			count[dir] = {'done':0,'total':0}

		count[dir]['total']+=1


		total+=1
		if 'gpt' in data:

			# if 'gpt3.5-daybook-json' in data['gpt']:
			if 'gpt4-daybook-json' in data['gpt']:

					
				complete+=1
				count[dir]['done']+=1


print(complete,'/',total)
for x in count:
	print(x, count[x])
