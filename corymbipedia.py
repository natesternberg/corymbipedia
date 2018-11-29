import sys
import numpy as np
from collections import defaultdict
from scipy.cluster.vq import kmeans2


def load_from_glovevec(vec_fname, max_recs=sys.maxsize):
    words = []
    with open(vec_fname, 'r', encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == max_recs:
                break
            elements = line.split(' ')
            word = elements[0]
            vector = [float(x) for x in elements[1:]]
            # normalize vector
            magnitude = np.linalg.norm(vector)
            vector = vector / magnitude
            words.append({'word': word, 'vector': vector})
    return words


def find_clusters(glove, cluster_count, max_iter=5):
    clusters = []
    centroids, labels = kmeans2(glove, cluster_count, max_iter, check_finite=False)
    label_groups = defaultdict(list)
    # group token indices by cluster membership
    for i, label in enumerate(labels):
        label_groups[label].append(i)
    for k, v in label_groups.items():
        # calculate average distance from centroid
        distances = np.linalg.norm(centroids[k] - glove[v], axis=1)
        # sort indices by distance
        sorted_indices = [i for i, _ in sorted(zip(v, distances), key=lambda pair: pair[1])]
        average_distance = sum(distances) / len(v)
        # skip clusters with a single token
        if len(v) > 1:
            clusters.append((sorted_indices, average_distance))
    return sorted(clusters, key=lambda x: x[1])


def main(argv):
    num_to_display = 20
    glove_vec_fname, cluster_count, max_recs = argv[1], int(argv[2]), int(argv[3])
    words = load_from_glovevec(glove_vec_fname, max_recs)
    vocab_size = len(words)
    feature_size = len(words[0]['vector'])
    words_to_indices = {w['word']: i for i, w in enumerate(words)}
    indices_to_words = {i: w['word'] for i, w in enumerate(words)}
    print("Building matrix...")
    vectors = np.zeros((vocab_size, feature_size))
    for w in words:
        index = words_to_indices[w['word']]
        vectors[index, :] = w['vector']
    print("Clustering...")
    clusters = find_clusters(vectors, cluster_count)
    for i, cluster in enumerate(clusters):
        tokens = [indices_to_words[j] for j in cluster[0][:num_to_display]]
        print("#{}, d={:.4f} {}".format(i, cluster[1], tokens))


if __name__ == '__main__':
    main(sys.argv)
