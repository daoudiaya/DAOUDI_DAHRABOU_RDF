from flask import Flask, render_template, request
from SPARQLWrapper import SPARQLWrapper, JSON

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
    results = None
    query = None
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            results = execute_sparql_query(query)

    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)






















