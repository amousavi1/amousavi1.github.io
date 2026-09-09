"""Weekly hub metadata for DATA 442/642."""

WEEKS = {
    1: {
        "label": "Module 1 — Linear algebra and loss",
        "discussion": [
            "What does a positive-definite Hessian tell you about a critical point?",
            "Name one regression loss that is more robust to outliers than squared error, and why.",
        ],
    },
    2: {
        "label": "Module 1 — Eigenpairs and optimization landscape",
        "discussion": [
            "Why do we care that a covariance matrix is PSD?",
            "When is a second-order method worth the extra linear algebra?",
        ],
    },
    3: {
        "label": "Module 1 — Gradient methods, optimality, duality",
        "discussion": [
            "Write the KKT stationarity condition for a problem you already know (least squares, SVM, …).",
            "What is a dual variable doing, in one sentence?",
        ],
    },
    4: {
        "label": "Module 2 — Constrained and sparsity-aware methods",
        "discussion": [
            "When would you pick ADMM over a projected gradient step?",
            "What constraint are you actually enforcing with an augmented Lagrangian penalty?",
        ],
    },
    5: {
        "label": "Module 3 — Kernels and RKHS",
        "discussion": [
            "What does the kernel trick avoid computing explicitly?",
            "Give a kernel that is not the linear or RBF kernel and say what similarity it encodes.",
        ],
    },
    6: {
        "label": "Module 4 — Perceptron and SVM",
        "discussion": [
            "Hard-margin SVM versus the perceptron: what extra object does the SVM find?",
            "Where does the kernel enter the SVM dual?",
        ],
    },
    7: {
        "label": "Module 4 — SVM variants",
        "discussion": [
            "What problem is one-class SVM solving that a standard SVM is not?",
            "Twin SVM fits two hyperplanes. What is each one close to?",
        ],
    },
    8: {
        "label": "Module 4 — Ensembles and heuristics",
        "discussion": [
            "Bagging versus boosting: which one reduces variance, and which one chases residual error?",
            "When is a hand-written heuristic safer than another learned layer?",
        ],
    },
    9: {
        "label": "Midterm (Modules 1–4)",
        "discussion": [
            "Which derivation still feels thin: KKT, kernels, or the SVM dual?",
            "Write one exam-style question you would not want to be surprised by.",
        ],
    },
    10: {
        "label": "Module 5 — Clustering",
        "discussion": [
            "k-means assumes spherical clusters. Give a data set where that is the wrong model.",
            "What do you do when k is not given?",
        ],
    },
    11: {
        "label": "Module 5 — GMMs and anomaly detection",
        "discussion": [
            "A GMM is a soft clustering. What is being mixed?",
            "How would you turn a GMM density into an anomaly score?",
        ],
    },
    12: {
        "label": "Module 6 — PCA and matrix factorization",
        "discussion": [
            "PCA versus a regularized matrix factorization for a recommender: what extra term appears?",
            "What does a negative eigenvalue tell you if someone hands you a “covariance” matrix?",
        ],
    },
    13: {
        "label": "Module 6 — ICA, CCA, tensors",
        "discussion": [
            "ICA looks for independence, PCA for variance. When do those disagree?",
            "CCA needs two views of the same objects. Name a pair of views.",
        ],
    },
    14: {
        "label": "Module 6 — Multimodal learning",
        "discussion": [
            "What is aligned in CLIP, and what loss pulls the alignment?",
            "When is early fusion the wrong way to combine image and text?",
        ],
    },
    15: {
        "label": "Module 6 — Neural nets and autoencoders",
        "discussion": [
            "What does back-prop actually compute, in one line?",
            "An autoencoder with a linear hidden layer and squared loss is close to which classical method?",
        ],
    },
}
