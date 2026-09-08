"""Lecture, lab, and hub metadata for DATA 441/641."""

NOTES = [
    {"slug": "nlp-in-the-real-world", "week": 1, "title": "1.1 NLP in the Real World", "lead": "What NLP is, the core tasks, and why human language is a hard input.", "slide": "1.1-nlp-in-the-real-world"},
    {"slug": "ml-dl-nlp-overview", "week": 1, "title": "1.2 Machine Learning, Deep Learning, and NLP", "lead": "Rules, then learning from examples, then stacked representations.", "slide": "1.2-ml-dl-nlp-overview"},
    {"slug": "python-tour", "week": 1, "title": "1.3 A Python Tour for NLP", "lead": "Types, strings, containers, control flow, functions, files, NumPy, and a small class.", "slide": "1.3-python-tour"},
    {"slug": "lab-1-numpy-nltk-files", "week": 1, "title": "Lab 1: NumPy, NLTK, and Files", "lead": "Arrays, stemming versus lemmatization, and a movie script."},
    {"slug": "data-acquisition", "week": 2, "title": "2.1 Data Acquisition", "lead": "Where the text comes from, and what counts as good enough data.", "slide": "2.1-data-acquisition"},
    {"slug": "text-extraction-cleanup", "week": 2, "title": "2.2 Text Extraction and Cleanup", "lead": "Pull words out of HTML and PDF, then fix encoding and boilerplate.", "slide": "2.2-text-extraction-cleanup"},
    {"slug": "preprocessing", "week": 2, "title": "2.3 Preprocessing", "lead": "Tokenize, normalize, drop stops, and choose stemming or lemmatization.", "slide": "2.3-preprocessing"},
    {"slug": "advanced-preprocessing", "week": 2, "title": "2.4 Advanced Preprocessing", "lead": "POS tags, a first look at entities, and why parsing is optional.", "slide": "2.4-advanced-preprocessing"},
    {"slug": "lab-2-text-extraction", "week": 2, "title": "Lab 2: Text Extraction and Cleanup", "lead": "Back-translation, HTML, a PDF, and a short preprocess chain."},
    {"slug": "feature-engineering", "week": 3, "title": "3.1 Feature Engineering", "lead": "Turn cleaned text into numbers a model can use.", "slide": "3.1-feature-engineering"},
    {"slug": "modeling", "week": 3, "title": "3.2 Modeling", "lead": "Heuristics, classical models, and when to stack them.", "slide": "3.2-modeling"},
    {"slug": "evaluation", "week": 3, "title": "3.3 Evaluation", "lead": "Intrinsic versus extrinsic tests, and precision, recall, and F1.", "slide": "3.3-evaluation"},
    {"slug": "deployment-monitoring", "week": 3, "title": "3.4 Deployment and Monitoring", "lead": "Ship a module, watch it drift, and collect the next batch of data.", "slide": "3.4-deployment-monitoring"},
    {"slug": "lab-3-fake-news", "week": 3, "title": "Lab 3: A Short Fake-News Pipeline", "lead": "Clean two news CSVs and walk them through the pipeline."},
    {"slug": "text-representation-intro", "week": 4, "title": "4.1 Text Representation: Introduction", "lead": "Why models need numbers, and the families of representations.", "slide": "4.1-text-representation-intro"},
    {"slug": "one-hot", "week": 4, "title": "4.2 One-Hot Vectors", "lead": "A word as a single 1 in a long, sparse vector.", "slide": "4.2-one-hot"},
    {"slug": "bow", "week": 4, "title": "4.3 Bag of Words", "lead": "Count tokens and ignore order.", "slide": "4.3-bow"},
    {"slug": "bonw", "week": 4, "title": "4.4 Bag of N-Grams", "lead": "Counts of short phrases keep a little local order.", "slide": "4.4-bonw"},
    {"slug": "tfidf", "week": 4, "title": "4.5 TF-IDF", "lead": "Down-weight words that appear in almost every document.", "slide": "4.5-tfidf"},
    {"slug": "intro-deep-learning", "week": 5, "title": "5.1 Introduction to Deep Learning", "lead": "Layers, loss, and why we stack representations.", "slide": "5.1-intro-deep-learning"},
    {"slug": "distributed-representations", "week": 5, "title": "5.2 Distributed Representations", "lead": "Similar words share dimensions instead of a single one-hot slot.", "slide": "5.2-distributed-representations"},
    {"slug": "word2vec-cbow", "week": 5, "title": "5.3 Word2Vec CBOW", "lead": "Predict the middle word from its neighbors.", "slide": "5.3-word2vec-cbow"},
    {"slug": "word2vec-skipgram", "week": 5, "title": "5.4 Word2Vec Skip-gram", "lead": "Predict the neighbors from the middle word.", "slide": "5.4-word2vec-skipgram"},
    {"slug": "word2vec-practical", "week": 5, "title": "5.5 Word2Vec Practical Considerations", "lead": "Negative sampling, window size, and other training tricks.", "slide": "5.5-word2vec-practical"},
    {"slug": "text-classification-pipeline", "week": 6, "title": "6.1 Text Classification Pipeline", "lead": "The full path from raw text to a label.", "slide": "6.1-text-classification-pipeline"},
    {"slug": "traditional-text-classification", "week": 6, "title": "6.2 Traditional Text Classification", "lead": "BoW or TF-IDF features with a linear or neighbor model.", "slide": "6.2-traditional-text-classification"},
    {"slug": "intro-cnns", "week": 7, "title": "7.1 Introduction to CNNs", "lead": "Filters, padding, stride, and pooling.", "slide": "7.1-intro-cnns"},
    {"slug": "cnns-text", "week": 7, "title": "7.2 CNNs for Text", "lead": "1-D convolutions over a sequence of embeddings.", "slide": "7.2-cnns-text"},
    {"slug": "cnn-text-classification", "week": 7, "title": "7.3 CNN Text Classification", "lead": "Several kernel sizes, then a classifier on the pooled features.", "slide": "7.3-cnn-text-classification"},
    {"slug": "loopy-rnns", "week": 8, "title": "8.1 Loopy Recurrent Neural Networks", "lead": "A hidden state that reads the text one token at a time.", "slide": "8.1-loopy-rnns"},
    {"slug": "rnns-classification", "week": 8, "title": "8.2 RNNs for Text Classification", "lead": "Use the last state, or a bidirectional read, as the document vector.", "slide": "8.2-rnns-classification"},
    {"slug": "midterm", "week": 9, "title": "Midterm Review", "lead": "What the midterm covers and how to prepare."},
    {"slug": "information-extraction", "week": 10, "title": "10.1 Information Extraction", "lead": "Pull structured fields out of free text.", "slide": "10.1-information-extraction"},
    {"slug": "ie-pipeline", "week": 10, "title": "10.2 Information Extraction Pipeline", "lead": "The usual stages from a document to a filled record.", "slide": "10.2-ie-pipeline"},
    {"slug": "keyphrase-extraction", "week": 10, "title": "10.3 Keyphrase Extraction", "lead": "Find the phrases that name what a document is about.", "slide": "10.3-keyphrase-extraction"},
    {"slug": "ner", "week": 11, "title": "11.1 Named Entity Recognition", "lead": "Find people, places, organizations, and similar spans.", "slide": "11.1-ner"},
    {"slug": "other-ner-applications", "week": 11, "title": "11.2 Other NER Applications", "lead": "Linking entities and extracting relations between them.", "slide": "11.2-other-ner-applications"},
    {"slug": "chatbot-taxonomy", "week": 12, "title": "12.1 Chatbot Applications and Taxonomy", "lead": "What bots are used for, and the main design families.", "slide": "12.1-chatbot-taxonomy"},
    {"slug": "chatbot-components", "week": 12, "title": "12.2 Basic Components of a Chatbot", "lead": "NLU, dialogue state, and how a reply is chosen.", "slide": "12.2-chatbot-components"},
    {"slug": "dialog-systems", "week": 12, "title": "12.3 Dialog Systems", "lead": "Frame-based, retrieval, and generative dialogue.", "slide": "12.3-dialog-systems"},
    {"slug": "math-topic-modeling", "week": 13, "title": "13.1 Math for Topic Modeling", "lead": "Documents as mixtures, and the linear algebra underneath.", "slide": "13.1-math-topic-modeling"},
    {"slug": "svd-topic-modeling", "week": 13, "title": "13.2 SVD and Topic Modeling", "lead": "Latent semantic analysis from a word-document matrix.", "slide": "13.2-svd-topic-modeling"},
    {"slug": "lda-topic-modeling", "week": 14, "title": "14.1 LDA Topic Modeling", "lead": "A probabilistic mixture of topics for each document.", "slide": "14.1-lda-topic-modeling"},
    {"slug": "nmf-topic-modeling", "week": 14, "title": "14.2 NMF Topic Modeling", "lead": "Non-negative factors as an additive topic model.", "slide": "14.2-nmf-topic-modeling"},
    {"slug": "evaluation-topic-modeling", "week": 14, "title": "14.3 Evaluating Topic Models", "lead": "Coherence, human checks, and what a good topic looks like.", "slide": "14.3-evaluation-topic-modeling"},
    {"slug": "text-summarization", "week": 14, "title": "14.4 Text Summarization", "lead": "Extractive versus abstractive shortening of a document."},
    {"slug": "machine-translation", "week": 14, "title": "14.5 Machine Translation", "lead": "Map a sentence in one language to a sentence in another."},
    {"slug": "recommender-systems", "week": 14, "title": "14.6 Recommender Systems", "lead": "Use text (and other signals) to rank items for a user."},
]

BY_SLUG = {n["slug"]: n for n in NOTES}

WEEKS = {
    1: {
        "lectures": ["nlp-in-the-real-world", "ml-dl-nlp-overview", "python-tour"],
        "labs": [("lab-1-numpy-nltk-files", True)],
        "homework": [("Homework 1", "hwk1.pdf")],
        "readings": [
            ("Practical NLP, Ch. 1", "https://www.oreilly.com/library/view/practical-natural-language/9781492054047/"),
            ("NLTK book: Language processing and Python", "https://www.nltk.org/book/ch01.html"),
        ],
        "discussion": [
            "Name a product you use and two NLP tasks it is doing.",
            "Why does a rule-only system struggle with sarcasm or a new slang word?",
        ],
    },
    2: {
        "lectures": ["data-acquisition", "text-extraction-cleanup", "preprocessing", "advanced-preprocessing"],
        "labs": [("lab-2-text-extraction", False)],
        "homework": [("Homework 2", "hwk2.pdf")],
        "readings": [
            ("Practical NLP, Ch. 2 (pipeline)", "https://www.oreilly.com/library/view/practical-natural-language/9781492054047/"),
            ("Unicode in Python", "https://docs.python.org/3/howto/unicode.html"),
        ],
        "discussion": [
            "When is a public web scrape the wrong data source for a product classifier?",
            "Stemming or lemmatization: which would you pick for a search box, and why?",
        ],
    },
    3: {
        "lectures": ["feature-engineering", "modeling", "evaluation", "deployment-monitoring"],
        "labs": [("lab-3-fake-news", False)],
        "readings": [
            ("Practical NLP, Ch. 2 continued", "https://www.oreilly.com/library/view/practical-natural-language/9781492054047/"),
            ("sklearn: Precision, recall, F-score", "https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics"),
        ],
        "discussion": [
            "Give one intrinsic and one extrinsic way to score a tokenizer.",
            "What would you monitor after a spam filter goes live?",
        ],
    },
    4: {
        "lectures": ["text-representation-intro", "one-hot", "bow", "bonw", "tfidf"],
        "readings": [
            ("Practical NLP, Ch. 3 (text representation)", "https://www.oreilly.com/library/view/practical-natural-language/9781492054047/"),
            ("sklearn: TfidfVectorizer", "https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html"),
        ],
        "discussion": [
            "Why is a one-hot vector a poor measure of word similarity?",
            "When do bigrams help a classifier more than unigrams?",
        ],
    },
    5: {
        "lectures": ["intro-deep-learning", "distributed-representations", "word2vec-cbow", "word2vec-skipgram", "word2vec-practical"],
        "readings": [
            ("Practical NLP, Ch. 3 continued", "https://www.oreilly.com/library/view/practical-natural-language/9781492054047/"),
            ("Mikolov et al., Efficient estimation of word representations", "https://arxiv.org/abs/1301.3781"),
        ],
        "discussion": [
            "CBOW versus skip-gram: which is predicting which?",
            "What does a negative sample do in Word2Vec training?",
        ],
    },
    6: {
        "lectures": ["text-classification-pipeline", "traditional-text-classification"],
        "readings": [
            ("Practical NLP, Ch. 4 (text classification)", "https://www.oreilly.com/library/view/practical-natural-language/9781492054047/"),
            ("sklearn: Working with text data", "https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html"),
        ],
        "discussion": [
            "Where does leakage creep into a text classification split?",
            "When is logistic regression enough, and when do you want a neural net?",
        ],
    },
    7: {
        "lectures": ["intro-cnns", "cnns-text", "cnn-text-classification"],
        "readings": [
            ("Chollet, Deep Learning with Python: convnets", "https://www.manning.com/books/deep-learning-with-python-second-edition"),
            ("Kim, Convolutional neural networks for sentence classification", "https://aclanthology.org/D14-1181/"),
        ],
        "discussion": [
            "What does a kernel of size 3 see in a sentence?",
            "Why use several kernel sizes in one text CNN?",
        ],
    },
    8: {
        "lectures": ["loopy-rnns", "rnns-classification"],
        "readings": [
            ("Chollet, Deep Learning with Python: RNNs", "https://www.manning.com/books/deep-learning-with-python-second-edition"),
            ("Understanding LSTM networks (Olah)", "https://colah.github.io/posts/2015-08-Understanding-LSTMs/"),
        ],
        "discussion": [
            "What information does the hidden state have to carry to the last token?",
            "When is a bidirectional RNN worth the extra compute?",
        ],
    },
    9: {
        "lectures": ["midterm"],
        "readings": [
            ("Review notes 1.1 through 8.2", "data-641.html"),
        ],
        "discussion": [
            "Which week still feels thin: pipeline, representations, or neural classifiers?",
            "Write one exam-style question you would not want to be surprised by.",
        ],
    },
    10: {
        "lectures": ["information-extraction", "ie-pipeline", "keyphrase-extraction"],
        "readings": [
            ("Practical NLP, Ch. 5 (IE)", "https://www.oreilly.com/library/view/practical-natural-language/9781492054047/"),
            ("spaCy: Information extraction", "https://spacy.io/usage/linguistic-features"),
        ],
        "discussion": [
            "Name a product field you would extract and the span type it is.",
            "When would keyphrases be more useful than a topic label?",
        ],
    },
    11: {
        "lectures": ["ner", "other-ner-applications"],
        "readings": [
            ("Practical NLP, Ch. 5 continued", "https://www.oreilly.com/library/view/practical-natural-language/9781492054047/"),
            ("spaCy: Named entities", "https://spacy.io/usage/linguistic-features#named-entities"),
        ],
        "discussion": [
            "Why is NER sequence labeling rather than document classification?",
            "What extra work is entity linking beyond spotting a span?",
        ],
    },
    12: {
        "lectures": ["chatbot-taxonomy", "chatbot-components", "dialog-systems"],
        "readings": [
            ("Practical NLP, Ch. 6 (chatbots)", "https://www.oreilly.com/library/view/practical-natural-language/9781492054047/"),
            ("Rasa: Conversational AI", "https://rasa.com/docs/"),
        ],
        "discussion": [
            "When is a retrieval bot safer than a generative one?",
            "What belongs in dialogue state for a pizza-order bot?",
        ],
    },
    13: {
        "lectures": ["math-topic-modeling", "svd-topic-modeling"],
        "readings": [
            ("Practical NLP, Ch. 7 (topic modeling)", "https://www.oreilly.com/library/view/practical-natural-language/9781492054047/"),
            ("sklearn: TruncatedSVD", "https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html"),
        ],
        "discussion": [
            "What does a topic vector mean in LSA?",
            "Why can two documents share a topic even if they share few words?",
        ],
    },
    14: {
        "lectures": [
            "lda-topic-modeling",
            "nmf-topic-modeling",
            "evaluation-topic-modeling",
            "text-summarization",
            "machine-translation",
            "recommender-systems",
        ],
        "readings": [
            ("Blei, Probabilistic topic models", "https://www.cs.columbia.edu/~blei/papers/Blei2012.pdf"),
            ("sklearn: LatentDirichletAllocation", "https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html"),
        ],
        "discussion": [
            "LDA versus NMF: what constraint makes the factors look like topics?",
            "How would you tell a good topic model from one that only found frequent words?",
        ],
    },
}

DATA_FILES = [
    "fakeNews.csv",
    "nemo.txt",
    "sample.pdf",
    "TrainLabels.csv",
    "trueNews.csv",
]
