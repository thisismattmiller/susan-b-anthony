import json
import util
import glob

from transformers import GPT2TokenizerFast
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text: str) -> int:
    """count the number of tokens in a string"""
    return len(tokenizer.encode(text))

file_item_order = {}

for file in glob.glob('anthony-speeches-and-other-writings-*/*.json'):

  dir = file.split('/')[-2]

  if dir == 'anthony-speeches-and-other-writings-resources':
    continue

  # if dir != 'anthony-speeches-and-other-writings-1862':
  #   continue

  if dir not in file_item_order:
    file_item_order[dir] = []

  file_id = int(file.split('/')[-1].replace('.json',''))

  file_item_order[dir].append(file_id)

  file_item_order[dir] = sorted(file_item_order[dir])

print(file_item_order)
for dir in file_item_order:

  all_text = ""  
  all_items = []
  all_items_ids = []
  blocks = []

  for id in file_item_order[dir]:
    print(id)
    data = json.load(open(f"{dir}/{id}.json"))

    if 'full_text' not in data:
      continue

    full_text = util.clean_up_transcribed_text(data['full_text'])
    data['id'] = id

    all_text = all_text + full_text
    all_items.append(data)
    all_items_ids.append(id)

    if count_tokens(all_text) >= 500:

      blocks.append({
          'items':all_items[:],
          'text':all_text,
          'tokenCount': count_tokens(all_text)
      })
      print(all_items_ids)
      all_text=''
      all_items=[]
      all_items_ids=[]

  # leftovers
  if len(all_items) >0:
    blocks.append({
        'items':all_items[:],
        'text':all_text,
        'tokenCount': count_tokens(all_text)
    })

  json.dump(blocks,open(f'anthony-speeches-and-other-writings-resources/{dir}.json','w'),indent=2)





  



    