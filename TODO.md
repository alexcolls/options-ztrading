# TODO / Roadmap

High-level ideas for next iterations. PRs welcome.

- Data enrichment
  - Normalize and expose Greeks (if/when API provides)
  - IV rank/percentile, historical IV comparison
  - Spreadable pairs discovery (e.g., verticals)
- Strategy support
  - Covered calls, cash-secured puts, debit/credit spreads
  - Filters: delta bands, POP, min OI/volume, min credit
  - Export ready-to-trade tickets CSV
- Performance & reliability
  - Request budget manager (global rate limit coordination)
  - Cache + incremental updates; Parquet storage option
  - Robust retry with jitter and circuit breakers
- UX & tooling
  - Progress summaries by symbol and error report file
  - Config profiles for recurring jobs (YAML/JSON)
  - Dockerfile and devcontainer
- Quality
  - Unit/integration tests with fixtures and VCR-like cassettes
  - Pre-commit hooks (ruff, black)
  - CI for lint and tests on PRs
- Integrations (optional)
  - Broker adapters (paper-trading safe): IBKR/TWS or Tasty
  - Web UI dashboard (later, optional)
