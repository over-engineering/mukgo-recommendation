from math import sqrt, isnan
import numpy as np

restaurant_list = ["아비꼬", "롱타임노씨", "피맥하우스", "오신 매운갈비찜", "오빠닭", "바나나 피자"]

test_data = {
    "Chang": np.array([2.5, 3.5, 3.0, 3.5, 2.5, 3.0]),
    "Chan": np.array([3.0, 3.5, 1.5, 5.0, 3.5, 3.0]),
    "jmpark": np.array([2.5, 3.5, 0, 3.5, 0, 4.0]),
    "Ruby": np.array([0, 3.5, 3.0, 4.0, 2.5, 4.5]),
    "suji kang": np.array([1.0, 0, 3.0, 2.0, 0, 1.5]),
    "Cold New User": np.array([0, 0, 0, 0, 0, 0]),
    "Hot New User": np.array([1.0, 0, 2.5, 3.5, 3.5, 4.5]),
    "Chang's soul mate": np.array([2.5, 3.5, 3.0, 3.5, 2.5, 3.0]),
}

def euclidean_distance(pref1, pref2):
    diff = pref1 - pref2
    return 1 / (1 + sqrt(np.sum(np.power(diff, 2))))

def pearson_correlation(pref1, pref2):
    evaluated = np.nonzero(np.logical_and(pref1, pref2))[0]
    number_of_ratings = evaluated.size

    if number_of_ratings == 0:
        return 0

    pref_sum1 = np.sum(pref1[evaluated])
    pref_sum2 = np.sum(pref2[evaluated])

    sqrt_pref_sum1 = np.matmul(pref1[evaluated], np.transpose(pref1[evaluated]))
    sqrt_pref_sum2 = np.matmul(pref2[evaluated], np.transpose(pref2[evaluated]))

    product_sum = np.matmul(pref1[evaluated], np.transpose(pref2[evaluated]))
    
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

    total_scores = [0] * len(data[user])
    similarity_sum = [0] * len(data[user])

    for other in data:
        if other == user:
            continue

        similarity = method(data[user], data[other])

        if similarity < 0:
            continue

        for index, score in enumerate(data[other]):
            # User not evaluated
            if data[user][index] == 0 and score > 0:
                total_scores[index] += similarity * score
                similarity_sum[index] += similarity

    rankings_not_visited = [ (score / similarity_sum[index], index) for index, score in enumerate(total_scores) if similarity_sum[index] != 0]
    rankings_not_visited.sort()
    rankings_not_visited.reverse()
    
    print("@@@@@@@@@@@@@@@@@@@@@@ Recommendation Rankings @@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    for index, ranking in enumerate(rankings_not_visited):
        score, restaurant_index = ranking
        print("Ranking %d : %s, Score : %f" % (index + 1, restaurant_list[restaurant_index], score))
    return rankings_not_visited

# user_similarity(test_data, "Chang")
user_similarity(test_data, "suji kang")
recommendation(test_data, "suji kang")
print('A')

