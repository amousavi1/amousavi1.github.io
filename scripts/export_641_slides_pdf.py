"""Export DATA 641 Reveal.js slide HTML to one-slide-per-page PDFs."""

from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = pathlib.Path(r"G:\My Drive\American University\Courses\Data_641\Slides")
WORK = ROOT / "files" / "data-641" / "_slide-work"
OUT = ROOT / "files" / "data-641" / "slides"

# (week, output stem, title, source relative to SRC)
SLIDES = [
    (1, "1.1-nlp-in-the-real-world", "1.1 NLP in the Real World", r"Week_1_Module_1_Slides\NLP_RealWorld\NLP_in_Real_World_Slides.slides.html"),
    (1, "1.2-ml-dl-nlp-overview", "1.2 Machine Learning, Deep Learning, and NLP", r"Week_1_Module_1_Slides\Overview_ML_DL_NLP\Machine Learning_Deep Learning_and NLP An Overview-Slides.slides.html"),
    (1, "1.3-python-tour", "1.3 A Python Tour for NLP", r"Week_1_Module_1_Slides\Python_Tour\Python_Tour-Slides.slides.html"),
    (2, "2.1-data-acquisition", "2.1 Data Acquisition", r"Week_2_Module_2_Slides\NLP_Pipeline_Data_Acquisition_1\Lecture_2_NLP_Pipeline-Data Acquisition-Slides.slides.html"),
    (2, "2.2-text-extraction-cleanup", "2.2 Text Extraction and Cleanup", r"Week_2_Module_2_Slides\NLP_Pipeline_Text Extraction and Cleanup_2\Lecture_2_NLP_Pipeline_TextExtractionCleanup-Slides.slides.html"),
    (2, "2.3-preprocessing", "2.3 Preprocessing", r"Week_2_Module_2_Slides\NLP_Pipeline_PreProcessing_3\Lecture_2_NLP_Pipeline-Preprocessing-Slides.slides.html"),
    (2, "2.4-advanced-preprocessing", "2.4 Advanced Preprocessing", r"Week_2_Module_2_Slides\NLP_Pipeline_Advanced_Preprocessing_4\Lecture_2_NLP_Pipeline-AdvancedProcessing-Slides.slides.html"),
    (3, "3.1-feature-engineering", "3.1 Feature Engineering", r"Week_3_Module_2_Slides\NLP_Pipeline_FeatureEngineering_1\Lecture_3_NLP_Feature_Engineering--Slides.slides.html"),
    (3, "3.2-modeling", "3.2 Modeling", r"Week_3_Module_2_Slides\NLP_Pipeline_Modeling_2\Lecture_3_NLP_Pipeline_Modeling-Slides.slides.html"),
    (3, "3.3-evaluation", "3.3 Evaluation", r"Week_3_Module_2_Slides\NLP_Pipeline_Evaluation\Lecture_3_NLP_Pipeline_Evaluation-Slides.slides.html"),
    (3, "3.4-deployment-monitoring", "3.4 Deployment and Monitoring", r"Week_3_Module_2_Slides\NLP_Pipeline_Deployment_Monitoring\Lecture_3_NLP_Pipeline_Deployment_Monitoring-Slides.slides.html"),
    (4, "4.1-text-representation-intro", "4.1 Text Representation: Introduction", r"Week_4_Module_3_Slides\Text_Represenation-Introduction\Lecture_4_Text_Representation_Intro-Slides.slides.html"),
    (4, "4.2-one-hot", "4.2 One-Hot Vectors", r"Week_4_Module_3_Slides\Text_Representation-One Hot Vectors\Lecture_4_Text_Representation_OneHot-Slides.slides.html"),
    (4, "4.3-bow", "4.3 Bag of Words", r"Week_4_Module_3_Slides\Text_Representation-BOW\Lecture_4_Text_Representation-BOW-Slides.slides.html"),
    (4, "4.4-bonw", "4.4 Bag of N-Grams", r"Week_4_Module_3_Slides\Text_Representation-BONW\Lecture_4_Text_Representation-BONW-Slides.slides.html"),
    (4, "4.5-tfidf", "4.5 TF-IDF", r"Week_4_Module_3_Slides\Text_Representation-TFIDF\Lecture_4_Text_Representation-TFIDF-Slides.slides.html"),
    (5, "5.1-intro-deep-learning", "5.1 Introduction to Deep Learning", r"Week_5_Module_3_Slides\IntroDeepLearning\Lecture_5_DeepLearning-Slides.slides.html"),
    (5, "5.2-distributed-representations", "5.2 Distributed Representations", r"Week_5_Module_3_Slides\Distributed_Representations\Lecture_5_Text_Representations-Distributed_Representations.slides.html"),
    (5, "5.3-word2vec-cbow", "5.3 Word2Vec CBOW", r"Week_5_Module_3_Slides\Word2VecCBOW\Lecture_5_Text_Word2Vec_CBOW.slides.html"),
    (5, "5.4-word2vec-skipgram", "5.4 Word2Vec Skip-gram", r"Week_5_Module_3_Slides\Word2vecSkipGram\Lecture_5_Text_Word2Vec_SkipGram.slides.html"),
    (5, "5.5-word2vec-practical", "5.5 Word2Vec Practical Considerations", r"Week_5_Module_3_Slides\Computational_tricks_Word2Vec\Lecture_5_Word2Vec_Practical_Considerations.slides.html"),
    (6, "6.1-text-classification-pipeline", "6.1 Text Classification Pipeline", r"Week_6_Module_4_Slides\TextClassificationPipeline\Lecture_6_Text_Classification_Pipeline.slides.html"),
    (6, "6.2-traditional-text-classification", "6.2 Traditional Text Classification", r"Week_6_Module_4_Slides\Traditional_TextClassification\Lecture_6_Traditional_Text_Classification.slides.html"),
    (7, "7.1-intro-cnns", "7.1 Introduction to CNNs", r"Week_7_Module_4_Slides\Introduction_CNNs\Lecture_7_CNNs.slides.html"),
    (7, "7.2-cnns-text", "7.2 CNNs for Text", r"Week_7_Module_4_Slides\CNNs_Text\Lecture_7_CNNs_Text.slides.html"),
    (7, "7.3-cnn-text-classification", "7.3 CNN Text Classification", r"Week_7_Module_4_Slides\CNN_Text_Classification\Lecture_7_CNNs_Text_Classification.slides.html"),
    (8, "8.1-loopy-rnns", "8.1 Loopy Recurrent Neural Networks", r"Week_8_Module_4_Slides\Loopy_Recurrent_Neural_Networks\Lecture_8_Loopy_RNNs.slides.html"),
    (8, "8.2-rnns-classification", "8.2 RNNs for Text Classification", r"Week_8_Module_4_Slides\RNNs_Text_Classification\Lecture_8_RNNs_Classification.slides.html"),
    (10, "10.1-information-extraction", "10.1 Information Extraction", r"Week_10_Module_5_Slides\IE_Applications_IE_Tasks\Lecture_10_Information_Extraction.slides.html"),
    (10, "10.2-ie-pipeline", "10.2 Information Extraction Pipeline", r"Week_10_Module_5_Slides\General_Pipeline_IE\Lecture_10_Information_Extraction_General_Pipeline.slides.html"),
    (10, "10.3-keyphrase-extraction", "10.3 Keyphrase Extraction", r"Week_10_Module_5_Slides\Keyphrase_Extraction\Lecture_10_KeyphraseExtraction.slides.html"),
    (11, "11.1-ner", "11.1 Named Entity Recognition", r"Week_11_Module_5_Slides\NER_Building_NER_System\Lecture_11_NER.slides.html"),
    (11, "11.2-other-ner-applications", "11.2 Other NER Applications", r"Week_11_Module_5_Slides\Other_NER_Applications\Lecture_11_Other_NER_Applications.slides.html"),
    (12, "12.1-chatbot-taxonomy", "12.1 Chatbot Applications and Taxonomy", r"Week_12_Module_Slides\Applications_Taxonomy_Chatbots\Lecture_12_Applications_Taxonomy.slides.html"),
    (12, "12.2-chatbot-components", "12.2 Basic Components of a Chatbot", r"Week_12_Module_Slides\BasicComponents_Chatbot\Lecture_12_Basic_Components_Chatbot.slides.html"),
    (12, "12.3-dialog-systems", "12.3 Dialog Systems", r"Week_12_Module_Slides\DeepDive_Chatbots\Lecture_12_DeepDive_DialogSystems.slides.html"),
    (13, "13.1-math-topic-modeling", "13.1 Math for Topic Modeling", r"Week_13_Module_Slides\Math_for_topic_modeling\Lecture_13_Math_for_topic_modeling.slides.html"),
    (13, "13.2-svd-topic-modeling", "13.2 SVD and Topic Modeling", r"Week_13_Module_Slides\SVD_TopicModeling\Lecture_13_SVD_TopicModeling.slides.html"),
]


def copy_deck(html_src: pathlib.Path, dest_dir: pathlib.Path) -> pathlib.Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_html = dest_dir / "slides.html"
    text = html_src.read_text(encoding="utf-8", errors="ignore")
    # DeckTape's Reveal plugin needs a global Reveal; these decks load it via RequireJS.
    if "window.Reveal = Reveal" not in text:
        text = text.replace(
            "Reveal.initialize({",
            "window.Reveal = Reveal;\n        Reveal.initialize({",
            1,
        )
    dest_html.write_text(text, encoding="utf-8")
    for item in html_src.parent.iterdir():
        if item.name.startswith("."):
            continue
        if item.is_dir():
            continue
        if item.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}:
            shutil.copy2(item, dest_dir / item.name)
    return dest_html


def export_pdf(html_path: pathlib.Path, pdf_path: pathlib.Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    uri = html_path.resolve().as_uri()
    cmd = [
        "npx",
        "--yes",
        "decktape",
        "reveal",
        uri,
        str(pdf_path),
        "--size",
        "1920x1080",
        "--pause",
        "1000",
        "--load-pause",
        "4000",
    ]
    subprocess.run(cmd, check=True, shell=True)


def main() -> None:
    week = None
    if len(sys.argv) > 1:
        week = int(sys.argv[1])
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for w, stem, _title, rel in SLIDES:
        if week is not None and w != week:
            continue
        src = SRC / rel
        if not src.exists():
            raise FileNotFoundError(src)
        dest = WORK / stem
        pdf = OUT / f"{stem}.pdf"
        if pdf.exists() and "--force" not in sys.argv:
            print(f"Skip existing {pdf.name}")
            continue
        html = copy_deck(src, dest)
        print(f"Exporting {stem} ...")
        export_pdf(html, pdf)
        print(f"Wrote {pdf} ({pdf.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
