# ContractPilot

A focused API migration assistant for the Nebius x NVIDIA Global AI Hackathon. Team: Asiya Ali and Taaha Younas. Taaha’s Devpost invitation has been sent and is awaiting acceptance.

ContractPilot compares two OpenAPI 3 JSON documents, identifies a bounded set of breaking changes, and can ask an NVIDIA model on Nebius Token Factory for a migration plan. Each accepted migration step must reference a detected change. It never executes generated code, tests, or instructions from input specifications.

## Run

Python 3.11+; standard library only:

```sh
python3 -m contractpilot examples/before.json examples/after.json
python3 -m unittest discover -s tests -v
```

The fictional parcel API example has three detected changes: a removed operation, a newly required query parameter, and a removed success code. Analysis-only mode makes no network calls and does not pretend to be an AI response.

For a real model run, configure your own Nebius Token Factory account and an available NVIDIA model. This consumes your account's inference credits. Never commit keys:

```sh
export NEBIUS_API_KEY='your-private-key'
export NEBIUS_MODEL='exact-nvidia/model-id-from-your-catalog'
python3 -m contractpilot examples/before.json examples/after.json --live
```

The endpoint is fixed to the official HTTPS Nebius Token Factory API. See https://tokenfactory.nebius.com/ for the account and model catalog. A provider failure, truncated answer, malformed JSON or invalid citation fails visibly rather than substituting an invented answer.

## Scope and limitations

Supported: operation removal, newly required inline parameters/request bodies, and removed success codes. Not supported: reference resolution, full JSON Schema compatibility, security changes, SDK analysis, or runtime behavior. “No supported changes” is not proof of backward compatibility. Reference checks do not prove the model's migration advice is correct; developers must review it. Use non-sensitive API specs when sending changes to an external model provider. Inputs are bounded to 500 KB per file.

## Browser app

Run `python3 server.py`, then open `http://127.0.0.1:8787`. Load the example or import two OpenAPI JSON files, inspect detected changes and export the review. With the environment variables above set, Draft with Nemotron makes a real Nebius request. Keys remain server-side. Without credentials, the browser clearly shows analysis-only mode. The server is loopback-only and is not a production deployment.

The static preview performs browser-local comparison only; it does not have live model access.

## Verification and submission status

CLI and local browser app with regression tests. Real Nebius/NVIDIA inference has **not** yet been verified. Source is published at https://github.com/aggravating08/contractpilot. A private analysis-only preview is deployed at https://contractpilot-asiya-taaha.asiyaaaaa8.chatgpt.site. No live AI demonstration video or final Devpost entry is claimed. This is preparation, not a completed eligible submission.

Proposed track: Coding and Agentic Engineering. Deadline: October 30, 2026, 22:00 PKT. Final entry needs actual Nebius/NVIDIA execution evidence, accessible test build/demo, public licensed repository, English description, tool feedback, and a public YouTube video under three minutes.
