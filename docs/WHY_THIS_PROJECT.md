# Why This Project

## Novelty
While automated API testing exists, current tools require manual test case authoring or only validate against the spec's static schema. They cannot infer intent or edge conditions. SpecTest uses LLM reasoning to generate test cases that uncover semantic mismatches—e.g., a required field that the spec marks as optional, but the server rejects, or an expected error code that is never returned.

## Avoid Repetition
- Not CodeSec: no security scanning or PR review.
- Not HookDoctor: no webhook signature debugging.
- Not Onboarder: no repository onboarding checklists.
- Not any previous niche (security, webhooks, onboarding).

## Fit for Harman
- Developer tool that can be showcased in a portfolio.
- Combines AI with practical engineering—appeals to ML/API roles.
- Can be extended to serve Scalecraft's clients needing API quality assurance.

## Difficulty & Learning
This is difficulty 6: requires OpenAPI parsing, LLM integration, async HTTP, and report generation. It builds on Python tooling knowledge from previous cycles and adds a new dimension (contract testing). The lessons will inform future agentic testing systems.