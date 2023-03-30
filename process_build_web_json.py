import glob
import json
import util
import os

try:
    os.mkdir('docs')    
except:
    pass

try:
    os.mkdir('docs/json')    
except:
    pass
try:
    os.mkdir('docs/json/daybooks')    
except:
    pass

all_index = {
    'daybooks':[],
    'writings':[],
    'correspondence':'correspondences.json'
}

dirs = sorted(list(glob.glob('daybook-and-diaries-1856-1906-daybook-1*/')))

dir_lookup = {}

for d in dirs:

    files = list(glob.glob(f'{d}/*.json'))
    order = []
    for file in files:
        order.append(int(file.split('/')[-1].replace('.json','')))
    order=sorted(order)
    dir_lookup[d] = order


for d in dir_lookup:


    all_cityOrState = {}
    all_people = {}
    all_geographicalLocations = {}
    all_data = {
        'digital_id':None,
        'title':None,
        'date':None,
        'facets':{
            'writtenFrom':{},
            'people':{},
            'locations':{}
        },
        'entries':[]
    }

    for file_id in dir_lookup[d]:


        print(file_id)

        data = json.load(open(f"{d}/{file_id}.json"))
        digital_id = data['options']['digital_id']

        all_data['digital_id'] = digital_id

        if 'created_published' in data['item']:
            all_data['date'] = data['item']['created_published'][0]
        else:
            all_data['date'] = data['item']['date']


        all_data['title'] = data['item']['item']['title']


        if 'gpt' in data:
            if 'gpt3.5-daybook-json' in data['gpt']:
                counter=0
                for entry in data['gpt']['gpt3.5-daybook-json']:
                    counter+=1

                    entry['digital_id'] = digital_id
                    entry['file_id'] = file_id




                    if isinstance(entry['geographicalLocations'],str):
                        entry['geographicalLocations'] = entry['geographicalLocations'].split(',')

                 
                    if isinstance(entry['people'],str):
                        entry['people'] = entry['people'].split(',')

                    if entry['geographicalLocations'] != None:
                        entry['geographicalLocations'] = [e.strip() for e in entry['geographicalLocations']]

                        for x in entry['geographicalLocations']:
                            x=x.strip()
                            if x == '':
                                continue

                            if x not in all_geographicalLocations:
                                all_geographicalLocations[x] = 0
                            all_geographicalLocations[x]=all_geographicalLocations[x]+1

                    if entry['people'] != None:

                        entry['people'] = [e.strip() for e in entry['people']]

                        for x in entry['people']:
                            x=x.strip()
                            if x == '':
                                continue
                            if x not in all_people:
                                all_people[x] = 0
                            all_people[x]=all_people[x]+1

                            if all_data['date'] == '1878':
                                if x == 'Frank':
                                    print(entry['people'])

                    if entry['cityOrState'] != None and entry['cityOrState'] != '' and '\n' not in entry['cityOrState']:
                        if entry['cityOrState'] not in all_cityOrState:
                            all_cityOrState[entry['cityOrState']] = 0
                        
                        all_cityOrState[entry['cityOrState']]=all_cityOrState[entry['cityOrState']]+1



                    this_index = ("daybooks",digital_id,f"{file_id}_{counter}")

                    if 'embedding' in entry:
                        del entry['embedding']



                    
                    

                    
                    entry['page'] = data['page'][0]['url']

                    entry['entry_id'] = counter
                    entry['file_id'] = file_id
                    entry['digital_id'] = digital_id

                    all_data['entries'].append(entry)
                    json.dump(entry,open('docs/json/daybooks/'+"_".join(this_index)+'.json','w'))


    all_index['daybooks'].append({
        'file':'daybooks_'+all_data['date'].replace(' ','_')+'.json',
        'title':all_data['title'],
        'date':all_data['date']
    })


    all_data['facets']['writtenFrom'] = all_cityOrState
    all_data['facets']['locations'] = all_geographicalLocations
    all_data['facets']['people'] = all_people

    json.dump(all_data,open('docs/json/daybooks_'+all_data['date'].replace(' ','_')+'.json','w'))




index = {}
total_writtings = len(list(glob.glob('anthony-speeches-and-other-writings-resources/*.json')))
done_counter = 0

all_index['writingsToDigitalId'] = {}
for file in glob.glob('anthony-speeches-and-other-writings-resources/*.json'):

    done_counter+=1
    print(done_counter, '/',total_writtings)
    print(file)
    data = json.load(open(file))
    blocks = []

    all_data = {
        'blocks' : []
    }

    for block in data:
        pages = []
        digital_id = None
        for item in block['items']:
            if 'created_published' in item['item']:
                all_data['date'] = item['item']['created_published'][0]
            else:
                all_data['date'] = item['item']['date']
            all_data['title'] = item['item']['item']['title']


            digital_id = item['options']['digital_id']
            pages.append(str(item['id']))

        this_index = ("writings",digital_id,"_".join(pages))

        all_data['blocks'].append({
            'text':block['text'],
            'similar':block['similar'],
            'digital_id': digital_id,
            'pages': "_".join(pages)
        })

    all_index['writings'].append({
        'file':'writings_'+"_".join(pages)+'.json',
        'title':all_data['title'],
        'date':all_data['date']
    })

    all_index['writingsToDigitalId']['writings_'+"_".join(pages)+'.json'] = digital_id

    json.dump(all_data,open('docs/json/writings_'+"_".join(pages)+'.json','w'))















total_writtings = len(list(glob.glob('anthony-correspondence-resources/*.json')))
done_counter = 0
index = {}
all_data = {
    'facets': {},
    'letters':[]
}
all_people = {}
all_recipient = {}
all_sender={}
all_sentFrom={}
for file in glob.glob('anthony-correspondence-resources/*.json'):

    done_counter+=1
    print(done_counter, '/',total_writtings)
    print(file)
    file_id = file.split('/')[-1].replace('.json','')

    data = json.load(open(file))

    letter = data['gpt']['summarized-gpt3.5']

    pages = []
    digital_id = None
    for item in data['items']:
        digital_id = item['options']['digital_id']
        pages.append(str(item['id']))

        if 'created_published' in item['item']:
            letter['date'] = item['item']['created_published'][0]
        else:
            letter['date'] = item['item']['date']


        letter['title'] = item['item']['item']['title']

    
    this_index = (digital_id,"_".join(pages))

    letter['index'] = this_index
    letter['digital_id'] = digital_id
    letter['pages'] = pages


    letter['similar'] = data['similar']

    if letter['recipient'] != None and letter['recipient'] != '' and '\n' not in letter['recipient']:
        if letter['recipient'] not in all_recipient:
            all_recipient[letter['recipient']] = 0
        
        all_recipient[letter['recipient']]+=1
    if letter['sender'] != None and letter['sender'] != '' and '\n' not in letter['sender']:
        if letter['sender'] not in all_sender:
            all_sender[letter['sender']] = 0
        
        all_sender[letter['sender']]+=1

    if letter['sentFrom'] != None and letter['sentFrom'] != '' and '\n' not in letter['sentFrom']:
        if letter['sentFrom'] not in all_sentFrom:
            all_sentFrom[letter['sentFrom']] = 0
        
        all_sentFrom[letter['sentFrom']]+=1



    if letter['peopleMentioned'] != None:
        for x in letter['peopleMentioned']:
            x=x.strip()
            if x == '':
                continue
            if x not in all_people:
                all_people[x] = 0
            all_people[x]+=1

    all_data['letters'].append(letter)

all_data['facets']['people'] = all_people
all_data['facets']['all_recipients'] = all_recipient
all_data['facets']['all_senders'] = all_sender
all_data['facets']['sent_from'] = all_sentFrom


json.dump(all_data,open('docs/json/correspondences.json','w'))



json.dump(all_index,open('docs/json/index.json','w'))

