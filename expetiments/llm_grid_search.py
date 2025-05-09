import pandas as pd
import requests
import itertools
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

smoothie = SmoothingFunction().method1

temperatures = [0.1, 0.5, 1.0]
top_ps = [0.7, 0.8, 0.9]

data = pd.read_csv("input.csv")


def grid_search():
    results = []

    for temp, top_p in itertools.product(temperatures, top_ps):
        total_rag_bleu1 = 0
        total_rag_bleu2 = 0
        rag_count = 0

        function_correct = 0
        function_total = 0

        for _, row in data.iterrows():
            category = row['Category']
            question = row['Question']
            target = row['Target']

            body = {
                "temperature": temp,
                "top_p": top_p,
                "text": question
            }

            if category == "rag":
                endpoint = "http://127.0.0.1:8888/api/rag"
            elif category == "Function Calling":
                endpoint = "http://127.0.0.1:8888/api/test"
            else:
                continue

            try:
                response = requests.post(endpoint, json=body)
                response.raise_for_status()
                answer = response.text.strip()

                if category == "Function Calling":
                    function_total += 1
                    if answer == target:
                        function_correct += 1

                elif category == "rag":
                    rag_count += 1
                    ref = [target.split()]
                    hyp = answer.split()
                    total_rag_bleu1 += sentence_bleu(ref, hyp, weights=(1, 0, 0, 0), smoothing_function=smoothie)
                    total_rag_bleu2 += sentence_bleu(ref, hyp, weights=(0.5, 0.5, 0, 0), smoothing_function=smoothie)

            except Exception as e:
                print(f"Error during request: {e}")

        result = {
            "temperature": temp,
            "top_p": top_p,
            "function_accuracy": function_correct / function_total if function_total else None,
            "rag_bleu1": total_rag_bleu1 / rag_count if rag_count else None,
            "rag_bleu2": total_rag_bleu2 / rag_count if rag_count else None
        }
        results.append(result)

    results_df = pd.DataFrame(results)
    results_df.to_csv("llm_grid_search_results.csv", index=False)


if __name__ == '__main__':
    grid_search()
