These notes walk through the lecture slides. The original deck is unchanged; use **(slides)** on the course hub if you want that PDF.

Figures and notes follow Géron, *Hands-On Machine Learning*; Deisenroth, Faisal, and Ong, *Mathematics for Machine Learning*; and Theodoridis.

## 1. Central idea

A little labeled data, a lot of unlabeled. Use the unlabeled **geometry** to help the supervised model.

![Semi-supervised learning from clusters](files/data-642/graphics/10.4-clustering-semi-supervised/Semi_Supervised_Learning.png)

**Method.** Cluster unlabeled points by similarity. Spread the few labels across each cluster. Train on the bigger labeled set.

**Why.** Unlabeled rows are cheap. Labels are not. The extra labels can make the supervised model more stable.

Applications: text, images, anomalies, customers — anywhere labels are scarce.

---

## 2. \(k\)-means for the labels

1. **Cluster.** Run \(k\)-means on the unlabeled points. Each cluster has a centroid.
2. **Label the centroids.** Majority vote among labeled points in the cluster, or copy the labels of the labeled points nearest the centroid.
3. **Propagate.** Every point in the cluster gets the centroid’s label.
4. **Augment.** Original labeled rows plus the newly labeled cluster members.
5. **Train.** Fit a supervised model (classification or regression) on the augmented set.
6. **Check.** Score on a held-out validation or test set. The question is whether the propagated labels helped on unseen data.

---

## Practice

1. After you label the centroids, who else gets a label, and from where?

2. Majority vote versus nearest labeled point: what is the difference when you tag a centroid?

3. Why does this pipeline help when labels are expensive?
