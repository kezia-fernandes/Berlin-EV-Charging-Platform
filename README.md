# ⚡ Berlin EV Charging Network

A production-ready, Domain-Driven Design (DDD) platform for discovering 1,989+ EV charging stations across Berlin and managing station malfunctions with real-time monitoring.


## 🚀 Live Demo

**🔗 Try it now:** [Berlin EV Charging Platform](https://berlin-ev-charging-platform-kdxxuctnz8adrhvikxqey7.streamlit.app/)

### 🔐 Demo Credentials (Operator Dashboard)
```
Username: operator
Password: berlin2025
```

---

## ✨ Features

### 🔍 **Station Discovery**
- 📍 Search **1,989+ Berlin charging stations** by postal code
- 🗺️ Interactive Folium maps with cluster visualization
- 🚦 Real-time status indicators:
  - 🟢 **Available** - Ready to charge
  - 🔴 **Defective** - Reported malfunction
  - 🟡 **In Use** - Currently occupied
- 📋 Detailed station information with address, coordinates, and mini-maps

### 🛠️ **Malfunction Reporting**
- 📢 Public reporting interface for station issues:
  - ⚡ Not Charging
  - 💳 Payment System Failure
  - 🔌 Cable/Connector Damage
  - 💥 Physical Damage
  - 🌐 Network Connectivity Issues
- 📝 Multi-step guided reporting workflow
- 🎫 Automatic ticket generation with unique IDs
- ⚙️ Instant station status updates

### 👨‍💼 **Operator Dashboard**
- 🔒 Authentication
- 📊 Network-wide statistics and KPIs:
  - Total stations count
  - Active malfunction reports
  - Defective stations tracking
- 🎯 Ticket management system:
  - View all open reports
  - Resolve issues with one click
  - Automatic station status restoration
- 📈 Real-time monitoring and operational insights

---

## 🏗️ Architecture

This project implements **Domain-Driven Design (DDD)** with a clean, maintainable architecture using **two bounded contexts**:

```
Berlin-EV-Charging-Platform/
│
├── contexts/
│   ├── discovery/                    # 🔍 Station Search Bounded Context
│   │   ├── domain/
│   │   │   ├── entities/            # OperationalStation (Aggregate Root)
│   │   │   ├── value_objects/       # StationStatus (Available/Defective/InUse)
│   │   │   └── repositories/        # IStationRepository (Interface)
│   │   ├── application/
│   │   │   └── use_cases/           # SearchStationsUseCase
│   │   └── infrastructure/
│   │       ├── data/                # LadesaeulenregisterLoader (CSV)
│   │       └── repositories/        # InMemoryStationRepository
│   │
│   ├── reporting/                    # 🛠️ Malfunction Reporting Bounded Context
│   │   ├── domain/
│   │   │   ├── entities/            # MalfunctionReport (Aggregate Root)
│   │   │   ├── enums/               # MalfunctionType, ReportStatus
│   │   │   ├── services/            # MalfunctionReportService (Domain Logic)
│   │   │   └── exceptions/          # StationNotFound, InvalidReport
│   │   ├── application/
│   │   │   └── use_cases/           # Report submission workflows
│   │   └── infrastructure/
│   │       └── repositories/        # InMemoryReportRepository
│   │
│   └── shared_kernel/                # 🔗 Shared Concepts
│       ├── common/                   # StationId (Value Object)
│       └── datasets/                 # Ladesaeulenregister.csv (1,989 stations)
│
├── tests/                            # ✅ Centralized Test Suite (75 tests, 92% coverage)
│   ├── conftest.py                  # Shared fixtures
│   ├── discovery/
│   │   ├── domain/                  # Entity & Value Object tests
│   │   ├── application/             # Use case tests
│   │   └── infrastructure/          # Repository & CSV loader tests
│   ├── reporting/
│   │   ├── domain/                  # Entity, Service & Exception tests
│   │   ├── application/             # Use case workflow tests
│   │   └── infrastructure/          # Repository tests
│   └── shared_kernel/               # Shared value object tests
│
├── presentation/
│   └── app.py                        # 🎨 Streamlit UI (Multi-page app)
│
├── pytest.ini                        # Test configuration
├── requirements.txt                  # 📦 Dependencies
└── README.md                         # 📖 This file
```

### 🎯 Key DDD Patterns

- **Bounded Contexts**: Discovery and Reporting are isolated, maintaining their own models
- **Aggregates**: OperationalStation and MalfunctionReport are aggregate roots
- **Value Objects**: StationId, PostalCode, StationStatus ensure immutability and validation
- **Repository Pattern**: Abstract data access through interfaces (IStationRepository, IReportRepository)
- **Domain Services**: MalfunctionReportService coordinates cross-aggregate operations
- **Use Cases**: Clear application layer orchestrating domain logic
- **Shared Kernel**: StationId is shared between contexts for integration

---

## 🧪 Testing

### Test Coverage: 92% 🎉

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=contexts --cov-report=html

# Run specific context tests
pytest tests/discovery/
pytest tests/reporting/
```

### Test Statistics
- **75 passing tests** across all layers
- **92% code coverage** (457 statements, 36 missed)
- **Domain layer**: 96-100% coverage
- **Application layer**: 71-96% coverage
- **Infrastructure layer**: 93-100% coverage

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Berlin-EV-Charging-Platform.git
   cd Berlin-EV-Charging-Platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run tests**
   ```bash
   pytest tests/
   ```

4. **Start the application**
   ```bash
   streamlit run presentation/app.py
   ```

5. **Access the app**
   - Open browser: `http://localhost:8501`
   - For operator dashboard, use credentials: `operator` / `berlin2025`

---

## 📦 Dependencies

### Core Framework
- **streamlit** (1.28.0): Web application framework
- **pandas** (2.1.1): Data manipulation and analysis

### Mapping & Visualization
- **folium** (0.14.0): Interactive maps
- **streamlit-folium** (0.15.0): Folium integration for Streamlit

### Testing
- **pytest** (7.4.2): Testing framework
- **pytest-cov** (4.1.0): Coverage reporting

---

## 💡 Usage Examples

### Searching for Stations
```python
from contexts.discovery.application.use_cases.search_stations_use_case import SearchStationsUseCase
from contexts.discovery.infrastructure.repositories.in_memory_station_repository import InMemoryStationRepository

# Initialize
repository = InMemoryStationRepository()
use_case = SearchStationsUseCase(repository)

# Search by postal code
stations = use_case.execute(postal_code="10115")
for station in stations:
    print(f"{station.name} - {station.address}")
```

### Reporting a Malfunction
```python
from contexts.reporting.application.use_cases.create_malfunction_report_use_case import CreateMalfunctionReportUseCase
from contexts.reporting.domain.enums.malfunction_type import MalfunctionType

# Create report
use_case = CreateMalfunctionReportUseCase(report_repository, station_repository)
report = use_case.execute(
    station_id="BERLIN-10115-0001",
    description="Charging cable damaged, unable to connect",
    malfunction_type=MalfunctionType.CABLE_CONNECTOR_DAMAGE
)
print(f"Report created: {report.report_id}")
```

---

## 📊 Data Source

This project uses the **German Ladesäulenregister** (Charging Station Registry):
- **Source**: Bundesnetzagentur (Federal Network Agency)
- **Berlin Stations**: 1,989 registered charging locations
- **Data Fields**: Location, postal code, operator, coordinates
- **Update Frequency**: Government database (periodic updates)

---

## 🎨 UI Features

### Station Discovery Page
- 🔍 Postal code search with validation (Berlin codes only: 10xxx-14xxx)
- 🗺️ Interactive cluster maps with station markers
- 📍 Individual station maps with detailed info
- 🚦 Real-time status indicators
- 📱 Responsive design for mobile devices

### Malfunction Reporting Page
- 📝 4-step guided reporting workflow:
  1. Station ID input with validation
  2. Malfunction type selection (6 categories)
  3. Detailed description (10-500 characters)
  4. Confirmation with unique ticket ID
- ✅ Input validation at each step
- 🎫 Automatic ticket generation
- 🔄 Instant status updates

### Operator Dashboard
- 🔐 Secure authentication
- 📊 Real-time KPI dashboard:
  - Total network stations
  - Active malfunction reports
  - Defective stations count
- 📋 Ticket management interface
- 🔧 One-click issue resolution
- 📈 Network health monitoring

---

## 🛠️ Technology Stack

- **Language**: Python 3.10+
- **Web Framework**: Streamlit
- **Architecture**: Domain-Driven Design (DDD)
- **Testing**: pytest, pytest-cov
- **Data Processing**: pandas
- **Mapping**: Folium, streamlit-folium
- **Deployment**: Streamlit Cloud

---

## 🧩 Domain-Driven Design Implementation

### Bounded Contexts
1. **Discovery Context**: Handles station search and availability
2. **Reporting Context**: Manages malfunction reports and tickets

### Aggregates
- **OperationalStation** (Discovery): Single aggregate, no child entities
- **MalfunctionReport** (Reporting): Single aggregate, no child entities

### Value Objects
- **StationId**: Immutable identifier shared across contexts
- **PostalCode**: Berlin-specific validation (10xxx-14xxx)
- **StationStatus**: Enum (Available, Defective, InUse, Maintenance)
- **ReportStatus**: Enum (Submitted, Validated, TicketCreated, Resolved)
- **MalfunctionType**: Enum (6 categories of station issues)
- **ReportDescription**: Validated text (10-500 characters)

### Integration Patterns
- **Customer-Supplier**: Reporting context depends on Discovery context
- **Shared Kernel**: StationId value object shared between contexts
- **Repository Pattern**: Abstract data access for testability
- **Use Cases**: Clear application layer boundaries

---

## 🎓 Academic Project Details

This project was developed as part of an Advanced Software Engineering course, demonstrating:

✅ **Domain-Driven Design** principles
✅ **Clean Architecture** with clear layer separation
✅ **Test-Driven Development** (92% coverage)
✅ **SOLID Principles** implementation
✅ **Value Objects** for domain validation
✅ **Repository Pattern** for data abstraction
✅ **Use Case Pattern** for application logic
✅ **Bounded Contexts** for domain isolation

---

## 📝 License

This project is developed for educational purposes.

---

## 🙏 Acknowledgments

- **Bundesnetzagentur** for providing the Ladesäulenregister dataset
- **Streamlit** for the excellent web framework
- **Course Instructors** for guidance on DDD principles

---

**⚡ Built with passion for sustainable urban mobility! 🌱**