from SearchService_pb2 import SearchService, SearchResponse

class SearchImpl(SearchService):
    def Search(self, controller, request, done): 
        print "In Search!"

        response = SearchResponse()
        response.response = "booooya"


        done.run(response)
