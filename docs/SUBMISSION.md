# ContractPilot — submission preparation

Team: Asiya Ali and Taaha Younas. Both members are now listed on the Devpost team.
Recommended track: Best Apps and Agents.
Deadline: October 30, 2026 at 22:00 Pakistan time.

## Inspiration

API release notes often explain the new feature while leaving downstream developers to discover what their clients can no longer do. ContractPilot gives a small team a focused pre-release review and a migration checklist anchored to the contract changes.

## What it does

Compare two OpenAPI 3 JSON versions in the browser or CLI. Inspect each supported breaking change, its JSON pointer and stable change ID. Export a portable JSON review. The local companion can send only detected change descriptions to an NVIDIA model on Nebius Token Factory for migration suggestions. Each accepted step must cite one or more detected change IDs. No generated code is executed.

## How we built it

Python standard library for the CLI and loopback companion; HTML, CSS and JavaScript for the browser; SHA-256 identifiers shared across both engines. Real provider access is environment-configured and server-side. The static preview performs local analysis only.

## Accomplishments and learning

The Python and JavaScript engines agree on the sample and on Unicode paths. Regression checks distinguish optional additions from newly required inputs. Model validation fails closed on invalid references instead of fabricating an offline AI result. Our central distinction is between deterministic change evidence and model-generated advice requiring review.

## Current limits

This is a bounded checker, not a complete OpenAPI compatibility implementation. It does not resolve references, compare schemas, evaluate authentication, inspect client SDKs or run tests against APIs. No findings does not prove compatibility. Advice is not automatically applied. Real Nebius/NVIDIA execution is pending; do not submit or describe the integration as verified until a genuine run has been saved.

## Remaining before final entry

- [x] Taaha accepted the team invitation.
- Complete Nebius sign-in, verify credits and select an available NVIDIA model.
- Run the live path, inspect semantic correctness and save sanitized evidence.
- Record a working demonstration under three minutes and publish it on YouTube.
- Update tools feedback from actual use, add video/demonstration/source links to Devpost.
- Review final entry terms and submission confirmation.
