import pickle
import glob
import json
import util
import numpy as np

def vector_similarity(x: list[float], y: list[float]) -> float:
    """
    Returns the similarity between two vectors.
    
    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))


daybook_embeddings_file = open('daybook-and-diaries-1856-1906.pickle', 'rb')
daybook_embeddings = pickle.load(daybook_embeddings_file)
daybook_embeddings_file.close()

writings_embeddings_file = open('anthony-speeches-and-other-writings-resources.pickle', 'rb')
writings_embeddings = pickle.load(writings_embeddings_file)
writings_embeddings_file.close()

correspondence_embeddings_file = open('anthony-correspondence-resources.pickle', 'rb')
correspondence_embeddings = pickle.load(correspondence_embeddings_file)
correspondence_embeddings_file.close()



total_daybook = len(list(glob.glob('daybook-and-diaries-1856-1906-daybook-1*/*.json')))
done_counter = 0
index={}
for file in glob.glob('daybook-and-diaries-1856-1906-daybook-1*/*.json'):

    done_counter+=1
    print(done_counter, '/',total_daybook)
    print(file)
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



                    this_index = ("daybooks",digital_id,f"{file_id}_{counter}")
                    entry['similar'] = {}
                    print(this_index)

                    query_embedding = entry['embedding']
                    
                    document_similarities = sorted([
                        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in daybook_embeddings.items()
                    ], reverse=True)
                    
                    
                    entry['similar']['daybook'] = document_similarities[1:20]

                    document_similarities = sorted([
                        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in writings_embeddings.items()
                    ], reverse=True)

                    entry['similar']['writings'] = document_similarities[0:10]

                    document_similarities = sorted([
                        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in correspondence_embeddings.items()
                    ], reverse=True)

                    entry['similar']['correspondence'] = document_similarities[0:10]


    json.dump(data,open(file,'w'),indent=2)







index = {}
total_writtings = len(list(glob.glob('anthony-speeches-and-other-writings-resources/*.json')))
done_counter = 0

for file in glob.glob('anthony-speeches-and-other-writings-resources/*.json'):

    done_counter+=1
    print(done_counter, '/',total_writtings)
    print(file)
    data = json.load(open(file))
    for block in data:

        if 'embedding' in block:

            pages = []
            digital_id = None
            for item in block['items']:
                digital_id = item['options']['digital_id']

                pages.append(str(item['id']))

            this_index = ("writings",digital_id,"_".join(pages))

            block['similar'] = {}


            query_embedding = block['embedding']
            
            document_similarities = sorted([
                (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in daybook_embeddings.items()
            ], reverse=True)
            
            
            block['similar']['daybook'] = document_similarities[0:20]

            document_similarities = sorted([
                (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in writings_embeddings.items()
            ], reverse=True)
            print(document_similarities[0])
            block['similar']['writings'] = document_similarities[1:20]

            document_similarities = sorted([
                (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in correspondence_embeddings.items()
            ], reverse=True)

            block['similar']['correspondence'] = document_similarities[0:10]


    json.dump(data,open(file,'w'),indent=2)
    









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

        
        this_index = (digital_id,"_".join(pages))

        
        data['similar'] = {}


        query_embedding = data['embedding']
        
        document_similarities = sorted([
            (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in daybook_embeddings.items()
        ], reverse=True)
        
        
        data['similar']['daybook'] = document_similarities[0:20]

        document_similarities = sorted([
            (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in writings_embeddings.items()
        ], reverse=True)
        print(document_similarities[0])
        data['similar']['writings'] = document_similarities[0:20]

        document_similarities = sorted([
            (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in correspondence_embeddings.items()
        ], reverse=True)

        data['similar']['correspondence'] = document_similarities[1:20]


        json.dump(data,open(file,'w'),indent=2)


