# ContractPilot readiness audit

Checked October 27, 2026, Pakistan time. This is a working prototype, not a submission-ready hackathon entry.

## Official requirements and status

| Requirement | Observed status | Remaining work |
|---|---|---|
| NVIDIA model running through Nebius | Adapter exists, no genuine provider execution yet | Activate account; choose actual NVIDIA model; save a successful run |
| Appropriate track | Coding track was proposed but is weak for a tool that never writes/runs code | Recommend Best Apps and Agents for this product |
| Public licensed source and setup | Public GitHub repository, recognized MIT license, Python/browser setup | Keep documentation aligned with verified behavior |
| Judge-accessible demo or test build | Public source ZIP runs analysis; private preview blocks outside access; AI needs owner credentials | Supply a free instance or equivalent unrestricted test access through judging |
| Working demonstration | Local browser comparison verified; model feature not verified | Verify actual AI path and record it |
| Public YouTube video under three minutes | Missing; only recording script exists | Record the real final app and publish publicly |
| English description and tool feedback | Draft text exists locally; Devpost story and detailed answers blank | Fill from actual model use, including size choice, output quality, comparison, platform experience and AI tools |
| Team | Both Asiya and taahayounas are listed | Team representative must confirm required eligibility declarations |
| Final entry | Devpost DRAFT, 2/5 steps | Complete remaining fields and final confirmation |

Deadline: October 30 at 17:00 UTC / 22:00 PKT. Keep free judge access available through December 15 at 20:00 UTC. Neither Tavily nor an in-person event is mandatory for the general entry; city and Tavily awards have separate criteria. A pitch deck and PDF report are not listed as required deliverables for this event.

Sources: [rules](https://nebiusglobalaihackathon.devpost.com/rules), [FAQ](https://nebiusglobalaihackathon.devpost.com/details/faqs), [final checklist](https://nebiusglobalaihackathon.devpost.com/updates/46207-final-stretch-here-s-your-submission-checklist).

## Missed guidance corrected

The FAQ explicitly routes unsupported-country onboarding and missing promo credits to the Nebius team on Discord. It describes this as provisioning rather than a Devpost eligibility rule. It rejects changing billing region or substituting a different inference provider as a workaround. The email support request remains useful, but waiting for email alone was incomplete guidance.

## Code findings and repairs

- Malformed nested OpenAPI objects could raise AttributeError. Both engines now validate their supported input structures and reject invalid required flags before comparing.
- Empty or malformed provider envelopes could raise uncaught IndexError or AttributeError. They now fail as explicit validation errors.
- Oversized provider responses are now rejected before parsing.
- Provider contract tests check the actual endpoint/payload path with mocked network responses, and reject truncated/malformed results. These tests do not establish live service access or model quality.
- Browser/Python change identifiers match, including Unicode paths. Citation checks constrain references, not the semantic truth of migration advice.
- Twenty Python tests and twelve browser-engine checks pass after the repairs.

## Product limits affecting judging

This is a bounded OpenAPI checker plus an optional model planning adapter. It does not yet resolve references, compare schemas, inspect SDKs, apply patches or execute generated tests. No detected breaking change is not a compatibility guarantee. No customer interviews, measured impact, model benchmark or real inference success is claimed. The next useful product validation is a real before/after API from a developer and a reviewed migration plan.
