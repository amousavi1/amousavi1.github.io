"""Export DATA 641 Reveal.js slide HTML to one-slide-per-page PDFs."""

from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DRIVE = pathlib.Path(r"G:\My Drive\American University\Courses\Data_641\Slides")
F641 = pathlib.Path(r"F:\641\Lecture_Notes_and_Scripts\Lecture_Notes_and_Scripts")
WORK = ROOT / "files" / "data-641" / "_slide-work"
OUT = ROOT / "files" / "data-641" / "slides"

# (week, output stem, title, source HTML)
SLIDES = [
    (1, "1.1-nlp-in-the-real-world", "1.1 NLP in the Real World", DRIVE / r"Week_1_Module_1_Slides\NLP_RealWorld\NLP_in_Real_World_Slides.slides.html"),
    (1, "1.2-ml-dl-nlp-overview", "1.2 Machine Learning, Deep Learning, and NLP", DRIVE / r"Week_1_Module_1_Slides\Overview_ML_DL_NLP\Machine Learning_Deep Learning_and NLP An Overview-Slides.slides.html"),
    (1, "1.3-python-tour", "1.3 A Python Tour for NLP", DRIVE / r"Week_1_Module_1_Slides\Python_Tour\Python_Tour-Slides.slides.html"),
    (2, "2.1-data-acquisition", "2.1 Data Acquisition", DRIVE / r"Week_2_Module_2_Slides\NLP_Pipeline_Data_Acquisition_1\Lecture_2_NLP_Pipeline-Data Acquisition-Slides.slides.html"),
    (2, "2.2-text-extraction-cleanup", "2.2 Text Extraction and Cleanup", DRIVE / r"Week_2_Module_2_Slides\NLP_Pipeline_Text Extraction and Cleanup_2\Lecture_2_NLP_Pipeline_TextExtractionCleanup-Slides.slides.html"),
    (2, "2.3-preprocessing", "2.3 Preprocessing", DRIVE / r"Week_2_Module_2_Slides\NLP_Pipeline_PreProcessing_3\Lecture_2_NLP_Pipeline-Preprocessing-Slides.slides.html"),
    (2, "2.4-advanced-preprocessing", "2.4 Advanced Preprocessing", DRIVE / r"Week_2_Module_2_Slides\NLP_Pipeline_Advanced_Preprocessing_4\Lecture_2_NLP_Pipeline-AdvancedProcessing-Slides.slides.html"),
    (3, "3.1-feature-engineering", "3.1 Feature Engineering", DRIVE / r"Week_3_Module_2_Slides\NLP_Pipeline_FeatureEngineering_1\Lecture_3_NLP_Feature_Engineering--Slides.slides.html"),
    (3, "3.2-modeling", "3.2 Modeling", DRIVE / r"Week_3_Module_2_Slides\NLP_Pipeline_Modeling_2\Lecture_3_NLP_Pipeline_Modeling-Slides.slides.html"),
    (3, "3.3-evaluation", "3.3 Evaluation", DRIVE / r"Week_3_Module_2_Slides\NLP_Pipeline_Evaluation\Lecture_3_NLP_Pipeline_Evaluation-Slides.slides.html"),
    (3, "3.4-deployment-monitoring", "3.4 Deployment and Monitoring", DRIVE / r"Week_3_Module_2_Slides\NLP_Pipeline_Deployment_Monitoring\Lecture_3_NLP_Pipeline_Deployment_Monitoring-Slides.slides.html"),
    (4, "4.1-text-representation-intro", "4.1 Text Representation: Introduction", DRIVE / r"Week_4_Module_3_Slides\Text_Represenation-Introduction\Lecture_4_Text_Representation_Intro-Slides.slides.html"),
    (4, "4.2-one-hot", "4.2 One-Hot Vectors", DRIVE / r"Week_4_Module_3_Slides\Text_Representation-One Hot Vectors\Lecture_4_Text_Representation_OneHot-Slides.slides.html"),
    (4, "4.3-bow", "4.3 Bag of Words", DRIVE / r"Week_4_Module_3_Slides\Text_Representation-BOW\Lecture_4_Text_Representation-BOW-Slides.slides.html"),
    (4, "4.4-bonw", "4.4 Bag of N-Grams", DRIVE / r"Week_4_Module_3_Slides\Text_Representation-BONW\Lecture_4_Text_Representation-BONW-Slides.slides.html"),
    (4, "4.5-tfidf", "4.5 TF-IDF", DRIVE / r"Week_4_Module_3_Slides\Text_Representation-TFIDF\Lecture_4_Text_Representation-TFIDF-Slides.slides.html"),
    (5, "5.1-intro-deep-learning", "5.1 Introduction to Deep Learning", DRIVE / r"Week_5_Module_3_Slides\IntroDeepLearning\Lecture_5_DeepLearning-Slides.slides.html"),
    (5, "5.2-distributed-representations", "5.2 Distributed Representations", DRIVE / r"Week_5_Module_3_Slides\Distributed_Representations\Lecture_5_Text_Representations-Distributed_Representations.slides.html"),
    (5, "5.3-word2vec-cbow", "5.3 Word2Vec CBOW", DRIVE / r"Week_5_Module_3_Slides\Word2VecCBOW\Lecture_5_Text_Word2Vec_CBOW.slides.html"),
    (5, "5.4-word2vec-skipgram", "5.4 Word2Vec Skip-gram", DRIVE / r"Week_5_Module_3_Slides\Word2vecSkipGram\Lecture_5_Text_Word2Vec_SkipGram.slides.html"),
    (5, "5.5-word2vec-practical", "5.5 Word2Vec Practical Considerations", DRIVE / r"Week_5_Module_3_Slides\Computational_tricks_Word2Vec\Lecture_5_Word2Vec_Practical_Considerations.slides.html"),
    (6, "6.1-text-classification-pipeline", "6.1 Text Classification Pipeline", DRIVE / r"Week_6_Module_4_Slides\TextClassificationPipeline\Lecture_6_Text_Classification_Pipeline.slides.html"),
    (6, "6.2-traditional-text-classification", "6.2 Traditional Text Classification", DRIVE / r"Week_6_Module_4_Slides\Traditional_TextClassification\Lecture_6_Traditional_Text_Classification.slides.html"),
    (7, "7.1-intro-cnns", "7.1 Introduction to CNNs", DRIVE / r"Week_7_Module_4_Slides\Introduction_CNNs\Lecture_7_CNNs.slides.html"),
    (7, "7.2-cnns-text", "7.2 CNNs for Text", DRIVE / r"Week_7_Module_4_Slides\CNNs_Text\Lecture_7_CNNs_Text.slides.html"),
    (7, "7.3-cnn-text-classification", "7.3 CNN Text Classification", DRIVE / r"Week_7_Module_4_Slides\CNN_Text_Classification\Lecture_7_CNNs_Text_Classification.slides.html"),
    (8, "8.1-loopy-rnns", "8.1 Loopy Recurrent Neural Networks", DRIVE / r"Week_8_Module_4_Slides\Loopy_Recurrent_Neural_Networks\Lecture_8_Loopy_RNNs.slides.html"),
    (8, "8.2-rnns-classification", "8.2 RNNs for Text Classification", DRIVE / r"Week_8_Module_4_Slides\RNNs_Text_Classification\Lecture_8_RNNs_Classification.slides.html"),
    (10, "10.1-information-extraction", "10.1 Information Extraction", DRIVE / r"Week_10_Module_5_Slides\IE_Applications_IE_Tasks\Lecture_10_Information_Extraction.slides.html"),
    (10, "10.2-ie-pipeline", "10.2 Information Extraction Pipeline", DRIVE / r"Week_10_Module_5_Slides\General_Pipeline_IE\Lecture_10_Information_Extraction_General_Pipeline.slides.html"),
    (10, "10.3-keyphrase-extraction", "10.3 Keyphrase Extraction", DRIVE / r"Week_10_Module_5_Slides\Keyphrase_Extraction\Lecture_10_KeyphraseExtraction.slides.html"),
    (11, "11.1-ner", "11.1 Named Entity Recognition", DRIVE / r"Week_11_Module_5_Slides\NER_Building_NER_System\Lecture_11_NER.slides.html"),
    (11, "11.2-other-ner-applications", "11.2 Other NER Applications", DRIVE / r"Week_11_Module_5_Slides\Other_NER_Applications\Lecture_11_Other_NER_Applications.slides.html"),
    (12, "12.1-chatbot-taxonomy", "12.1 Chatbot Applications and Taxonomy", DRIVE / r"Week_12_Module_Slides\Applications_Taxonomy_Chatbots\Lecture_12_Applications_Taxonomy.slides.html"),
    (12, "12.2-chatbot-components", "12.2 Basic Components of a Chatbot", DRIVE / r"Week_12_Module_Slides\BasicComponents_Chatbot\Lecture_12_Basic_Components_Chatbot.slides.html"),
    (12, "12.3-dialog-systems", "12.3 Dialog Systems", DRIVE / r"Week_12_Module_Slides\DeepDive_Chatbots\Lecture_12_DeepDive_DialogSystems.slides.html"),
    (13, "13.1-math-topic-modeling", "13.1 Math for Topic Modeling", DRIVE / r"Week_13_Module_Slides\Math_for_topic_modeling\Lecture_13_Math_for_topic_modeling.slides.html"),
    (13, "13.2-svd-topic-modeling", "13.2 SVD and Topic Modeling", DRIVE / r"Week_13_Module_Slides\SVD_TopicModeling\Lecture_13_SVD_TopicModeling.slides.html"),
    (14, "14.1-lda-topic-modeling", "14.1 LDA Topic Modeling", F641 / r"Module7\Week14\LDA_TopicModeling\Lecture_14_LDA_TopicModeling.slides.html"),
    (14, "14.2-nmf-topic-modeling", "14.2 NMF Topic Modeling", F641 / r"Module7\Week14\NMF_TopicModeling\Lecture_14_NMF_TopicModeling.slides.html"),
    (14, "14.3-evaluation-topic-modeling", "14.3 Evaluating Topic Models", F641 / r"Module7\Week14\Evaluation_topic_modeling\Lecture_14_Evaluation_TopicModeling.slides.html"),
    (15, "15.1-text-summarization", "15.1 Text Summarization", F641 / r"Module7\Week15\Text_Summarization\Lecture_15_Text_Summarization.slides.html"),
    (15, "15.2-machine-translation", "15.2 Machine Translation", F641 / r"Module7\Week15\Machine_Translation\Lecture_15_Machine_Translation.slides.html"),
    (15, "15.3-recommender-systems", "15.3 Recommender Systems", F641 / r"Module7\Week15\Recommender_Systems\Lecture_15_Recommender Systems.slides.html"),
]


SLIDE_FIGURE_CSS = """
<style id="slide-figure-fit">
.reveal section img,
.reveal .slides img,
.reveal .jp-RenderedMarkdown img {
  display: block !important;
  margin: 0.4em auto !important;
  width: auto !important;
  height: auto !important;
  max-width: 82% !important;
  max-height: 48vh !important;
  object-fit: contain !important;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}
.reveal section center {
  display: block !important;
  text-align: center !important;
  width: 100% !important;
}
</style>
"""


def strip_img_size_attrs(html: str) -> str:
    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        tag = re.sub(
            r"\s+(?:width|height)\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>]+)",
            "",
            tag,
            flags=re.I,
        )
        tag = re.sub(
            r"\s+style\s*=\s*\"[^\"]*(?:width|height)[^\"]*\"",
            "",
            tag,
            flags=re.I,
        )
        return tag

    return re.sub(r"<img\b[^>]*>", repl, html, flags=re.I)


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
    text = strip_img_size_attrs(text)
    if 'id="slide-figure-fit"' not in text:
        text = text.replace("</head>", SLIDE_FIGURE_CSS + "</head>", 1)
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
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    weeks = {int(a) for a in args} if args else None
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for w, stem, _title, src in SLIDES:
        if weeks is not None and w not in weeks:
            continue
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
