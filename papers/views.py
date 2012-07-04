# Create your views here.
from mendeley_client import MendeleyClient

from django.conf import settings


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