import json
import util

page_order = json.load(open('group-ui-util/anthony-correspondence-id-sets.json'))


for pages in page_order:

  resource_data = {
    'items': []
  }

  all_pages_text = ''
  filename=''
  for p in pages:

    page_data = json.load(open(f"anthony-correspondence/{p}.json"))
    page_data['id'] = p
    resource_data['items'].append(page_data)
    full_text = util.clean_up_transcribed_text(page_data['full_text'])

    all_pages_text = all_pages_text + full_text + '\n\n'
    filename = filename + f"{p}_"


  filename = filename[0:-1] + '.json'

  resource_data['ids'] = pages
  resource_data['filename'] = filename
  resource_data['full_text']  = all_pages_text


  json.dump(resource_data,open(f'anthony-correspondence-resources/{filename}','w'),indent=2)
 
