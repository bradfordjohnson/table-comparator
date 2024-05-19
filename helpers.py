from fuzzywuzzy import fuzz
from itertools import combinations

def get_similar_fields(datasets, max_items=None):
    output = {}
    for dataset1, dataset2 in combinations(datasets.items(), 2):
        for item1 in dataset1[1]:
            matches = []
            for item2 in dataset2[1]:
                score = fuzz.ratio(item1, item2)
                if score > 0:
                    matches.append({item2: score})
            if matches:
                matches.sort(key=lambda x: list(x.values())[0], reverse=True)
                if max_items is not None:
                    matches = matches[:max_items]
                if dataset1[0] not in output:
                    output[dataset1[0]] = {}
                output[dataset1[0]][item1] = [{dataset2[0]: matches}]
    return output