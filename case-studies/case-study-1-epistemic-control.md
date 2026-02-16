# Case Study #1

## Designing Epistemically-Aware AI Systems to Prevent Hallucination and Overconfidence

---

## 1. Problem Definition

Modern LLM-based systems tend to **over-generalize**. When presented with ambiguous or unverifiable questions, they often respond with **confident but fabricated answers**, which erodes user trust and introduces significant product risk.

This problem becomes especially pronounced in domains where:

- Ground truth is incomplete or unknowable
- Users expect authoritative responses
- Narrative plausibility conflicts with factual accuracy

In the context of historical simulation, these risks are unavoidable. Many user questions *sound factual* but are, in reality, speculative or unknowable.

**Core problem:**

How can an AI system respond intelligently and engagingly **without presenting speculation as fact**?

---

## 2. Why Naive LLM Systems Fail

In a naive architecture:

```
User Question → LLM → Answer

```

The model is implicitly rewarded for:

- Fluency
- Confidence
- Completeness

This leads to predictable failure modes:

- Hallucinated facts
- Fabricated emotional states
- False historical certainty
- Overconfident tone in unverifiable contexts

Prompt engineering alone is insufficient because the issue is not *how* the model responds, but **when it should be allowed to respond at all**.

This is a **systems design problem**, not a prompt problem.

---

## 3. Design Constraints

The system needed to satisfy the following constraints:

- Prevent speculative content from being presented as fact
- Preserve narrative immersion without lying
- Allow agents to defer or express uncertainty
- Maintain consistent behavior across interactions
- Remain model-agnostic and future-proof

Most importantly:

> The system must be allowed to say “I don’t know” in a structured, trustworthy way.
> 

---

## 4. Architectural Approach (Odyssey)

To address this, I designed Odyssey as an **AI orchestration platform**, rather than a single LLM pipeline.

### Key Architectural Principles

- Intent-driven routing
- Epistemic separation of knowledge types
- Constrained speculation
- Continuous evaluation and control

Rather than asking “Can the model answer this?”, the system asks:

> “What kind of intelligence is appropriate here?”
> 

---

## 5. Epistemic Control in Practice

### Example User Question

> “What was the crowd thinking when Michael Jackson stepped on stage?”
> This question:

- Sounds factual
- Has no verifiable ground truth
- Strongly tempts hallucination

### System Handling

**Intent Routing Engine**

- Classifies the query as *speculative inference*, not factual retrieval

**Truth & Knowledge Engine**

- Confirms absence of canonical data
- Flags response as non-authoritative

**Speculative / Reconstruction Logic**

- Generates a constrained interpretation
- Enforces explicit uncertainty language

**Evaluation & Control Layer**

- Verifies speculative labeling
- Prevents authoritative tone

### Resulting Behavior

The system responds with a **plausible but clearly inferred** interpretation, preserving immersion **without misrepresenting truth**.

---

## 6. Failure Case Comparison

### Without Epistemic Control

- Confident emotional claims
- Fabricated collective sentiment
- No indication of uncertainty

### With Odyssey’s Architecture

- Clear distinction between fact and inference
- Language that signals uncertainty
- Trust preserved even when answers are incomplete

This distinction dramatically improves user trust and long-term system credibility.

---

## 7. Evaluation Strategy

Because epistemic correctness is qualitative, evaluation focused on:

- Presence of uncertainty signaling
- Absence of fabricated specifics
- Consistency across repeated queries
- User trust perception
- Narrative coherence under constraint

Evaluation was treated as a **first-class system**, not post-hoc testing.

---

## 8. Tradeoffs and Limitations

### Tradeoffs

- Some responses are less “impressive”
- Reduced narrative flourish in uncertain contexts
- Additional system complexity

### Why This Is Acceptable

- Trust outweighs impressiveness
- Long-term product credibility improves
- Architecture scales across domains

---

## 9. Key Takeaways

- Hallucination is a **systems problem**, not a model problem
- Epistemic uncertainty must be explicitly designed for
- Constrained intelligence builds more trust than fluent intelligence
- Applied AI success depends on **behavioral governance**, not raw capability

---

## 10. Why This Matters for Applied AI Engineering

This project reinforced a core principle:

> Applied AI engineers are responsible not for what models can say, but for what systems should say.
> Designing for epistemic humility is essential for any AI system operating in real-world products.