'''This package contains useful scripts for the papers app which arent views, tests or urls'''
from mendeley_client import MendeleyClient

from django.conf import settings

from papers.models import Publication

def get_mendeley_authored_documents():
    '''This function gets all of the authored documents in the authorized library.
    
    It will return a dictionary named documents with keys documentId and several fields from the Mendeley API.
    '''
    mendeley = MendeleyClient(settings.MENDELEY_CONSUMER_KEY, settings.MENDELEY_SECRET_KEY)

    try:
        mendeley.load_keys()
    except IOError:
        mendeley.get_required_keys()
        mendeley.save_keys()
    authored_document_list = {}
    response = mendeley.documents_authored() #this get a list of all documents authored by the authorized user
    for document in response['document_ids']: #this generates a list of all the details for each of these documents
        details = mendeley.document_details(document)
        authored_document_list[document] = details
    return authored_document_list
    
def write_mendeley_papers_to_database(documents):
    '''This function will take a document list and update the Publication model in the database.
    
    To call this you have to get a document list, for example from get_mendeley_authored_documents() 
    the output of that function is then passed to this function.'''
    for key in documents.keys():
        paper = Publication(mendeley_url = documents[key]['mendeley_url'],    
        	title = documents[key]['title'],  
        	id = documents[key]['canonical_id'],
        	doi = documents[key]['doi'],  
        	year = documents[key]['year'],
            issue = documents[key]['issue'], 
            pages = documents[key]['pages'],
            abstract = documents[key]['abstract'],
            type = documents[key]['type'])
        paper.save()