# Berlin EV Charging Network

A Streamlit app for finding electric-vehicle charging stations in Berlin by postal code
and for reporting and resolving station malfunctions. Built for the course Advanced
Software Engineering (M.Sc. Data Science, Berliner Hochschule für Technik) to practise
Domain-Driven Design and test-driven development. It was set as a team assignment; I
designed and implemented the application and its tests.

**Live demo:** [berlin-ev-charging-platform.streamlit.app](https://berlin-ev-charging-platform-kdxxuctnz8adrhvikxqey7.streamlit.app/)
Operator dashboard login (demo only): `operator` / `berlin2025`

## What it does

- **Station search.** Look up the 1,989 Berlin stations in the Bundesnetzagentur's
  charging station register by postal code, on an interactive map.
- **Malfunction reporting.** A guided form creates a ticket and marks the station as defective.
- **Operator dashboard.** Shows open tickets and network counts; resolving a ticket
  restores the station's status.

## Limitations

This is a learning project, not a production system:

- Station data is a static CSV snapshot, and all state is held in memory. Reports are
  lost when the app restarts.
- Station status changes only through reports made in the app. There is no live feed
  from the charging stations.
- The operator login is a hard-coded demo credential, not real authentication.

## Architecture

The code is split into two bounded contexts that share only a station identifier:

```
contexts/
├── discovery/         station search
│   ├── domain/           OperationalStation, StationStatus, PostalCode, repository interface
│   ├── application/      SearchStationsUseCase
│   └── infrastructure/   CSV loader, in-memory repository
├── reporting/         malfunction reports
│   ├── domain/           MalfunctionReport, MalfunctionReportService, enums, exceptions
│   ├── application/      create and resolve use cases
│   └── infrastructure/   in-memory repository
└── shared_kernel/     StationId value object, dataset
presentation/app.py    Streamlit UI
tests/                 mirrors the structure above
```

Design choices worth knowing:

- **Domain logic has no framework dependencies.** Streamlit and pandas appear only in
  the presentation and infrastructure layers, so the domain can be tested in isolation.
- **Repositories are interfaces.** The in-memory implementations could be replaced by a
  database without touching domain or application code.
- **Value objects validate on creation.** A `PostalCode` that is not a Berlin code, or a
  report description outside 10 to 500 characters, cannot exist.

## Tests

75 tests, 92% line coverage (see `docs/coverage_report.txt`).

```bash
pytest tests/
pytest tests/ --cov=contexts
```

## Run it locally

Requires Python 3.10 or newer.

```bash
git clone https://github.com/kezia-fernandes/Berlin-EV-Charging-Platform.git
cd Berlin-EV-Charging-Platform
pip install -r requirements.txt
streamlit run presentation/app.py
```

## Data

Charging station register (Ladesäulenregister) published by the Bundesnetzagentur.
