


def clean_up_transcribed_text(text):

	text = text.replace('Transcribed and reviewed by volunteers participating in the By The People project at crowd.loc.gov.','')
	text = text.replace('&amp;','&')
	text = text.replace('"',"'")
	text = text.strip()

	return text