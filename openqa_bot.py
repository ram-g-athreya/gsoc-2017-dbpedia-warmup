from SPARQLWrapper import SPARQLWrapper, JSON
import requests, urllib, cStringIO

OPENQA_URL = "http://search.openqa.aksw.org/api/rest/search?q="

def query_open_qa(question):
    r = requests.get(OPENQA_URL + question)
    return r.json()

def get_data_from_dbpedia(list):
    result_list = []
    for item in list:
        uri = item['URI_PARAM']
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX res: <http://dbpedia.org/resource/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        select DISTINCT ?label ?abstract ?wikipedia
        where {
            <%s> rdfs:label ?label .
            FILTER(LANG(?label)='en') .
            OPTIONAL {<%s> dbo:abstract ?abstract FILTER(LANG(?abstract)='en')} .
            OPTIONAL {<%s> dbo:thumbnail ?thumbnail} .         
            OPTIONAL {<%s> foaf:isPrimaryTopicOf ?wikipedia} .
        }
        """ % (uri, uri, uri, uri))
        
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        result_list.append(results)
    return result_list

def handle_request(question):
    json_result = query_open_qa(question)

    if len(json_result) == 0: # No Results Found
        print('I am sorry I was not able to find anything for you query would you like to try again?')
    else:
        result_list = get_data_from_dbpedia(json_result)
        for result in result_list:
            if len(result['results']['bindings']) == 0:
                continue
            result = result['results']['bindings'][0]
            print(result['label']['value'] + '\n\n')
            if result['abstract']:
                if len(result['abstract']['value']) > 300:
                    print(result['abstract']['value'][:300] + '...')
                else:
                    print(result['abstract']['value'])
                print('\n\n')            
            if result['wikipedia']:
                print('Wikipedia URL: ' + result['wikipedia']['value'] + '\n\n')                
        print 'What else would you like to ask me?'       

def main():
    print('Hi I am the OpenQA Bot. Ask me anything and I will try my best to answer.')
    
    while(True):
        handle_request(raw_input().strip())        
        
if __name__ == '__main__':
    main()