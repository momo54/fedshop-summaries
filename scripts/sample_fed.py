import argparse
import sys
from SPARQLWrapper import SPARQLWrapper, N3,TURTLE,RDF
from string import Template
import requests
from rdflib import Graph
import os

predicates=['<http://www.w3.org/2002/07/owl#sameAs>','<http://xmlns.com/foaf/0.1/based_near>']

query_template_star= Template("""construct {
  ?z ?p ?o .
  ?x ?p1 ?o1
} WHERE {
  ?x $placeholder ?y .
  ?z $placeholder ?y .
  filter (isIRI(?x) && isIRI(?y) && isIRI(?z)).
  optional {?z ?p ?o}
  optional {?x ?p1 ?o1}
  filter (?x != ?z)
  bind (STRBEFORE(STRAFTER(STR(?x), "://"),"/") as ?xp) .
  bind (STRBEFORE(STRAFTER(STR(?z), "://"),"/") as ?zp) .
  filter (?xp != ?zp)
} limit $placeholder_limit offset $placeholder_offset
""")

query_template_chain=Template("""construct {
  ?x ?p ?o .
  ?y ?p1 ?o1
} WHERE {
  ?x $placeholder ?y .
  filter (isIRI(?x) && isIRI(?y)).
  optional {?x ?p ?o}
  optional {?y ?p1 ?o1}
  filter (?x != ?y)
  bind (STRBEFORE(STRAFTER(STR(?x), "://"),"/") as ?xp) .
  bind (STRBEFORE(STRAFTER(STR(?y), "://"),"/") as ?yp) .
  filter (?xp != ?yp)
} limit $placeholder_limit offset $placeholder_offset
""")

# headers = {
#     "Accept": "text/ntriples"
# }

def construct_query_virtuoso(endpoint_url, query_template,pred,limit=1000000,offset=0):

    query = query_template.substitute(placeholder=pred,placeholder_limit=limit,placeholder_offset=offset)
    print(f"executing query: {query} on {endpoint_url}", file=sys.stderr)

#    response = requests.get(endpoint_url, params={'query': query}, headers=headers)
    
#    if response.status_code == 200:
#        print(response.text)
#    else:
#        print(f"Error: {response.status_code}")
    
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(N3)  # Set the return format to N3 (which can return N-Triples)
    results = sparql.query().convert()
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Execute a SPARQL CONSTRUCT query and get results in NT format.')
    parser.add_argument('--endpoint_url', default='http://localhost:8890/sparql', help='The URL of the Virtuoso SPARQL endpoint')
    parser.add_argument('output_file', help='Path to the output file where results will be saved in NT format')
    
    args = parser.parse_args()

    if os.path.exists(args.output_file):
        os.remove(args.output_file)
    
    for predicat in predicates:
        results=construct_query_virtuoso(args.endpoint_url,query_template_star,predicat)

        if results:
            graph = Graph()
            graph.parse(data=results, format='n3')
            ntriples_data = graph.serialize(format='nt')
            with open(args.output_file, 'ab') as f:  # Open the file in append mode
                f.write(ntriples_data.encode('utf-8'))

        results=construct_query_virtuoso(args.endpoint_url,query_template_chain,predicat)
        if results:
            graph = Graph()
            graph.parse(data=results, format='n3')
            ntriples_data = graph.serialize(format='nt')
            with open(args.output_file, 'ab') as f:  # Open the file in append mode
                f.write(ntriples_data.encode('utf-8'))
    
#    print(f"Results have been written to {args.output_file}")
