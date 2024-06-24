import argparse
from rdflib import Graph,ConjunctiveGraph
def convert_nquads_to_ntriples(input_file, output_file):

    with open(input_file, 'r') as f:
        print("Premières lignes du fichier :")
        for _ in range(5):  # Afficher les 5 premières lignes
            print(f.readline().strip())
            
            
    # Créer un graphe RDF
    g = ConjunctiveGraph()

    try:
        g.parse(location=input_file, format='nquads')
        print(f"Chargement réussi, {len(g)} triplets lus.")
    except Exception as e:
        print(f"Erreur lors du chargement du fichier: {e}")
        return


    
    # Enlever les doublons en convertissant le graphe en un ensemble de triplets
    seen_triples = set()
    for subj, pred, obj in g:
        triple = (subj, pred, obj)
        if triple not in seen_triples:
            seen_triples.add(triple)

    # Écrire les triplets uniques dans un fichier N-Triples
    with open(output_file, 'w') as f:
        for subj, pred, obj in seen_triples:
            # Formatte chaque triplet en N-Triple
            line = f"{subj.n3()} {pred.n3()} {obj.n3()} .\n"
            f.write(line)

    print(f"Conversion terminée. Le fichier '{output_file}' a été créé avec des triplets uniques.")

def main():
    # Définir le parser d'arguments
    parser = argparse.ArgumentParser(description='Convert N-Quads (.nq) file to N-Triples (.nt) with no duplicates.')
    parser.add_argument('input_file', type=str, help='Input N-Quads file path')
    parser.add_argument('output_file', type=str, help='Output N-Triples file path')
    
    # Parse les arguments
    args = parser.parse_args()
    
    # Exécuter la conversion
    convert_nquads_to_ntriples(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
