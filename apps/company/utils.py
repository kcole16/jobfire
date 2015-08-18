import os

from algoliasearch import algoliasearch

def add_to_algolia(posting):
    client = algoliasearch.Client("74PKG6FSJB", os.environ['ALGOLIA_KEY']);
    index = client.init_index('Postings')
    posting_dict = [{"objectID": posting.id, 
    "expiration_date": posting.expiration_date,
    "position": posting.position,
    "job_type": posting.job_type,
    "company": {
    	"id":posting.company.id,
    	"name":posting.company.name,
    	"logo":posting.company.logo,
    	"about":posting.company.about
    	},
    "location":posting.location,
    "university":posting.university.name,
    "active":posting.active,
    "description":posting.description,
    "role": posting.role,
    "id":posting.id
    }]	
    index.save_objects(posting_dict)    