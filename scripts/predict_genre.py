#!./.venv/bin/python
import sys
import joblib
import numpy as np
import argparse
from sentence_transformers import SentenceTransformer

# Paths to the model and components
MODEL_PATH = "./data/genre_classifier.joblib"
TRANSFORMER_MODEL = 'paraphrase-multilingual-MiniLM-L12-v2'

def predict(text, show_probs=False):
    # Load the trained model
    try:
        data = joblib.load(MODEL_PATH)
        clf = data['model']
        genres = data['genres']
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        sys.exit(1)

    # Load the embedding model
    model = SentenceTransformer(TRANSFORMER_MODEL)

    # Generate embedding
    embedding = model.encode([text], convert_to_numpy=True)

    # Predict
    prediction_idx = clf.predict(embedding)[0]
    predicted_genre = genres[prediction_idx]


    if not show_probs:
        print(f"{predicted_genre}")
    else:
        probs = clf.predict_proba(embedding)[0]
        for genre, prob in zip(genres, probs):
            print(f"{genre:10}: {prob:.4f}")

def main():
    parser = argparse.ArgumentParser(description="Predict movie genre from text.")
    parser.add_argument("text", help="The text/subtitle to analyze (enclose in quotes if multiple words).", nargs="?")
    parser.add_argument("--probs", action="store_true", help="Show probabilities for all genres.")
    
    args = parser.parse_args()

    if args.text:
        predict(args.text, args.probs)
    else:
        # If no text provided as argument, read from stdin
        print("Reading from stdin (Ctrl+D to finish)...", file=sys.stderr)
        text = sys.stdin.read().strip()
        if text:
            predict(text, args.probs)
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
