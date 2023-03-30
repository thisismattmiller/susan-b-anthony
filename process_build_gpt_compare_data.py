import glob
import json
import os

# try:
#     os.mkdir('docs/json/compare/')    
# except:
#     pass


total =0
complete = 0
all_data={}
for file in glob.glob('daybook-and-diaries-1856-1906-daybook-1*/*.json'):

	data = json.load(open(file))
	if 'full_text' in data:



		dir = file.split('/')[-2]
		dir = dir.replace('daybook-and-diaries-1856-1906-daybook-','')

		if dir not in all_data:
			all_data[dir] = []


		if 'gpt' in data:

			if 'daybook-json' in data['gpt'] and 'gpt3.5-daybook-json' in data['gpt'] and 'gpt4-daybook-json' in data['gpt']:



				print(file)
				most_entries = max([len(data['gpt']['daybook-json']),len(data['gpt']['gpt3.5-daybook-json']),len(data['gpt']['gpt4-daybook-json'])])
				min_entries = min([len(data['gpt']['daybook-json']),len(data['gpt']['gpt3.5-daybook-json']),len(data['gpt']['gpt4-daybook-json'])])
				file_data_meta = {
					'most_entries': most_entries,
					'digital_id' : data['options']['digital_id'],
					'page' : data['id'],
					'3':[],
					'3.5':[],
					'4':[]
				}



				if isinstance(data['gpt']['daybook-json'], dict) == True:
					continue
				if isinstance(data['gpt']['gpt3.5-daybook-json'], dict) == True:
					continue
				if isinstance(data['gpt']['gpt4-daybook-json'], dict) == True:
					continue

				for idx in range(0,most_entries):

					for gpt in ['daybook-json','gpt3.5-daybook-json','gpt4-daybook-json']:

						geokey = 'geographicalLocations'

						if gpt == 'daybook-json':
							add_to = '3'
							geokey = 'geographical'
						if gpt == 'gpt3.5-daybook-json':
							add_to = '3.5'
						if gpt == 'gpt4-daybook-json':
							add_to = '4'

						# print(gpt)
						# print(most_entries,min_entries)
						# print(data['gpt'][gpt])
						# print(file)
						# print('------')
						if 0 <= idx < len(data['gpt'][gpt]):
		

							add = {
								'cityOrState': data['gpt'][gpt][idx]['cityOrState'],
								'geographicalLocations': data['gpt'][gpt][idx][geokey],
								'people': data['gpt'][gpt][idx]['people'],
								'fullText': data['gpt'][gpt][idx]['fullText'],
								'dateFormated': None,
								'summaryText': None								
							}

							if 'summaryText' in data['gpt'][gpt][idx]:
								add['summaryText'] = data['gpt'][gpt][idx]['summaryText']
							# else:
							# 	print('no summary')
							# 	print(data['gpt'][gpt][idx])

							if 'dateFormatted' in data['gpt'][gpt][idx]:
								add['dateFormated'] = data['gpt'][gpt][idx]['dateFormatted']
								
							if 'dateFormated' in data['gpt'][gpt][idx]:
								add['dateFormated'] = data['gpt'][gpt][idx]['dateFormated']




							file_data_meta[add_to].append(add)
						else:
							file_data_meta[add_to].append(False)

				
				# print(file_data_meta)

				all_data[dir].append(file_data_meta)

		# print(all_data)
final={}
for x in all_data:
	print(x,len(all_data[x]))
	if len(all_data[x]) != 0:
		final[x] = all_data[x]


json.dump(final,open('docs/json/compare.json','w'))
