import spacy
import re
import emoji

# Load the pre-trained spaCy model for English language
nlp = spacy.load("en_core_web_sm")

# Define regex patterns for hashtags and mentions
""""
This pattern matches any word starting with the # symbol followed by one or more alphanumeric characters or underscores. 
The (?:^|\s) part of the pattern ensures that the hashtag is preceded by either a space or the beginning of the string.
"""
hashtag_pattern = r"(?:^|\s)(#[A-Za-z0-9_]+)"

""""
This pattern matches any word starting with the @ symbol followed by one or more alphanumeric characters or underscores. 
The (?:^|\s) part of the pattern ensures that the mention is preceded by either a space or the beginning of the string.
"""
mention_pattern = r"(?:^|\s)(@[A-Za-z0-9_]+)"

#Define a function to extract entities, hashtags, mentions, and emojis from text
def extract_entities(text):
    
    #Use spaCy to perform named entity recognition
    doc = nlp(text)
    
    #Initialize an empty list to store all the detected entities
    entities = []
    
    #Loop over all the named entities detected by spaCy and add them to the entities list
    for ent in doc.ents:
        entity = {}
        entity['text'] = ent.text
        entity['start'] = ent.start_char
        entity['end'] = ent.end_char
        
        #Map the entity label detected by spaCy to our own entity type categories
        if ent.label_ == 'GPE':
            entity['type'] = 'GPE'
        elif ent.label_ == 'ORG':
            entity['type'] = 'ORG'
        else:
            entity['type'] = 'NON-GPE'
            
        #Add the entity to the entities list
        entities.append(entity)
        
    #Extract hashtags using regex pattern matching
    for match in re.finditer(hashtag_pattern, text):
        entity = {}
        entity['text'] = match.group(1)
        entity['start'] = match.start(1)
        entity['end'] = match.end(1)
        entity['type'] = 'HASHTAG'
        entities.append(entity)
        
    #Extract mentions using regex pattern matching
    for match in re.finditer(mention_pattern, text):
        entity = {}
        entity['text'] = match.group(1)
        entity['start'] = match.start(1)
        entity['end'] = match.end(1)
        entity['type'] = 'MENTION'
        entities.append(entity)
        
    #Extract emojis using the emoji library
    emojis = list(filter(lambda x: x in emoji.UNICODE_EMOJI, text))
    
    #Return a dictionary containing the extracted entities and emojis
    return {'entities': entities, 'emojis': emojis}

#Test the function with a sample text and print the extracted entities and emojis
text = "Just bought some #DodgeCoin and I'm loving it! Also, did you know that @elonmusk is the CEO of Tesla and SpaceX, both headquartered in California? 😊💰"

entities = extract_entities(text)

print(entities)
