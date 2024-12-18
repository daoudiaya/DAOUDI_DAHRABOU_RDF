from flask import Flask, render_template, request
from SPARQLWrapper import SPARQLWrapper, JSON

# Initialisation de l'application Flask
app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Route principale pour afficher le formulaire de requête SPARQL et les résultats.
    """
    results = None  # Initialisation des résultats à None
    query = None    # Initialisation de la requête à None
    
    if request.method == "POST":
        query = request.form.get("query")  # Récupère la requête SPARQL depuis le formulaire
        if query:
            results = execute_sparql_query(query)  # Exécute la requête SPARQL

    # Rend le template HTML avec les résultats
    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    # Exécute l'application Flask en mode debug
    app.run(debug=True)
