"""Lecture, lab, and hub metadata for DATA 442/642.

Notes follow the Drive course: Lectures/Module*/Week* topic folders.
One folder = one note PDF, built from that folder's Jupyter notebook.
"""

NOTES = [
    {"slug": "ml-basics", "week": 1, "title": "1.1 Machine Learning Basics", "lead": "Supervised, unsupervised, batch versus online, and the usual failure modes.", "slide": "1.1-ml-basics"},
    {"slug": "vector-calc-motivation", "week": 1, "title": "1.2 Why Vector Calculus", "lead": "Training is an optimization problem. Linear regression is the first example.", "slide": "1.2-vector-calc-motivation"},
    {"slug": "derivatives", "week": 1, "title": "1.3 Derivatives for Optimization", "lead": "Gradients point uphill. We walk the other way.", "slide": "1.3-derivatives"},
    {"slug": "vector-calculus", "week": 1, "title": "1.4 Basic Vector Calculus", "lead": "Gradients, Jacobians, and Hessians in the notation this course uses.", "slide": "1.4-vector-calculus"},
    {"slug": "lab-1-mnist-sgd", "week": 1, "title": "Lab 1: A 5-Detector on MNIST", "lead": "Binary SGD, cross-validation, and the precision–recall trade-off."},
    {"slug": "intro-optimization", "week": 2, "title": "2.1 Introduction to Optimization", "lead": "Cost functions, local versus global minima, convexity, and first- and second-order tests.", "slide": "2.1-intro-optimization"},
    {"slug": "unconstrained-methods", "week": 2, "title": "2.2 Unconstrained Methods", "lead": "Line search, steepest descent, momentum, and SGD.", "slide": "2.2-unconstrained-methods"},
    {"slug": "second-order", "week": 2, "title": "2.3 Second-Order Methods", "lead": "Newton, Levenberg–Marquardt, and BFGS.", "slide": "2.3-second-order"},
    {"slug": "lab-2-gradient-descent", "week": 2, "title": "Lab 2: Gradient Descent and Newton", "lead": "Step sizes, SGD versus batch, and a badly conditioned quadratic."},
    {"slug": "constrained-optimization", "week": 3, "title": "3.1 Constrained Optimization", "lead": "Lagrange multipliers, the primal, and the dual.", "slide": "3.1-constrained-optimization"},
    {"slug": "linear-programming", "week": 3, "title": "3.2 Linear Programming", "lead": "A linear cost, linear inequalities, and a dual that is also an LP.", "slide": "3.2-linear-programming"},
    {"slug": "quadratic-programming", "week": 3, "title": "3.3 Quadratic Programming", "lead": "A convex quadratic with linear constraints. SVM is the running example.", "slide": "3.3-quadratic-programming"},
    {"slug": "lab-3-lagrange", "week": 3, "title": "Lab 3: A Lagrange Multiplier by Hand", "lead": "One equality constraint, stationary points, and a contour picture."},
    {"slug": "sparsity-motivation", "week": 4, "title": "4.1 Motivation for Sparsity-Aware Learning", "lead": "Why we want models that can set coefficients to zero.", "slide": "4.1-sparsity-motivation"},
    {"slug": "ridge-regression", "week": 4, "title": "4.2 Ridge Regression", "lead": "Shrink coefficients with an L2 penalty.", "slide": "4.2-ridge-regression"},
    {"slug": "lasso", "week": 4, "title": "4.3 LASSO", "lead": "An L1 penalty that can zero out coordinates.", "slide": "4.3-lasso"},
    {"slug": "sparsity-practical", "week": 4, "title": "4.4 Practical Considerations", "lead": "Tuning, scaling, and what to watch for in sparse models.", "slide": "4.4-sparsity-practical"},
    {"slug": "hilbert-spaces", "week": 5, "title": "5.1 Hilbert Spaces", "lead": "Inner-product spaces as the setting for kernels.", "slide": "5.1-hilbert-spaces"},
    {"slug": "kernel-ridge", "week": 5, "title": "5.2 Kernel Ridge Regression", "lead": "Ridge regression in a feature space, without building the features.", "slide": "5.2-kernel-ridge"},
    {"slug": "svms", "week": 5, "title": "5.3 Support Vector Machines", "lead": "Margins, the dual, and the kernel trick.", "slide": "5.3-svms"},
    {"slug": "intro-pca", "week": 6, "title": "6.1 Introduction to PCA", "lead": "Directions of largest variance, and the covariance eigenproblem.", "slide": "6.1-intro-pca"},
    {"slug": "kernel-pca", "week": 6, "title": "6.2 Kernel PCA", "lead": "PCA in a kernel-induced feature space.", "slide": "6.2-kernel-pca"},
    {"slug": "pca-special", "week": 6, "title": "6.3 Special Considerations for PCA", "lead": "Centering, scaling, and how many components to keep.", "slide": "6.3-pca-special"},
    {"slug": "multimodal-learning", "week": 7, "title": "7.1 Multimodal Learning", "lead": "Two or more views of the same objects.", "slide": "7.1-multimodal-learning"},
    {"slug": "cca", "week": 7, "title": "7.2 Canonical Correlation Analysis", "lead": "Find paired directions that co-vary across two views.", "slide": "7.2-cca"},
    {"slug": "iva", "week": 7, "title": "7.3 Independent Vector Analysis", "lead": "Independent components that stay aligned across datasets.", "slide": "7.3-iva"},
    {"slug": "intro-tensors", "week": 8, "title": "8.1 Introduction to Tensors", "lead": "Multi-way arrays and why flattening loses structure.", "slide": "8.1-intro-tensors"},
    {"slug": "tensor-decomposition", "week": 8, "title": "8.2 Tensor Decomposition Algorithms", "lead": "CP, Tucker, and how the factors are computed.", "slide": "8.2-tensor-decomposition"},
    {"slug": "tensors-ml", "week": 8, "title": "8.3 Tensors and Machine Learning", "lead": "Where tensor factorizations show up in models.", "slide": "8.3-tensors-ml"},
    {"slug": "midterm", "week": 9, "title": "Midterm Review", "lead": "Modules 1–4: optimization, sparsity, kernels and SVMs, then PCA through tensors."},
    {"slug": "clustering-kmeans", "week": 10, "title": "10.1 Clustering and K-Means", "lead": "Partition points into spherical clusters.", "slide": "10.1-clustering-kmeans"},
    {"slug": "clustering-segmentation", "week": 10, "title": "10.2 Clustering for Image Segmentation", "lead": "Treat pixels as points and cluster them.", "slide": "10.2-clustering-segmentation"},
    {"slug": "clustering-other", "week": 10, "title": "10.3 Other Clustering Algorithms", "lead": "When k-means is the wrong shape.", "slide": "10.3-clustering-other"},
    {"slug": "clustering-semi-supervised", "week": 10, "title": "10.4 Clustering and Semi-Supervised Learning", "lead": "Use unlabeled structure together with a few labels.", "slide": "10.4-clustering-semi-supervised"},
    {"slug": "gmms", "week": 11, "title": "11.1 Gaussian Mixture Models", "lead": "Soft clusters as a mixture of Gaussians.", "slide": "11.1-gmms"},
    {"slug": "gmms-anomaly", "week": 11, "title": "11.2 GMMs for Anomaly Detection", "lead": "Low density under the mixture as an anomaly score.", "slide": "11.2-gmms-anomaly"},
    {"slug": "gmms-practical", "week": 11, "title": "11.3 Practical Considerations", "lead": "Covariance types, initialization, and how many components.", "slide": "11.3-gmms-practical"},
    {"slug": "neural-networks", "week": 12, "title": "12.1 Neural Networks and the Perceptron", "lead": "A linear threshold unit, and what it cannot do.", "slide": "12.1-neural-networks"},
    {"slug": "multilayer-nets", "week": 12, "title": "12.2 Multilayer Neural Networks", "lead": "Hidden layers and a composition of linear maps and nonlinearities.", "slide": "12.2-multilayer-nets"},
    {"slug": "training-nns", "week": 12, "title": "12.3 Training Neural Networks", "lead": "An intuitive look at the forward and backward pass.", "slide": "12.3-training-nns"},
    {"slug": "backprop-challenges", "week": 13, "title": "13.1 Back-Propagation Challenges", "lead": "Vanishing gradients and other training failure modes.", "slide": "13.1-backprop-challenges"},
    {"slug": "faster-optimizers", "week": 13, "title": "13.2 Faster Optimizers", "lead": "Momentum, adaptive rates, and related tricks.", "slide": "13.2-faster-optimizers"},
    {"slug": "hyperparameters", "week": 13, "title": "13.3 Hyperparameters", "lead": "What you tune, and how you choose it.", "slide": "13.3-hyperparameters"},
    {"slug": "regularization", "week": 13, "title": "13.4 Regularization", "lead": "Weight decay, dropout, and related controls on capacity.", "slide": "13.4-regularization"},
    {"slug": "autoencoders-intro", "week": 14, "title": "14.1 Autoencoders", "lead": "Encode, decode, and reconstruct.", "slide": "14.1-autoencoders-intro"},
    {"slug": "autoencoders-part-ii", "week": 14, "title": "14.2 Autoencoders, Part II", "lead": "Deeper autoencoders and what the latent code is for.", "slide": "14.2-autoencoders-part-ii"},
    {"slug": "vaes", "week": 14, "title": "14.3 Variational Autoencoders", "lead": "A probabilistic latent space and the reparameterization trick.", "slide": "14.3-vaes"},
    {"slug": "intro-gans", "week": 15, "title": "15.1 Introduction to GANs", "lead": "A generator and a discriminator playing a two-player game.", "slide": "15.1-intro-gans"},
    {"slug": "notes-gans", "week": 15, "title": "15.2 Notes on GANs", "lead": "Training issues and the usual variants.", "slide": "15.2-notes-gans"},
    {"slug": "evaluating-gans", "week": 15, "title": "15.3 Evaluating GANs", "lead": "How to tell a sample from a training point besides looking at it.", "slide": "15.3-evaluating-gans"},
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
        "lectures": ["sparsity-motivation", "ridge-regression", "lasso", "sparsity-practical"],
        "lab_files": [("Lab 4", "lab-4-assignment.pdf")],
        "homework": [("Homework 2", "hwk2.pdf")],
        "discussion": [
            "Why can ridge shrink coefficients but not set them to zero?",
            "What does soft thresholding do to a coordinate of the LASSO?",
        ],
    },
    5: {
        "label": "Module 3 — Hilbert spaces, kernels, and SVMs",
        "lectures": ["hilbert-spaces", "kernel-ridge", "svms"],
        "lab_files": [("Lab 5", "lab-5-assignment.pdf")],
        "discussion": [
            "What does the kernel trick avoid computing?",
            "Where do the support vectors appear in the SVM dual?",
        ],
    },
    6: {
        "label": "Module 4 — PCA",
        "lectures": ["intro-pca", "kernel-pca", "pca-special"],
        "lab_files": [("Lab 6", "lab-6-assignment.pdf")],
        "homework": [("Homework 4", "hwk4.pdf")],
        "discussion": [
            "PCA maximizes variance. What matrix’s eigenvectors are you computing?",
            "When would you prefer kernel PCA to ordinary PCA?",
        ],
    },
    7: {
        "label": "Module 4 — Multimodal learning, CCA, IVA",
        "lectures": ["multimodal-learning", "cca", "iva"],
        "discussion": [
            "CCA needs two views of the same objects. Name a pair.",
            "What extra assumption does IVA add on top of ICA?",
        ],
    },
    8: {
        "label": "Module 4 — Tensors",
        "lectures": ["intro-tensors", "tensor-decomposition", "tensors-ml"],
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
        "lectures": ["clustering-kmeans", "clustering-segmentation", "clustering-other", "clustering-semi-supervised"],
        "homework": [("Homework 5", "hwk5.pdf")],
        "discussion": [
            "k-means assumes spherical clusters. Give a data set where that is wrong.",
            "What do you do when k is not given?",
        ],
    },
    11: {
        "label": "Module 5 — GMMs and anomaly detection",
        "lectures": ["gmms", "gmms-anomaly", "gmms-practical"],
        "discussion": [
            "A GMM is a soft clustering. What is being mixed?",
            "How would you turn a GMM density into an anomaly score?",
        ],
    },
    12: {
        "label": "Module 6 — Perceptrons and multilayer nets",
        "lectures": ["neural-networks", "multilayer-nets", "training-nns"],
        "homework": [("Homework 6", "hwk6.pdf")],
        "discussion": [
            "What does a hidden layer buy you that a perceptron cannot do?",
            "Write the forward pass of a two-layer net in one line of matrix products.",
        ],
    },
    13: {
        "label": "Module 6 — Training neural nets",
        "lectures": ["backprop-challenges", "faster-optimizers", "hyperparameters", "regularization"],
        "discussion": [
            "Name one reason a ReLU helps with vanishing gradients.",
            "Dropout versus weight decay: which one is stochastic at train time?",
        ],
    },
    14: {
        "label": "Module 6 — Autoencoders and VAEs",
        "lectures": ["autoencoders-intro", "autoencoders-part-ii", "vaes"],
        "discussion": [
            "A linear autoencoder with squared loss is close to which classical method?",
            "What problem does the reparameterization trick solve?",
        ],
    },
    15: {
        "label": "Module 6 — GANs",
        "lectures": ["intro-gans", "notes-gans", "evaluating-gans"],
        "discussion": [
            "What two networks are playing the GAN game, and what does each want?",
            "Name one way to tell a GAN sample from a training point besides looking at it.",
        ],
    },
}
