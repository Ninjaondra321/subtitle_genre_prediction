#!./.venv/bin/python
import sys
import numpy as np
from sentence_transformers import SentenceTransformer

def process_genre(genre_name, input_file):
    print(f"--- Processing {genre_name} ---")
    
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        sentences = [line.strip() for line in f if line.strip()]
    
    print(f"Loaded {len(sentences)} sentences. Encoding...")
    
    embeddings = model.encode(
        sentences,
        show_progress_bar=True, 
        convert_to_numpy=True
    )
    
    output_file = f"./data/embeddings/{genre_name}.npy"
    np.save(output_file, embeddings)
    print(f"Saved {len(embeddings)} embeddings to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_embeddings.py <genre_name> <input_file>")
    else:
        process_genre(sys.argv[1], sys.argv[2])