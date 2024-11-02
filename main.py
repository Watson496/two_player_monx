from fractions import Fraction
from score import Score
import json
import csv


def generate_unique_pairs(N: int) -> list[list[int]]:
    return [[i, N - i] for i in range(1, (N // 2) + 1)]


def generate_all_pairs(N: int) -> list[list[int]]:
    return [[i, N - i] for i in range(1, N)]


def generate_score_patterns(max_m: int, max_n: int) -> list[Score]:
    patterns = [
        list(
            {
                Score(m_1, n_1, m_2, n_2)
                for sum1, sum2 in generate_unique_pairs(N)
                for m_1, n_1 in generate_all_pairs(sum1)
                for m_2, n_2 in generate_all_pairs(sum2)
                if m_1 <= max_m and n_1 <= max_n and m_2 <= max_m and n_2 <= max_n
            }
        )
        for N in range(4, 2 * (max_m + max_n) + 1)
    ]
    patterns_sorted = [
        sorted(
            N_patterns, key=(lambda score: (score.m_1, score.n_1, score.m_2, score.n_2))
        )
        for N_patterns in patterns
    ]
    return patterns_sorted


def main():
    """
    7○3×の試合に現れる各試合状況におけるhat_p, W_1, W_2の計算
    """
    patterns = generate_score_patterns(7, 3)
    res = [score.summary() for pattern in patterns for score in pattern]
    print(json.dumps(res, indent=2))

    with open("res.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=["S", "m_1", "n_1", "m_2", "n_2", "hat_p", "W_1", "W_2"]
        )
        writer.writeheader()
        for row in res:
            writer.writerow(row)

def main2():
    """
    50○50×までの各試合状況において、hat_pが予想を満たすことを検証
    """
    patterns = generate_score_patterns(50, 50)
    res = [score.summary() for pattern in patterns for score in pattern]

    # 予想の検証
    for r in res:
        e = Fraction(
            r["m_1"] + r["m_2"] - 1,
            r["m_1"] + r["n_1"] + r["m_2"] + r["n_2"] - 2
        )
        if not r["hat_p"] == str(e):
            print(r)
            print(f'e = {e} != {r["hat_p"]} = hat_p')

    with open("res2.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=["S", "m_1", "n_1", "m_2", "n_2", "hat_p", "W_1", "W_2"]
        )
        writer.writeheader()
        for row in res:
            writer.writerow(row)    

if __name__ == "__main__":
    main()
    # main2()
