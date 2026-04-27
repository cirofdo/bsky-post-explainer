import json
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

from backend.app.agent import explain
from backend.app.llm import openai_client_auth

PASS_THRESHOLD = 0.5  # pass if ≥50% of concepts are covered


def llm_judge(client, explanation: str, expected_concepts: list[str]) -> dict:
    concepts_str = "\n".join(f"- {c}" for c in expected_concepts)
    response = client.chat.completions.create(
        model=os.environ["OPENAI_MODEL"],
        messages=[
            {
                "role": "system",
                "content": (
                    "You evaluate whether an explanation covers a list of expected concepts. "
                    "For each concept, decide if it is mentioned or clearly implied in the explanation. "
                    "Return a JSON object with:\n"
                    "  - 'concepts_covered': integer (how many concepts are covered)\n"
                    "  - 'concepts_total': integer (total concepts)\n"
                    "  - 'reason': string (one sentence summary)"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Expected concepts:\n{concepts_str}\n\n"
                    f"Explanation:\n{explanation}\n\n"
                    "How many of the expected concepts does the explanation cover?"
                ),
            },
        ],
        response_format={"type": "json_object"},
    )
    data = json.loads(response.choices[0].message.content)
    covered = data.get("concepts_covered", 0)
    total = data.get("concepts_total", len(expected_concepts))
    score = covered / total if total > 0 else 0
    passed = score >= PASS_THRESHOLD
    return {
        "passed": passed,
        "score": round(score, 2),
        "concepts_covered": covered,
        "concepts_total": total,
        "reason": data.get("reason", ""),
    }


def main():
    with open("eval/test_cases.json") as f:
        test_cases = json.load(f)

    llm = openai_client_auth()
    results = []

    print(
        f"Running {len(test_cases)} test cases (pass threshold: {int(PASS_THRESHOLD * 100)}%)...\n"
    )

    for test in test_cases:
        print(f"[{test['id']}] {test['topic']}")
        print(f"URL: {test['url']}")

        try:
            explanation = explain(test["url"])
            result = llm_judge(llm, explanation, test["expected_concepts"])
            status = "PASS" if result["passed"] else "FAIL"
            print(f"Output: \n{explanation}")
            print(
                f"\n{status} ({result['concepts_covered']}/{result['concepts_total']} concepts): {result['reason']}"
            )
        except Exception as e:
            result = {
                "passed": False,
                "score": 0,
                "concepts_covered": 0,
                "concepts_total": 0,
                "reason": str(e),
            }
            print(f"ERROR: {e}")

        results.append(
            {
                "id": test["id"],
                "topic": test["topic"],
                "url": test["url"],
                **result,
            }
        )
        print()

    passed_count = sum(1 for r in results if r["passed"])
    avg_score = sum(r["score"] for r in results) / len(results)
    print(
        f"Score: {passed_count}/{len(results)} passed | avg concept coverage: {avg_score:.0%}"
    )

    with open("eval/results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Results saved to eval/results.json")


if __name__ == "__main__":
    main()
