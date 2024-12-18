from SPARQLWrapper import SPARQLWrapper, JSON

def execute_sparql_query(query):
    """
    Exécute une requête SPARQL sur l'endpoint DbPedia et retourne les résultats.
    """
    endpoint_url = "https://dbpedia.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()
        return results
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête SPARQL : {e}")
        return None

def format_results(results):
    """
    Formate les résultats SPARQL pour un affichage lisible.
    """
    if not results or "results" not in results:
        print("Aucun résultat.")
        return

    for result in results["results"]["bindings"]:
        for key, value in result.items():
            print(f"{key}: {value['value']}")
        print("-" * 30)

def main():
    """
    Application principale.
    """
    print("Bienvenue dans l'application SPARQL pour DbPedia!")
    print("Exemples de requêtes SPARQL :")
    print("1. Rechercher des villes en France :")
    print("""
    SELECT ?city ?label
    WHERE {
        ?city rdf:type dbo:City ;
              dbo:country dbr:France ;
              rdfs:label ?label .
        FILTER (lang(?label) = 'fr')
    }
    LIMIT 10
    """)
    
    print("2. Rechercher les livres écrits par J.K. Rowling :")
    print("""
    SELECT ?book ?label
    WHERE {
        ?book rdf:type dbo:Book ;
              dbo:author dbr:J._K._Rowling ;
              rdfs:label ?label .
        FILTER (lang(?label) = 'fr')
    }
    LIMIT 10
    """)
    
    choice = input("Choisissez une option (1 ou 2) ou entrez votre propre requête SPARQL :\n")
    
    if choice == "1":
        query = """
        SELECT ?city ?label
        WHERE {
            ?city rdf:type dbo:City ;
                  dbo:country dbr:France ;
                  rdfs:label ?label .
            FILTER (lang(?label) = 'fr')
        }
        LIMIT 10
        """
    elif choice == "2":
        query = """
        SELECT ?book ?label
        WHERE {
            ?book rdf:type dbo:Book ;
                  dbo:author dbr:J._K._Rowling ;
                  rdfs:label ?label .
            FILTER (lang(?label) = 'fr')
        }
        LIMIT 10
        """
    else:
        query = choice
    
    print("Exécution de la requête...")
    results = execute_sparql_query(query)
    format_results(results)

if __name__ == "__main__":
    main()
