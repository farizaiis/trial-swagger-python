from flask import make_response, abort, jsonify
from elasticsearch import Elasticsearch, helpers
import string
import random

es = Elasticsearch(host="localhost", port=9200)
es = Elasticsearch()
index = "train_elastic_user"


def get_all():
    print("test")
    query = {
        "query": {
            "match_all" : {}
        }
    }
    result = helpers.scan(es, index=index, body=query)

    data = [d["_source"] for d in result]

    return jsonify(data)

def post(user):
    full_name = user.get("full_name", None)
    email = user.get("email", None)
    age = user.get("age", None)
    user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=11))

    query = {
		"query": {
			"match_phrase": {
				"email": email
			}
		}
	}

    result = es.search(index=index, body=query)
	
    if len(result["hits"]["hits"])==0 and email:
        data = {
            "full_name" : full_name,
            "email" : email,
            "age" : age,
            "user_id" : user_id
        }
        es.index(index=index,body=data)
        
        res = {
            "status" : "Success",
            "message" : "Data with email {email} succesfully created".format(email=email)
        }

        return make_response(
            jsonify(res)
        )
    else:
        abort(
            406,
			"Email {email} already use".format(email=email)
        )

def get_by_id(user_id):
    query = {
		"query": {
			"match_phrase": {
				"user_id": user_id
			}
		}
	}
    result = es.search(index=index, body=query)

    if len(result["hits"]["hits"]) > 0:
        return_value = result["hits"]["hits"][0]["_source"]
        return jsonify(return_value)

    else:
        abort(
			404, "User with user_id {user_id} not found".format(user_id=user_id)
		)

def put(user_id, user):
    query = {
		"query": {
			"match_phrase": {
				"user_id": user_id
			}
		}
	}
    result = es.search(index=index, body=query)
	
    if len(result["hits"]["hits"])>=1:
        data= {
			"doc": {
				"full_name": user.get("full_name", result["hits"]["hits"][0]["_source"]["full_name"]),
				"email": user.get("email", result["hits"]["hits"][0]["_source"]["email"]),
				"age": user.get("age", result["hits"]["hits"][0]["_source"]["age"]),
			}
		}
        
        es.update(
			index=index,
			id=result["hits"]["hits"][0]["_id"],
			body=data
		)
		
        return jsonify(data)
    else:
        abort(
			404, "User with user_id {user_id} not found".format(user_id=user_id)
		)


def delete(user_id):
    query = {
		"query": {
			"match_phrase": {
				"user_id": user_id
			}
		}
	}
    
    result = es.search(index=index, body=query)
    
    if len(result["hits"]["hits"])>=1:
        es.delete(index=index, id=result["hits"]["hits"][0]["_id"])

        res = {
            "status" : "Success",
            "message" : "Data with user_id {user_id} succesfully deleted".format(user_id=user_id)
        }

        return make_response(
            jsonify(res)
        )
    else:
        abort(
			404, "User with user_id {user_id} not found".format(user_id=user_id)
		)