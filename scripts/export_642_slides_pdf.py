"""Export DATA 642 Reveal.js lecture notebooks to one-slide-per-page PDFs."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from export_641_slides_pdf import (  # noqa: E402
    build_from_notebook,
    copy_deck,
    export_pdf,
    find_notebook as find_notebook_641,
    notebook_slide_count,
    pdf_pages,
)

DRIVE = pathlib.Path(r"G:\My Drive\American University\Courses\Data_642\Lectures")
WORK = ROOT / "files" / "data-642" / "_slide-work"
OUT = ROOT / "files" / "data-642" / "slides"

SKIP_NOTEBOOKS = {"figure.ipynb"}

# (week, output stem, title, source slides HTML)
SLIDES = [
    (1, "1.1-ml-basics", "1.1 Machine Learning Basics", DRIVE / r"Module1\Week1\1-ML_Basics\Lecture_ML_Basics.slides.html"),
    (1, "1.2-vector-calc-motivation", "1.2 Why Vector Calculus", DRIVE / r"Module1\Week1\2-Motivation_VectorCalc\Intro_Vector_Calc.slides.html"),
    (1, "1.3-derivatives", "1.3 Derivatives for Optimization", DRIVE / r"Module1\Week1\3-Derivatives_Optimization_Intro\Intro_to_derivatives.slides.html"),
    (1, "1.4-vector-calculus", "1.4 Basic Vector Calculus", DRIVE / r"Module1\Week1\4-Basic_Vector_Calculus\Basics_Vector_Calculus.slides.html"),
    (2, "2.1-intro-optimization", "2.1 Introduction to Optimization", DRIVE / r"Module1\Week2\Introduction to Optimization\Intro_to_optimization.slides.html"),
    (2, "2.2-unconstrained-methods", "2.2 Unconstrained Methods", DRIVE / r"Module1\Week2\Methods_Uncostrained_Optimization\Methods_Unconstrained_Optimization.slides.html"),
    (2, "2.3-second-order", "2.3 Second-Order Methods", DRIVE / r"Module1\Week2\Second_Order_Optimization\Second_Order_Optimization.slides.html"),
    (3, "3.1-constrained-optimization", "3.1 Constrained Optimization", DRIVE / r"Module1\Week3\Constrained_Optimization\Constrained_Optimization.slides.html"),
    (3, "3.2-linear-programming", "3.2 Linear Programming", DRIVE / r"Module1\Week3\Linear_Programming\Linear_Programming.slides.html"),
    (3, "3.3-quadratic-programming", "3.3 Quadratic Programming", DRIVE / r"Module1\Week3\Quadratic_Programming\Quadratic_Programming.slides.html"),
    (4, "4.1-sparsity-motivation", "4.1 Motivation for Sparsity-Aware Learning", DRIVE / r"Module2\Week4\Motivation_Sparsity_Aware_Learning\Motivation_Sparsity_Aware_Learning.slides.html"),
    (4, "4.2-ridge-regression", "4.2 Ridge Regression", DRIVE / r"Module2\Week4\Shrinkage_Ridge_Regression\Ridge_Regression.slides.html"),
    (4, "4.3-lasso", "4.3 LASSO", DRIVE / r"Module2\Week4\LASSO\LASSO.slides.html"),
    (4, "4.4-sparsity-practical", "4.4 Practical Considerations", DRIVE / r"Module2\Week4\Practical_Considerations\Practical_Considerations.slides.html"),
    (5, "5.1-hilbert-spaces", "5.1 Hilbert Spaces", DRIVE / r"Module3\Week5\HilbertSpaces\Hilbert_Spaces.slides.html"),
    (5, "5.2-kernel-ridge", "5.2 Kernel Ridge Regression", DRIVE / r"Module3\Week5\Kernel_Ridge_Regression\Kernel Ridge Regression.slides.html"),
    (5, "5.3-svms", "5.3 Support Vector Machines", DRIVE / r"Module3\Week5\SVMs\SVMs.slides.html"),
    (6, "6.1-intro-pca", "6.1 Introduction to PCA", DRIVE / r"Module4\Week6\Introduction_to_PCA\Intro_PCA.slides.html"),
    (6, "6.2-kernel-pca", "6.2 Kernel PCA", DRIVE / r"Module4\Week6\Kernel_PCA\Kernel_PCA.slides.html"),
    (6, "6.3-pca-special", "6.3 Special Considerations for PCA", DRIVE / r"Module4\Week6\Special_considerations_PCA\Special_considerations.slides.html"),
    (7, "7.1-multimodal-learning", "7.1 Multimodal Learning", DRIVE / r"Module4\Week7\Intro_MultiModal_Learning\Multi_modal_learning.slides.html"),
    (7, "7.2-cca", "7.2 Canonical Correlation Analysis", DRIVE / r"Module4\Week7\Introduction_to_CCA\CCA.slides.html"),
    (7, "7.3-iva", "7.3 Independent Vector Analysis", DRIVE / r"Module4\Week7\Intorduction_to_IVA\Independent_Vector_Analysis.slides.html"),
    (8, "8.1-intro-tensors", "8.1 Introduction to Tensors", DRIVE / r"Module4\Week8\Introduction_to_Tensors\Intro_Tensors.slides.html"),
    (8, "8.2-tensor-decomposition", "8.2 Tensor Decomposition Algorithms", DRIVE / r"Module4\Week8\Tensor_Decomposition_Algorithms\Tensor Decomposition Algorithm.slides.html"),
    (8, "8.3-tensors-ml", "8.3 Tensors and Machine Learning", DRIVE / r"Module4\Week8\Connection_Machine_Learning\Connection_to_ML.slides.html"),
    (10, "10.1-clustering-kmeans", "10.1 Clustering and K-Means", DRIVE / r"Module5\Week10\Clustering_Kmeans\Clustering.slides.html"),
    (10, "10.2-clustering-segmentation", "10.2 Clustering for Image Segmentation", DRIVE / r"Module5\Week10\Clustering_Image_Segmentation\Clustering_Image_Segmentation.slides.html"),
    (10, "10.3-clustering-other", "10.3 Other Clustering Algorithms", DRIVE / r"Module5\Week10\Clustering_Other_Algorithms\Clustering_Other_Alogorithms.slides.html"),
    (10, "10.4-clustering-semi-supervised", "10.4 Clustering and Semi-Supervised Learning", DRIVE / r"Module5\Week10\Clustering_Semi_Supervised_Learning\Clustering_Semi_Supervised_Learning.slides.html"),
    (11, "11.1-gmms", "11.1 Gaussian Mixture Models", DRIVE / r"Module5\Week11\Gaussian_Mixtures\Gaussian_Mixture_Model.slides.html"),
    (11, "11.2-gmms-anomaly", "11.2 GMMs for Anomaly Detection", DRIVE / r"Module5\Week11\GMMs_Anomaly_Detection\GMMs_Anomaly_Detection.slides.html"),
    (11, "11.3-gmms-practical", "11.3 Practical Considerations", DRIVE / r"Module5\Week11\Practical_Considerations\Practical_Considerations.slides.html"),
    (12, "12.1-neural-networks", "12.1 Neural Networks and the Perceptron", DRIVE / r"Module6\Week12\Neural_Networks_Perceptron\Neural_Networks.slides.html"),
    (12, "12.2-multilayer-nets", "12.2 Multilayer Neural Networks", DRIVE / r"Module6\Week12\Multilayer_Neural_Networks\Multi_Layer_Neural_Networks.slides.html"),
    (12, "12.3-training-nns", "12.3 Training Neural Networks", DRIVE / r"Module6\Week12\Training_NN_Intuitive\Training_Neural_Networks.slides.html"),
    (13, "13.1-backprop-challenges", "13.1 Back-Propagation Challenges", DRIVE / r"Module6\Week13\Back_Propagation_Challenges_learning\Back_Propagation_Challenges.slides.html"),
    (13, "13.2-faster-optimizers", "13.2 Faster Optimizers", DRIVE / r"Module6\Week13\Faster_optimizers\FasterOptimizers.slides.html"),
    (13, "13.3-hyperparameters", "13.3 Hyperparameters", DRIVE / r"Module6\Week13\Hyperparameters\Hyperparameters.slides.html"),
    (13, "13.4-regularization", "13.4 Regularization", DRIVE / r"Module6\Week13\Regularization\Regularizations.slides.html"),
    (14, "14.1-autoencoders-intro", "14.1 Autoencoders", DRIVE / r"Module6\Week14\Autoencoders_Intro\Autoencoders_Intro.slides.html"),
    (14, "14.2-autoencoders-part-ii", "14.2 Autoencoders, Part II", DRIVE / r"Module6\Week14\Autoencoders_Part_II\Autoencoders_Part_II.slides.html"),
    (14, "14.3-vaes", "14.3 Variational Autoencoders", DRIVE / r"Module6\Week14\Variational_Autoencoders\Variational_Autoencoders.slides.html"),
    (15, "15.1-intro-gans", "15.1 Introduction to GANs", DRIVE / r"Module6\Week15\Intorduction_GANs\Introduction_to_GANs.slides.html"),
    (15, "15.2-notes-gans", "15.2 Notes on GANs", DRIVE / r"Module6\Week15\Notes_GANs\Notes_GANs.slides.html"),
    (15, "15.3-evaluating-gans", "15.3 Evaluating GANs", DRIVE / r"Module6\Week15\Evaluating_GANs\Evaluating_GANs.slides.html"),
]


def find_notebook(html_src: pathlib.Path) -> pathlib.Path | None:
    nbs = [
        p
        for p in html_src.parent.glob("*.ipynb")
        if ".ipynb_checkpoints" not in str(p)
        and "checkpoint" not in p.name.lower()
        and "handout" not in p.name.lower()
        and p.name.lower() not in SKIP_NOTEBOOKS
    ]
    if not nbs:
        return None
    stem = html_src.name.replace(".slides.html", "")
    for p in nbs:
        if p.stem == stem or p.stem.replace("-Slides", "") in stem:
            return p
    slides = [p for p in nbs if "slide" in p.name.lower()]
    return slides[0] if slides else nbs[0]


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    weeks = {int(a) for a in args} if args else None
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    missing = [src for _w, _stem, _title, src in SLIDES if not src.exists()]
    if missing:
        raise FileNotFoundError("\n".join(str(p) for p in missing))
    for w, stem, _title, src in SLIDES:
        if weeks is not None and w not in weeks:
            continue
        dest = WORK / stem
        pdf = OUT / f"{stem}.pdf"
        if pdf.exists() and "--force" not in sys.argv:
            print(f"Skip existing {pdf.name}")
            continue
        nb = find_notebook(src) or find_notebook_641(src)
        expected = notebook_slide_count(nb) if nb else None
        if nb:
            print(f"Building {stem} from {nb.name} ({expected} slides) ...", flush=True)
            html = build_from_notebook(nb, dest)
        else:
            print(f"No notebook for {stem}; using existing slides HTML", flush=True)
            html = copy_deck(src, dest)
        export_pdf(html, pdf)
        pages = pdf_pages(pdf)
        extra = f", expected {expected}" if expected is not None else ""
        print(f"Wrote {pdf.name} ({pages} pages{extra}, {pdf.stat().st_size} bytes)", flush=True)


if __name__ == "__main__":
    main()
