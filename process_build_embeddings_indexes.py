import pickle
import glob
import json
import util


total_daybook = len(list(glob.glob('daybook-and-diaries-1856-1906-daybook-1*/*.json')))
done_counter = 0
index={}
for file in glob.glob('daybook-and-diaries-1856-1906-daybook-1*/*.json'):
    done_counter+=1
    print(done_counter, '/',total_daybook)
    dir = file.split('/')[-2]
    file_id = int(file.split('/')[-1].replace('.json',''))

    data = json.load(open(file))
    if 'gpt' in data:
        if 'gpt3.5-daybook-json' in data['gpt']:
            counter=0
            for entry in data['gpt']['gpt3.5-daybook-json']:
                counter+=1
                if 'embedding' in entry:

                    digital_id = data['options']['digital_id']

                    print(digital_id,f"{file_id}_{counter}")
                    index[("daybooks",digital_id,f"{file_id}_{counter}")] = entry['embedding']

file = open('daybook-and-diaries-1856-1906.pickle', 'wb')
pickle.dump(index, file)
file.close()

index = {}
total_writtings = len(list(glob.glob('anthony-speeches-and-other-writings-resources/*.json')))
done_counter = 0

for file in glob.glob('anthony-speeches-and-other-writings-resources/*.json'):

    done_counter+=1
    print(done_counter, '/',total_writtings)
    print(file)
    data = json.load(open(file))
    for block in data:

        pages = []
        digital_id = None
        for item in block['items']:
            digital_id = item['options']['digital_id']

            pages.append(str(item['id']))


        print(digital_id,pages)
        index[("writings",digital_id,"_".join(pages))] = block['embedding']

file = open('anthony-speeches-and-other-writings-resources.pickle', 'wb')
pickle.dump(index, file)
file.close()


total_writtings = len(list(glob.glob('anthony-correspondence-resources/*.json')))
done_counter = 0
index = {}
for file in glob.glob('anthony-correspondence-resources/*.json'):

    done_counter+=1
    print(done_counter, '/',total_writtings)
    print(file)
    file_id = file.split('/')[-1].replace('.json','')

    data = json.load(open(file))
    if 'embedding' in data:

        pages = []
        digital_id = None
        for item in data['items']:
            digital_id = item['options']['digital_id']
            pages.append(str(item['id']))

        
        print((digital_id,"_".join(pages)))

        index[('correspondence',digital_id,"_".join(pages))] = data['embedding']


file = open('anthony-correspondence-resources.pickle', 'wb')
pickle.dump(index, file)
file.close()


