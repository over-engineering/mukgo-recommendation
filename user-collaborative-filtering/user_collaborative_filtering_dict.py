from math import sqrt, isnan
import numpy as np

restaurant_list = ["아비꼬", "롱타임노씨", "피맥하우스", "오신 매운갈비찜", "오빠닭", "바나나 피자"]

test_data = {
    "Chang": {
        "0": 2.5,
        "1": 3.5,
        "2": 3.0,
        "3": 3.5,
        "4": 2.5,
        "5": 3.0
    },
    "Chan": {
        "0": 3.0,
        "1": 3.5,
        "2": 1.5,
        "3": 5.0,
        "4": 3.5,
        "5": 3.0
    },
    "jmpark": {
        "0": 2.5,
        "1": 3.5,
        "3": 3.5,
        "5": 4.0
    },
    "Ruby": {
        "1": 3.5,
        "2": 3.0,
        "3": 4,
        "4": 2.5,
        "5": 4.5
    },
    "suji kang": {
        "0": 1.0,
        "2": 3.0,
        "3": 2.0,
        "5": 1.5   
    },
    "suji kang": {
        "0": 1.0,
        "2": 3.0,
        "3": 2.0,
        "5": 1.5
    },
    "Cold New User": {
    },
    "Hot New User": {
        "0": 1.0,
        "1": 3.5,
        "2": 2.5,
        "3": 3.5,
        "4": 3.5,
        "5": 4.5
    },
    "Chang's soul mate": {
        "0": 2.5,
        "1": 3.5,
        "2": 3.0,
        "3": 3.5,
        "4": 2.5,
        "5": 3.0
    },
}

def euclidean_distance(pref1, pref2):
    simularity_items = dict()

    for item in pref1:
        if item in pref2:
            simularity_items[item] =True
    
    number_of_ratings = len(simularity_items)
    
    if number_of_ratings == 0:
        return 0
               
    return 1 / (1 + sqrt(sum([(pref1[item] - pref2[item]) ** 2 for item in pref1 if item in pref2])))

def pearson_correlation(pref1, pref2):
    simularity_items = dict()

    for item in pref1:
        if item in pref2:
            simularity_items[item] =True
    
    number_of_ratings = len(simularity_items)

    if number_of_ratings == 0:
        return 0

    pref_sum1 = sum([pref1[item] for item in simularity_items])
    pref_sum2 = sum([pref2[item] for item in simularity_items])
    
    sqrt_pref_sum1 = sum([(pref1[item])**2 for item in simularity_items])
    sqrt_pref_sum2= sum([(pref2[item])**2 for item in simularity_items])
    
    product_sum = sum([pref1[item] * pref2[item] for item in simularity_items])
    
    numerator_value = product_sum - (pref_sum1 * pref_sum2 / number_of_ratings)
    denominator_value = sqrt((sqrt_pref_sum1 - pow(pref_sum1, 2) / number_of_ratings)\
        * (sqrt_pref_sum2 - pow(pref_sum2, 2) / number_of_ratings))
    
    if denominator_value == 0 or isnan(denominator_value):
        return 0

    return numerator_value / denominator_value

def user_similarity(data, user, method = pearson_correlation, maximum = 10):
    scores = [(method(data[user], data[other]), other) for other in data if other != user]

    scores.sort()
    scores.reverse()

    print("@@@@@@@@@@@@@@@@@@@@@@ Similarity @@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    for score, identifier in scores:
        print("%s is Similar with %s about : %f" % (user, identifier, score))

    return scores[0:min(maximum, len(scores))]


def recommendation(data, user, method = pearson_correlation, maximum = 10):

    total_scores = dict()
    similarity_sum = dict()

    for other in data:
        if other == user:
            continue

        similarity = method(data[user], data[other])

        if similarity < 0:
            continue

        for item, score in data[other].items():
            # User not evaluated
            if item not in data[user] or data[user][item] == 0:
                total_scores.setdefault(item, 0)
                total_scores[item] += similarity * data[other][item]
                similarity_sum.setdefault(item, 0)
                similarity_sum[item] += similarity

    rankings_not_visited = [ (total / similarity_sum[item], item) for item, total in total_scores.items() ]
    rankings_not_visited.sort()
    rankings_not_visited.reverse()
    
    print("@@@@@@@@@@@@@@@@@@@@@@ Recommendation Rankings @@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    for index, ranking in enumerate(rankings_not_visited):
        score, restaurant_index = ranking
        print("Ranking %d : %s, Score : %f" % (index + 1, restaurant_list[int(restaurant_index)], score))
    return rankings_not_visited


user_similarity(test_data, "suji kang")
recommendation(test_data, "suji kang")
print('A')

