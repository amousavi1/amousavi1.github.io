"""Lecture, lab, and hub metadata for DATA 442/642.

Week map follows the Drive course (Lectures/Module*/Week*).
"""

NOTES = [
    {"slug": "ml-basics", "week": 1, "title": "1.1 Machine Learning Basics", "lead": "Supervised, unsupervised, batch versus online, and the usual failure modes."},
    {"slug": "vector-calc-motivation", "week": 1, "title": "1.2 Why Vector Calculus", "lead": "Training is an optimization problem. Linear regression is the first example."},
    {"slug": "derivatives", "week": 1, "title": "1.3 Derivatives for Optimization", "lead": "Gradients point uphill. We walk the other way."},
    {"slug": "vector-calculus", "week": 1, "title": "1.4 Basic Vector Calculus", "lead": "Gradients, Jacobians, and Hessians in the notation this course uses."},
    {"slug": "lab-1-mnist-sgd", "week": 1, "title": "Lab 1: A 5-Detector on MNIST", "lead": "Binary SGD, cross-validation, and the precision–recall trade-off."},
    {"slug": "intro-optimization", "week": 2, "title": "2.1 Introduction to Optimization", "lead": "Cost functions, local versus global minima, convexity, and first- and second-order tests."},
    {"slug": "unconstrained-methods", "week": 2, "title": "2.2 Unconstrained Methods", "lead": "Line search, steepest descent, momentum, and SGD."},
    {"slug": "second-order", "week": 2, "title": "2.3 Second-Order Methods", "lead": "Newton, Levenberg–Marquardt, and BFGS."},
    {"slug": "lab-2-gradient-descent", "week": 2, "title": "Lab 2: Gradient Descent and Newton", "lead": "Step sizes, SGD versus batch, and a badly conditioned quadratic."},
    {"slug": "constrained-optimization", "week": 3, "title": "3.1 Constrained Optimization", "lead": "Lagrange multipliers, the primal, and the dual."},
    {"slug": "linear-programming", "week": 3, "title": "3.2 Linear Programming", "lead": "A linear cost, linear inequalities, and a dual that is also an LP."},
    {"slug": "quadratic-programming", "week": 3, "title": "3.3 Quadratic Programming", "lead": "A convex quadratic with linear constraints. SVM is the running example."},
    {"slug": "lab-3-lagrange", "week": 3, "title": "Lab 3: A Lagrange Multiplier by Hand", "lead": "One equality constraint, stationary points, and a contour picture."},
    {"slug": "midterm", "week": 9, "title": "Midterm Review", "lead": "Modules 1–4: optimization, sparsity, kernels and SVMs, then PCA through tensors."},
]

BY_SLUG = {n["slug"]: n for n in NOTES}

WEEKS = {
    1: {
        "label": "Module 1 — Machine learning and vector calculus",
        "lectures": ["ml-basics", "vector-calc-motivation", "derivatives", "vector-calculus"],
        "labs": [("lab-1-mnist-sgd", False)],
        "discussion": [
            "Name one supervised and one unsupervised method this course will treat later, and what label each one does or does not see.",
            "Why is the normal equation a calculus problem, not a programming problem?",
        ],
    },
    2: {
        "label": "Module 1 — Unconstrained optimization",
        "lectures": ["intro-optimization", "unconstrained-methods", "second-order"],
        "labs": [("lab-2-gradient-descent", False)],
        "discussion": [
            "When does a local minimum fail to be global?",
            "What does a large condition number do to steepest descent?",
        ],
    },
    3: {
        "label": "Module 1 — Constrained optimization, LP, QP",
        "lectures": ["constrained-optimization", "linear-programming", "quadratic-programming"],
        "labs": [("lab-3-lagrange", False)],
        "homework": [("Homework 1", "hwk1.pdf")],
        "discussion": [
            "What does a Lagrange multiplier charge you for?",
            "Why is a soft-margin SVM a quadratic program?",
        ],
    },
    4: {
        "label": "Module 2 — Sparsity-aware learning",
        "homework": [("Homework 2", "hwk2.pdf")],
        "discussion": [
            "Why can ridge shrink coefficients but not set them to zero?",
            "What does soft thresholding do to a coordinate of the LASSO?",
        ],
    },
    5: {
        "label": "Module 3 — Hilbert spaces, kernels, and SVMs",
        "discussion": [
            "What does the kernel trick avoid computing?",
            "Where do the support vectors appear in the SVM dual?",
        ],
    },
    6: {
        "label": "Module 4 — PCA",
        "homework": [("Homework 4", "hwk4.pdf")],
        "discussion": [
            "PCA maximizes variance. What matrix’s eigenvectors are you computing?",
            "When would you prefer kernel PCA to ordinary PCA?",
        ],
    },
    7: {
        "label": "Module 4 — Multimodal learning, CCA, IVA",
        "discussion": [
            "CCA needs two views of the same objects. Name a pair.",
            "What extra assumption does IVA add on top of ICA?",
        ],
    },
    8: {
        "label": "Module 4 — Tensors",
        "discussion": [
            "A matrix is a 2-way array. What is a tensor adding?",
            "Why might a tensor factorization beat flattening the same data into a matrix?",
        ],
    },
    9: {
        "label": "Midterm (Modules 1–4)",
        "lectures": ["midterm"],
        "discussion": [
            "Which derivation still feels thin: KKT, kernels, or PCA via SVD?",
            "Write one exam-style question you would not want to be surprised by.",
        ],
    },
    10: {
        "label": "Module 5 — Clustering",
        "homework": [("Homework 5", "hwk5.pdf")],
        "discussion": [
            "k-means assumes spherical clusters. Give a data set where that is wrong.",
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
        "label": "Module 6 — Perceptrons and multilayer nets",
        "homework": [("Homework 6", "hwk6.pdf")],
        "discussion": [
            "What does a hidden layer buy you that a perceptron cannot do?",
            "Write the forward pass of a two-layer net in one line of matrix products.",
        ],
    },
    13: {
        "label": "Module 6 — Training neural nets",
        "discussion": [
            "Name one reason a ReLU helps with vanishing gradients.",
            "Dropout versus weight decay: which one is stochastic at train time?",
        ],
    },
    14: {
        "label": "Module 6 — Autoencoders and VAEs",
        "discussion": [
            "A linear autoencoder with squared loss is close to which classical method?",
            "What problem does the reparameterization trick solve?",
        ],
    },
    15: {
        "label": "Module 6 — GANs",
        "discussion": [
            "What two networks are playing the GAN game, and what does each want?",
            "Name one way to tell a GAN sample from a training point besides looking at it.",
        ],
    },
}
