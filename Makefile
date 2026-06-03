
./data/download/cs.zip:
	mkdir -p $(dir $@)
	curl -L "https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2024/xml/cs.zip" -o $@

./data/prepared/cs_sentences: ./data/download/cs.zip
	mkdir -p $(dir $@)
	./scripts/generate_sentences_tsv.py $< > $@

./data/milion_lines/Action_milion: ./data/prepared/cs_sentences
	mkdir -p $(dir $@)
	grep $'^Action,Adventure,Drama\t' < $< | cut -f3 > $@

./data/milion_lines/Drama_milion: ./data/prepared/cs_sentences
	mkdir -p $(dir $@)
	grep $'^Drama\t' < $< | cut -f3 > $@

./data/milion_lines/Comedy_milion: ./data/prepared/cs_sentences
	mkdir -p $(dir $@)
	grep $'^Comedy\t' < $< | cut -f3 > $@

./data/milion_lines/Crime_milion: ./data/prepared/cs_sentences
	mkdir -p $(dir $@)
	grep -E "^(Crime,Drama,Thriller|Crime,Drama,Mystery|Crime,Drama)"$'\t' < $< | cut -f3 > $@

./data/milion_lines/Fantasy_milion: ./data/prepared/cs_sentences
	mkdir -p $(dir $@)
	grep -E "^(Drama,Mystery,Sci-Fi|Drama,Fantasy,Mystery|Adventure,Drama,Fantasy)"$'\t' < $< | cut -f3 > $@

./data/milion_lines/Horror_milion: ./data/prepared/cs_sentences
	mkdir -p $(dir $@)
	grep $'^Horror\t' < $< | cut -f3 > $@


./data/embeddings/Action.npy: ./data/milion_lines/Action_milion
	./scripts/generate_embeddings.py Action $^ 

./data/embeddings/Comedy.npy: ./data/milion_lines/Comedy_milion
	./scripts/generate_embeddings.py Comedy $^
	
./data/embeddings/Crime.npy: ./data/milion_lines/Crime_milion
	./scripts/generate_embeddings.py Crime $^

./data/embeddings/Drama.npy: ./data/milion_lines/Drama_milion
	./scripts/generate_embeddings.py Drama $^

./data/embeddings/Fantasy.npy: ./data/milion_lines/Fantasy_milion
	./scripts/generate_embeddings.py Fantasy $^

./data/embeddings/Horror.npy: ./data/milion_lines/Horror_milion
	./scripts/generate_embeddings.py Horror $^

./data/embeddings/Romance.npy: ./data/milion_lines/Romance_milion
	./scripts/generate_embeddings.py Romance $^	


./data/genre_classifier.joblib: ./data/embeddings/Action.npy ./data/embeddings/Comedy.npy ./data/embeddings/Crime.npy ./data/embeddings/Drama.npy ./data/embeddings/Fantasy.npy ./data/embeddings/Horror.npy ./data/embeddings/Romance.npy
	./scripts/train_classifier.py

