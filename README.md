# Subtitle genre prediction
Predict a genre of a czech sentence from a movie. Can be easily updated for different language.

## Usage

### Download this project
```bash
git clone https://github.com/Ninjaondra321/subtitle_genre_prediction
```

### (optional) Generate a model
This repo comes with pretrained model (data/genre_classifier.joblib), but you can train your own like this:
(Keep in mind, that even on large servers this takes > 24 hours to train)
Note: it's recomended to use venv. For that, rewrite the first line of all scripts to your venv.
```bash
make ./data/genre_classifier.joblib
```

### Using the model

```bash
> ./scripts/predict_genre.py "Ach můj Rómeo, já tě tak miluji"
Romance
```

Or with probabilities:

```bash
> ./scripts/predict_genre.py --probs "Ach můj Rómeo, já tě tak miluji"
Action    : 0.0715
Comedy    : 0.1735
Crime     : 0.0873
Drama     : 0.1687
Fantasy   : 0.0895
Horror    : 0.1058
Romance   : 0.3038
```


## About the project (czech sentences):
### Data:
A major issue arose from the fact that most movies are not labeled with a single genre, but with multiple. A histogram showing the number of movies across different sets of genres can be found in the file `./report_data/genre_movies_stats`. The main problem, however, is that genres occur in mixed combinations where classification cannot be easily performed—for example, *Drama* appears in 90,344 out of 156,040 movies, and most frequently in combination with *Crime*, *Comedy*, and *Romance* (where I expect distinct differences).

Therefore, I selected the following groups for classification:

| Class | Genres |
| :--- | :--- |
| Action | (Action,Adventure,Drama) |
| Drama | (Drama) |
| Comedy | (Comedy) |
| Crime | (Crime,Drama,Thriller) \| (Crime,Drama,Mystery) \| (Crime,Drama) |
| Fantasy | (Drama,Mystery,Sci-Fi) \| (Drama,Fantasy,Mystery) \| (Adventure,Drama,Fantasy) |
| Horror | (Horror), (Drama,Horror,Thriller) |
| Romance | (Drama,Romance) |

### Training
From each group, I extracted one million random sentences and converted them into vectors using sentence embeddings (`paraphrase-multilingual-MiniLM-L12-v2`). I then trained a logistic regression model on these vectors.

### Result
The resulting model achieved an accuracy of 0.2346. In most fields, this would indicate failure, but in the case of subtitles, it is a satisfactory result, as the majority of sentences can appear in virtually any genre. It performs well on sentences explicitly tailored to a specific genre:

<pre>
> ./scripts/predict_genre.py --probs "Ach můj Rómeo, já tě tak miluji"
Action    : 0.0715
Comedy    : 0.1735
Crime     : 0.0873
Drama     : 0.1687
Fantasy   : 0.0895
Horror    : 0.1058
<mark>Romance   : 0.3038</mark>

> ./scripts/predict_genre.py --probs "Viděl jsem ho, jak odhodil zbraň do řeky"
Action    : 0.1408
Comedy    : 0.0636
<mark>Crime     : 0.2923</mark>
Drama     : 0.0938
Fantasy   : 0.1541
Horror    : 0.2053
Romance   : 0.0500

> ./scripts/predict_genre.py --probs "Tahle kouzelná hůlka odkryje všechno tajemství"
Action    : 0.2159
Comedy    : 0.0489
Crime     : 0.0763
Drama     : 0.0447
<mark>Fantasy   : 0.4047</mark>
Horror    : 0.1757
Romance   : 0.0337

> xnecas3@asteria04:~/subtitle_analysis/final_project$ ./scripts/predict_genre.py --probs "Utíkej nebo tě zabiju!"
<mark>Action    : 0.2195</mark>
Comedy    : 0.0735
Crime     : 0.1014
Drama     : 0.1174
Fantasy   : 0.1763
<mark>Horror    : 0.2498</mark>
Romance   : 0.0621
</mark>
</pre>




## Special thanks
This project was developed as a final project of a IB030: Natural language processing course. I want to thank [NLP Lab at MUNI FI](https://nlp.fi.muni.cz/) for letting me develop this project at their servers <3.