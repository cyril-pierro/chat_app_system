from rest_framework import views
from rest_framework.response import Response
from elasticsearch import Elasticsearch
from django.conf import settings

HOST = settings.ELASTICSEARCH_HOST
PORT = settings.ELASTICSEARCH_PORT

es = Elasticsearch(hosts=f"http://{HOST}:{PORT}")

INDEX = "elasticsearch_users"


class SearchUsers(views.APIView):
    """Search all users in the system.
    """

    def get(self, request, username, format=None):
        """Return results
        """
        index_state = es.indices.exists(index=INDEX)
        if index_state:
            res = es.search(
                index=INDEX,
                query={
                    "fuzzy": {
                        "USERNAME": {
                            "value": username,
                            "fuzziness": 2,
                            "max_expansions": 50,
                            "prefix_length": 1,
                            "transpositions": True,
                            "rewrite": "constant_score"
                        }
                    }
                }

            )
            list_of_users = [i["_source"] for i in res["hits"]["hits"]]
            return Response(list_of_users)
        return Response({"error": "Users not Found"}, status=500)