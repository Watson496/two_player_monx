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


if __name__ == "__main__":
    main()
