import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from rdflib import Graph

def execute_sparql_query(rdf_file, sparql_query):
    g = Graph()
    g.parse(rdf_file, format="turtle")
    
    results = g.query(sparql_query)
    output = []
    for row in results:
        result = [row[var] for var in results.vars]
        output.append(result)
    return list(results.vars), output

def load_file():
    file_path = filedialog.askopenfilename(
        title="Sélectionnez un fichier RDF",
        filetypes=[("Fichiers Turtle", "*.ttl"), ("Tous les fichiers", "*.*")]
    )
    if file_path:
        rdf_file_var.set(file_path)

def execute_query():
    rdf_file = rdf_file_var.get()
    sparql_query = sparql_text.get("1.0", tk.END).strip()
    
    if not rdf_file:
        messagebox.showerror("Erreur", "Veuillez sélectionner un fichier RDF.")
        return
    if not sparql_query:
        messagebox.showerror("Erreur", "Veuillez entrer une requête SPARQL.")
        return
    
    try:
        headers, results = execute_sparql_query(rdf_file, sparql_query)
        populate_results_table(headers, results)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution : {e}")

def populate_results_table(headers, results):
    # Clear existing data
    for item in results_table.get_children():
        results_table.delete(item)
    
    # Set new headers
    results_table["columns"] = headers
    for col in headers:
        results_table.heading(col, text=col)
        results_table.column(col, anchor="w", width=100)
    
    # Insert new rows
    for result in results:
        results_table.insert("", tk.END, values=result)

# Interface Tkinter
root = tk.Tk()
root.title("Exécution de requêtes SPARQL")

# Appliquer un thème ttk
style = ttk.Style()
style.theme_use("clam")  # Choisissez un thème moderne

# Variables
rdf_file_var = tk.StringVar()

# Widgets
frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Fichier RDF :").grid(row=0, column=0, sticky="w", pady=5)
ttk.Entry(frame, textvariable=rdf_file_var, width=50).grid(row=0, column=1, padx=5)
ttk.Button(frame, text="Parcourir", command=load_file).grid(row=0, column=2, padx=5)

ttk.Label(frame, text="Requête SPARQL :").grid(row=1, column=0, sticky="nw", pady=5)
sparql_text = tk.Text(frame, height=10, width=60, font=("Arial", 10))
sparql_text.grid(row=1, column=1, columnspan=2, pady=5)

ttk.Button(frame, text="Exécuter", command=execute_query).grid(row=2, column=2, pady=10, sticky="e")

ttk.Label(frame, text="Résultats :").grid(row=3, column=0, sticky="nw", pady=5)

# Résultats sous forme de tableau
results_table = ttk.Treeview(frame, show="headings")
results_table.grid(row=3, column=1, columnspan=2, pady=5, sticky="nsew")

# Configurer les colonnes dans le cadre
frame.columnconfigure(1, weight=1)
frame.rowconfigure(3, weight=1)

# Lancement de l'interface
root.mainloop()
