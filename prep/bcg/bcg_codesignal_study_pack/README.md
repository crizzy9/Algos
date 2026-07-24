# BCG X General Coding Assessment study pack

This pack is tailored to the BCG/BCG X AI Engineer General Coding Assessment reports discussed in the accompanying research. It is not a verbatim copy of a live assessment.

## What your assessment looks like

- 70 minutes total.
- Four **independent** questions, all visible from the beginning.
- Each file exposes a `solution(...)` function, matching the usual CodeSignal style.
- The questions do **not** build on one another.

Suggested simulation: spend 10 minutes on Q1, 15 minutes on Q2, 20 minutes on Q3, and the remaining 25 minutes on Q4 and review.

## Mock 1: closest reconstructable 2026 BCG set

1. `mock_1/q1_key_changes.py` — case-insensitive adjacent key changes.
2. `mock_1/q2_lunar_phase.py` — cyclic lunar-phase lookup.
3. `mock_1/q3_bubble_board.py` — matrix simulation with diagonal pops and gravity.
4. `mock_1/q4_alternating_parity.py` — count alternating-parity subarrays.

Run its tests from this directory:

```bash
python3 -m unittest mock_1.test_mock
```

## Additional reconstructable reported questions

- `extras/cumulative_visits.py` — earliest prefix reaching a target.
- `extras/maximum_subarray.py` — maximum contiguous-subarray sum (Kadane-style problem).

Run their tests:

```bash
python3 -m unittest extras.test_extras
```

## Source fidelity

| Exercise | What was publicly disclosed |
|---|---|
| Key changes | The BCG report publicly exposed the core rule. |
| Lunar phase | The BCG report exposed the topic; the public prompt was incomplete, so this pack supplies explicit calendar inputs. |
| Bubble board | The BCG report exposed the matrix topic; mechanics are reconstructed from the matching public CodeSignal problem. |
| Alternating parity | The BCG report publicly exposed the core rule. |
| Cumulative visits | A BCG X internship report exposed most of the prompt. |
| Maximum subarray | A BCG X candidate disclosed that the question was Kadane's algorithm, but not its exact story text. |

The remaining three entries from the nine-item research list were only described as “string matching,” “a matrix implementation,” and “a hash-map optimization problem.” There is not enough public information to reproduce those exact questions honestly.

Reference implementations are under `answer_key/`. Avoid opening that directory until you finish a timed attempt.
