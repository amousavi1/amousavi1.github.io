"""Complementary notes and past practice, mapped onto DATA 641 and 642 weeks.

Sources live in files/Notes___641_and_642 and files/Quizzes___641and_642.
Compiled PDFs go to files/<course>/extra/.

kind: notes | practice | homework
assign: list of (course, week)
"""

from __future__ import annotations

NOTES = "files/Notes___641_and_642"
Q641 = "files/Quizzes___641and_642/641"
Q642 = "files/Quizzes___641and_642/642"

# Skip live/reusable exams: Final_exam.tex, final.tex, final_exam.tex, midterm.tex
ITEMS = [
    # --- 641 notes ---
    {"src": f"{NOTES}/preprocessing.tex", "pdf": "preprocessing.pdf", "title": "Preprocessing notes", "kind": "notes", "assign": [("data-641", 2)]},
    {"src": f"{NOTES}/preprocessing_pipline.tex", "pdf": "preprocessing-pipeline.pdf", "title": "Preprocessing pipeline", "kind": "notes", "assign": [("data-641", 2)]},
    {"src": f"{NOTES}/pos_tagging.tex", "pdf": "pos-tagging.pdf", "title": "POS tagging", "kind": "notes", "assign": [("data-641", 2)]},
    {"src": f"{NOTES}/Embeddings.tex", "pdf": "embeddings.pdf", "title": "Embeddings", "kind": "notes", "assign": [("data-641", 5)]},
    {"src": f"{NOTES}/SVM.tex", "pdf": "svm.pdf", "title": "SVM as a QP", "kind": "notes", "assign": [("data-641", 6), ("data-642", 5)]},
    {"src": f"{NOTES}/CNNs.tex", "pdf": "cnns.pdf", "title": "CNNs", "kind": "notes", "assign": [("data-641", 7), ("data-642", 15)]},
    {"src": f"{NOTES}/Sequential_Data.tex", "pdf": "sequential-data.pdf", "title": "Handling sequential data", "kind": "notes", "assign": [("data-641", 8)]},
    {"src": f"{NOTES}/RNNs.tex", "pdf": "rnns.pdf", "title": "Recurrent neural networks", "kind": "notes", "assign": [("data-641", 8), ("data-642", 15)]},
    {"src": f"{NOTES}/LSTMs.tex", "pdf": "lstms.pdf", "title": "LSTMs", "kind": "notes", "assign": [("data-641", 8)]},
    {"src": f"{NOTES}/GRUs.tex", "pdf": "grus.pdf", "title": "GRUs", "kind": "notes", "assign": [("data-641", 8)]},
    {"src": f"{NOTES}/Information_Extraction.tex", "pdf": "information-extraction.pdf", "title": "Information extraction pipeline", "kind": "notes", "assign": [("data-641", 10)]},
    {"src": f"{NOTES}/Transformers.tex", "pdf": "transformers.pdf", "title": "Transformers", "kind": "notes", "assign": [("data-641", 12)]},
    {"src": f"{NOTES}/BERT.tex", "pdf": "bert.pdf", "title": "BERT", "kind": "notes", "assign": [("data-641", 12)]},
    {"src": f"{NOTES}/GPT.tex", "pdf": "gpt.pdf", "title": "GPT", "kind": "notes", "assign": [("data-641", 12)]},
    {"src": f"{NOTES}/Prompt_engineering.tex", "pdf": "prompt-engineering.pdf", "title": "Prompt engineering", "kind": "notes", "assign": [("data-641", 12)]},
    {"src": f"{NOTES}/Token_by_token.tex", "pdf": "token-by-token.pdf", "title": "Token-by-token training", "kind": "notes", "assign": [("data-641", 12)]},
    {"src": f"{NOTES}/Sentiment_attention.tex", "pdf": "sentiment-attention.pdf", "title": "Sentiment with multi-head attention", "kind": "notes", "assign": [("data-641", 12)]},
    {"src": f"{NOTES}/Pretraining.tex", "pdf": "pretraining.pdf", "title": "Pretraining", "kind": "notes", "assign": [("data-641", 12), ("data-642", 15)]},
    {"src": f"{NOTES}/Fine-tuning.tex", "pdf": "fine-tuning.pdf", "title": "Fine-tuning", "kind": "notes", "assign": [("data-641", 12), ("data-642", 15)]},
    {"src": f"{NOTES}/Transfer_Learning.tex", "pdf": "transfer-learning.pdf", "title": "Transfer learning", "kind": "notes", "assign": [("data-641", 12), ("data-642", 15)]},
    {"src": f"{NOTES}/Seq2seq_models_loss.tex", "pdf": "seq2seq-loss.pdf", "title": "Seq2seq models and loss", "kind": "notes", "assign": [("data-641", 14)]},
    {"src": f"{NOTES}/Sequence_generating_models_evaluation.tex", "pdf": "sequence-eval.pdf", "title": "Evaluating sequence models", "kind": "notes", "assign": [("data-641", 14)]},
    {"src": f"{NOTES}/Forecast.tex", "pdf": "forecast.pdf", "title": "Forecasting with sequential models", "kind": "notes", "assign": [("data-641", 14)]},
    {"src": f"{Q641}/recom.tex", "pdf": "recommenders-extra.pdf", "title": "Recommender notes", "kind": "notes", "assign": [("data-641", 14)]},
    {"src": f"{NOTES}/Self-supervised_learning.tex", "pdf": "self-supervised.pdf", "title": "Self-supervised learning", "kind": "notes", "assign": [("data-641", 14), ("data-642", 15)]},
    {"src": f"{NOTES}/One_shot_learning.tex", "pdf": "one-shot.pdf", "title": "One-shot learning", "kind": "notes", "assign": [("data-641", 14), ("data-642", 15)]},
    # --- 641 practice (past quizzes / sample exam; not the live final) ---
    {"src": f"{Q641}/Quiz1.tex", "pdf": "quiz-1.pdf", "title": "Quiz 1 (practice)", "kind": "practice", "assign": [("data-641", 2)]},
    {"src": f"{Q641}/Quiz1_solutions.tex", "pdf": "quiz-1-solutions.pdf", "title": "Quiz 1 solutions", "kind": "practice", "assign": [("data-641", 2)]},
    {"src": f"{Q641}/Quiz2.tex", "pdf": "quiz-2.pdf", "title": "Quiz 2 (practice)", "kind": "practice", "assign": [("data-641", 5)]},
    {"src": f"{Q641}/Quiz2_solutions.tex", "pdf": "quiz-2-solutions.pdf", "title": "Quiz 2 solutions", "kind": "practice", "assign": [("data-641", 5)]},
    {"src": f"{Q641}/Quiz3.tex", "pdf": "quiz-3.pdf", "title": "Quiz 3 (practice)", "kind": "practice", "assign": [("data-641", 9)]},
    {"src": f"{Q641}/Quiz3_solutions.tex", "pdf": "quiz-3-solutions.pdf", "title": "Quiz 3 solutions", "kind": "practice", "assign": [("data-641", 9)]},
    {"src": f"{Q641}/Quiz4_solutions.tex", "pdf": "quiz-4-solutions.pdf", "title": "Quiz 4 solutions", "kind": "practice", "assign": [("data-641", 12)]},
    {"src": f"{Q641}/Final_sample.tex", "pdf": "final-sample.pdf", "title": "Final exam sample", "kind": "practice", "assign": [("data-641", 14)]},
    # --- 642 numbered notes ---
    {"src": f"{NOTES}/642-1-ML_Math_Basics.tex", "pdf": "642-1-ml-math-basics.pdf", "title": "1. ML math basics", "kind": "notes", "assign": [("data-642", 1)]},
    {"src": f"{NOTES}/Linear_regression.tex", "pdf": "linear-regression.pdf", "title": "OLS variance and residuals", "kind": "notes", "assign": [("data-642", 1)]},
    {"src": f"{NOTES}/Loss_functions.tex", "pdf": "loss-functions.pdf", "title": "Loss functions", "kind": "notes", "assign": [("data-642", 1)]},
    {"src": f"{NOTES}/642-Loss-Functions.tex", "pdf": "642-loss-functions.pdf", "title": "Loss functions (course notes)", "kind": "notes", "assign": [("data-642", 1)]},
    {"src": f"{NOTES}/bias.tex", "pdf": "bias.pdf", "title": "Bias", "kind": "notes", "assign": [("data-642", 1)]},
    {"src": f"{NOTES}/642-2-Eigenpairs and PSD.tex", "pdf": "642-2-eigenpairs-psd.pdf", "title": "2. Eigenpairs and PSD matrices", "kind": "notes", "assign": [("data-642", 2)]},
    {"src": f"{NOTES}/642-Optimization Methods.tex", "pdf": "642-optimization-methods.pdf", "title": "Optimization methods", "kind": "notes", "assign": [("data-642", 2)]},
    {"src": f"{NOTES}/642-3-GD and Newton's Methods.tex", "pdf": "642-3-gd-newton.pdf", "title": "3. Gradient descent and Newton", "kind": "notes", "assign": [("data-642", 2)]},
    {"src": f"{NOTES}/642-4-Necessary and Sufficient Conds.tex", "pdf": "642-4-optimality.pdf", "title": "4. Necessary and sufficient conditions", "kind": "notes", "assign": [("data-642", 3)]},
    {"src": f"{NOTES}/642-5-Dual Theory.tex", "pdf": "642-5-dual-theory.pdf", "title": "5. Dual theory", "kind": "notes", "assign": [("data-642", 3)]},
    {"src": f"{NOTES}/ADMM_vs_PD.tex", "pdf": "admm-vs-pd.pdf", "title": "ADMM versus primal-dual", "kind": "notes", "assign": [("data-642", 3)]},
    {"src": f"{NOTES}/Augmented_Lagrangian_Method.tex", "pdf": "augmented-lagrangian.pdf", "title": "Augmented Lagrangian", "kind": "notes", "assign": [("data-642", 3)]},
    {"src": f"{NOTES}/642-6-Kernel Methods.tex", "pdf": "642-6-kernel-methods.pdf", "title": "6. Kernel methods", "kind": "notes", "assign": [("data-642", 5)]},
    {"src": f"{NOTES}/642-7-SVM.tex", "pdf": "642-7-svm.pdf", "title": "7. Support vector machines", "kind": "notes", "assign": [("data-642", 5)]},
    {"src": f"{NOTES}/642-16-Perceptron.tex", "pdf": "642-16-perceptron.pdf", "title": "16. Perceptron", "kind": "notes", "assign": [("data-642", 12)]},
    {"src": f"{NOTES}/Twin_SVM.tex", "pdf": "twin-svm.pdf", "title": "Twin SVM", "kind": "notes", "assign": [("data-642", 5)]},
    {"src": f"{NOTES}/One-Class-SVM.tex", "pdf": "one-class-svm.pdf", "title": "One-class SVM", "kind": "notes", "assign": [("data-642", 11)]},
    {"src": f"{NOTES}/SVM_TR.tex", "pdf": "svm-tr.pdf", "title": "SVM (technical remarks)", "kind": "notes", "assign": [("data-642", 5)]},
    {"src": f"{NOTES}/Ensemble_learning.tex", "pdf": "ensemble-learning.pdf", "title": "Ensemble learning", "kind": "notes", "assign": [("data-642", 12)]},
    {"src": f"{NOTES}/Incorporating_Heuristics.tex", "pdf": "heuristics.pdf", "title": "Incorporating heuristics", "kind": "notes", "assign": [("data-642", 12)]},
    {"src": f"{NOTES}/Clustering.tex", "pdf": "clustering.pdf", "title": "Clustering", "kind": "notes", "assign": [("data-642", 10)]},
    {"src": f"{NOTES}/GMMs.tex", "pdf": "gmms.pdf", "title": "Gaussian mixture models", "kind": "notes", "assign": [("data-642", 11)]},
    {"src": f"{NOTES}/642-15-GMMs.tex", "pdf": "642-15-gmms.pdf", "title": "15. Gaussian mixture models", "kind": "notes", "assign": [("data-642", 11)]},
    {"src": f"{NOTES}/PCA.tex", "pdf": "pca.pdf", "title": "PCA", "kind": "notes", "assign": [("data-642", 6)]},
    {"src": f"{NOTES}/Matrix_Factorization.tex", "pdf": "matrix-factorization.pdf", "title": "Matrix factorization", "kind": "notes", "assign": [("data-641", 14), ("data-642", 6)]},
    {"src": f"{NOTES}/ICA.tex", "pdf": "ica.pdf", "title": "Independent component analysis", "kind": "notes", "assign": [("data-642", 7)]},
    {"src": f"{NOTES}/ICA1.tex", "pdf": "ica-extended.pdf", "title": "ICA (extended notes)", "kind": "notes", "assign": [("data-642", 7)]},
    {"src": f"{NOTES}/IVA.tex", "pdf": "iva.pdf", "title": "Independent vector analysis", "kind": "notes", "assign": [("data-642", 7)]},
    {"src": f"{NOTES}/CCA.tex", "pdf": "cca.pdf", "title": "Canonical correlation analysis", "kind": "notes", "assign": [("data-642", 7)]},
    {"src": f"{NOTES}/Tensors.tex", "pdf": "tensors.pdf", "title": "Tensors", "kind": "notes", "assign": [("data-642", 8)]},
    {"src": f"{NOTES}/Multimodal_Learning.tex", "pdf": "multimodal-learning.pdf", "title": "Multimodal learning", "kind": "notes", "assign": [("data-642", 7)]},
    {"src": f"{NOTES}/Multi_modal.tex", "pdf": "multimodal.pdf", "title": "Multimodal methods", "kind": "notes", "assign": [("data-642", 7)]},
    {"src": f"{NOTES}/CLIP.tex", "pdf": "clip.pdf", "title": "CLIP", "kind": "notes", "assign": [("data-642", 7)]},
    {"src": f"{NOTES}/Embeddings_images.tex", "pdf": "embeddings-images.pdf", "title": "Image embeddings", "kind": "notes", "assign": [("data-642", 7)]},
    {"src": f"{NOTES}/NNs.tex", "pdf": "neural-nets.pdf", "title": "Neural networks", "kind": "notes", "assign": [("data-642", 12)]},
    {"src": f"{NOTES}/back-propagation.tex", "pdf": "backpropagation.pdf", "title": "Back-propagation", "kind": "notes", "assign": [("data-642", 13)]},
    {"src": f"{NOTES}/autoencoders.tex", "pdf": "autoencoders.pdf", "title": "Autoencoders", "kind": "notes", "assign": [("data-642", 14)]},
    {"src": f"{NOTES}/U-net.tex", "pdf": "unet.pdf", "title": "U-Net", "kind": "notes", "assign": [("data-642", 14)]},
    {"src": f"{Q642}/notes_on_U-net.tex", "pdf": "unet-notes.pdf", "title": "U-Net notes", "kind": "notes", "assign": [("data-642", 14)]},
    # --- 642 homework / practice ---
    {"src": f"{NOTES}/642-0-extra_credit_homework.tex", "pdf": "extra-credit-hw.pdf", "title": "Extra-credit homework (Module 1)", "kind": "homework", "assign": [("data-642", 3)]},
    {"src": f"{Q642}/main.tex", "pdf": "extra-credit-exercises.pdf", "title": "Extra-credit exercises (Module 1)", "kind": "homework", "assign": [("data-642", 3)]},
    {"src": f"{Q642}/lab3.tex", "pdf": "lab-3-lagrange.pdf", "title": "Lab 3: Lagrange multipliers", "kind": "notes", "assign": [("data-642", 3)]},
    {"src": f"{NOTES}/642_quiz_1_solution.tex", "pdf": "quiz-1-solutions.pdf", "title": "Quiz 1 solutions", "kind": "practice", "assign": [("data-642", 3)]},
    {"src": f"{Q642}/quiz1_sol.tex", "pdf": "quiz-1-solutions-alt.pdf", "title": "Module 1 quiz solutions", "kind": "practice", "assign": [("data-642", 3)]},
    {"src": f"{Q642}/Quiz1_Solution.tex", "pdf": "quiz-1-solution-set.pdf", "title": "Module 1 quiz solution set", "kind": "practice", "assign": [("data-642", 3)]},
    {"src": f"{Q642}/quiz2_sol.tex", "pdf": "quiz-2-solutions.pdf", "title": "Module 2 quiz solutions", "kind": "practice", "assign": [("data-642", 4)]},
    {"src": f"{Q642}/Quiz 4.tex", "pdf": "quiz-4.pdf", "title": "Quiz 4 (practice)", "kind": "practice", "assign": [("data-642", 12)]},
    {"src": f"{Q642}/Quiz 5.tex", "pdf": "quiz-5.pdf", "title": "Quiz 5 (clustering, practice)", "kind": "practice", "assign": [("data-642", 10)]},
    {"src": f"{Q642}/Quiz 5, solutions.tex", "pdf": "quiz-5-solutions.pdf", "title": "Quiz 5 solutions", "kind": "practice", "assign": [("data-642", 10)]},
    {"src": f"{Q642}/midterm_sample.tex", "pdf": "midterm-sample.pdf", "title": "Midterm sample", "kind": "practice", "assign": [("data-642", 9)]},
    {"src": f"{Q642}/final_sample.tex", "pdf": "final-sample.pdf", "title": "Final exam sample", "kind": "practice", "assign": [("data-642", 15)]},
    {"src": f"{Q642}/Fina_Exam_Sample.tex", "pdf": "final-sample-modules.pdf", "title": "Final exam sample (by module)", "kind": "practice", "assign": [("data-642", 15)]},
]


def extras_for(course: str, week: int, kind: str) -> list[tuple[str, str]]:
    out = []
    for item in ITEMS:
        if item["kind"] != kind:
            continue
        if (course, week) in item["assign"]:
            out.append((item["title"], f"extra/{item['pdf']}"))
    return out
