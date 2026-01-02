
# ⚡ Berlin EV Charging Network

A production-ready, Domain-Driven Design (DDD) platform for discovering 1,989+ EV charging stations across Berlin and managing station malfunctions with real-time monitoring.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://berlin-ev-charging-platform-kdxxuctnz8adrhvikxqey7.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-25%20passing-success.svg)](./contexts/)
[![DDD](https://img.shields.io/badge/architecture-DDD-orange.svg)](https://en.wikipedia.org/wiki/Domain-driven_design)

---

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
│   │   ├── infrastructure/
│   │   │   ├── data/                # LadesaeulenregisterLoader (CSV)
│   │   │   └── repositories/        # InMemoryStationRepository
│   │   └── tests/                   # 13 passing tests
│   │
│   ├── reporting/                    # 🛠️ Malfunction Reporting Bounded Context
│   │   ├── domain/
│   │   │   ├── entities/            # MalfunctionReport (Aggregate Root)
│   │   │   ├── enums/               # MalfunctionType, ReportStatus
│   │   │   ├── services/            # MalfunctionReportService (Domain Logic)
│   │   │   └── exceptions/          # StationNotFound, InvalidReport
│   │   ├── application/
│   │   │   └── use_cases/           # Report submission workflows
│   │   ├── infrastructure/
│   │   │   └── repositories/        # InMemoryReportRepository
│   │   └── tests/                   # 12 passing tests
│   │
│   └── shared_kernel/                # 🔗 Shared Concepts
│       ├── common/                   # StationId (Value Object)
│       └── datasets/                 # Ladesaeulenregister.csv (1,989 stations)
│
├── presentation/
│   └── app.py                        # 🎨 Streamlit UI (Multi-page app)
│
├── requirements.txt                  # 📦 Dependencies
├── pytest.ini                        # 🧪 Test configuration
└── README.md                         # 📖 You are here
```

### 🎯 Key Design Patterns

| Pattern | Purpose | Implementation |
|---------|---------|----------------|
| **Bounded Contexts** | Separates station discovery from malfunction reporting | `contexts/discovery/` vs `contexts/reporting/` |
| **Entities** | Business objects with identity | `OperationalStation`, `MalfunctionReport` |
| **Value Objects** | Immutable domain concepts | `StationId`, `StationStatus`, `MalfunctionType` |
| **Repository Pattern** | Abstracts data persistence | `IStationRepository`, `InMemoryStationRepository` |
| **Domain Services** | Complex business workflows | `MalfunctionReportService` |
| **Layered Architecture** | Dependency inversion | Domain ← Application ← Infrastructure ← Presentation |
| **Use Cases** | Application-specific business rules | `SearchStationsUseCase` |

---

## 🧪 Testing

The project maintains **100% test coverage** of domain logic with **25 passing tests**:

```bash
# Run all tests
pytest contexts/

# Run with coverage report
pytest --cov=contexts --cov-report=html contexts/

# Run specific context tests
pytest contexts/discovery/tests/         # 13 tests
pytest contexts/reporting/tests/         # 12 tests
pytest contexts/shared_kernel/tests/     # Shared tests

# Run with verbose output
pytest -v contexts/

# Run specific test file
pytest contexts/discovery/tests/test_operational_station.py -v
```

### Test Coverage
- ✅ **Domain Entities**: Station and Report lifecycle
- ✅ **Value Objects**: StationId uniqueness, Status transitions
- ✅ **Business Rules**: Validation, constraints, invariants
- ✅ **Repository Operations**: CRUD, filtering, state management
- ✅ **Integration Flows**: End-to-end reporting workflow
- ✅ **Edge Cases**: Invalid inputs, duplicate reports, missing stations

---

## 🛠️ Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Backend language | 3.10+ |
| **Streamlit** | Web framework & UI | 1.40.0 |
| **Folium** | Interactive maps | 0.15.0 |
| **Pandas** | Data processing | 2.2.0+ |
| **Pytest** | Testing framework | 7.4.0 |
| **UUID** | Unique ID generation | stdlib |

---

## 📦 Installation & Local Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/kezia-fernandes/Berlin-EV-Charging-Platform.git
cd Berlin-EV-Charging-Platform

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests to verify setup
pytest contexts/

# 5. Launch the application
streamlit run presentation/app.py
```

The app will automatically open at `http://localhost:8501` 🎉

---

## 📊 Data Source

Station data sourced from **Bundesnetzagentur** (German Federal Network Agency):

- **Dataset**: Ladesäulenregister (EV Charging Station Registry)
- **Coverage**: 1,989 stations across all Berlin postal codes
- **Attributes**:
  - GPS coordinates (latitude, longitude)
  - Full addresses and postal codes
  - Station operator information
  - Installation dates
- **Update Frequency**: Government maintains official registry
- **License**: Public domain government data

---

## 🎯 User Journeys

### 🙋 **For Public Users**

1. **Find Charging Stations**
   - Enter Berlin postal code (e.g., 10115, 10178, 12345)
   - View interactive map with all stations in that area
   - Click any station to see detailed information
   - Check real-time availability status

2. **Report Malfunctions**
   - Navigate to "Report Issue" page
   - Enter Station ID from physical station label
   - Select malfunction type from dropdown
   - Describe the issue in detail
   - Receive confirmation with ticket ID
   - Station automatically marked as "Defective"

### 👨‍💼 **For Network Operators**

1. **Login to Dashboard**
   - Navigate to "Operator Dashboard"
   - Enter credentials (demo: operator/berlin2025)
   - Access secure operator interface

2. **Monitor Network Health**
   - View total station count (1,989)
   - Track active malfunction reports
   - Identify defective stations
   - Monitor resolution metrics

3. **Resolve Issues**
   - Review all open tickets with details
   - Inspect station ID, malfunction type, and description
   - Click "Resolve" after fixing the issue
   - Station automatically restored to "Available"
   - Ticket marked as "Resolved"

---

## 🚀 Deployment

The application is deployed on **Streamlit Community Cloud**:

### Deployment Configuration

```toml
# .streamlit/config.toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
```

### Environment Variables
- No secrets required for public demo
- In production, store operator credentials in Streamlit secrets

### Continuous Deployment
- Automatic deployment on `git push` to `main` branch
- GitHub integration via Streamlit Cloud dashboard

---

## 🔮 Future Enhancements

- [ ] **Real Database**: Replace in-memory repos with PostgreSQL/MongoDB
- [ ] **User Authentication**: Full user registration and role-based access
- [ ] **Real-time Updates**: WebSocket integration for live status changes
- [ ] **Mobile App**: React Native companion app
- [ ] **Email Notifications**: Alert operators of new reports
- [ ] **Analytics Dashboard**: Historical trends and usage patterns
- [ ] **Multi-language Support**: German and English interfaces
- [ ] **Route Planning**: Navigate to nearest available station
- [ ] **Payment Integration**: Reserve and pay for charging sessions
- [ ] **API Gateway**: RESTful API for third-party integrations

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Write tests for new functionality
4. Ensure all tests pass (`pytest contexts/`)
5. Commit your changes (`git commit -m 'Add AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Maintain test coverage above 90%
- Document all public methods and classes
- Use type hints for function signatures

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---


## 🙏 Acknowledgments

- **Data Source**: Bundesnetzagentur (German Federal Network Agency)
- **DDD Inspiration**: Eric Evans' "Domain-Driven Design" book
- **Framework**: Streamlit for rapid prototyping
- **Deployment**: Streamlit Community Cloud for free hosting
- **Community**: Thanks to all contributors and users!

---

## 📸 Screenshots

### Station Search
![Station Search](https://via.placeholder.com/800x400?text=Station+Search+Interface)

### Malfunction Reporting
![Report Issue](https://via.placeholder.com/800x400?text=Malfunction+Reporting)

### Operator Dashboard
![Dashboard](https://via.placeholder.com/800x400?text=Operator+Dashboard)

---

## 📞 Support

- 📖 **Documentation**: Check this README
- 🐛 **Bug Reports**: [Open an issue](https://github.com/kezia-fernandes/Berlin-EV-Charging-Platform/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/kezia-fernandes/Berlin-EV-Charging-Platform/discussions)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ and ☕ in Berlin

[🔗 Live Demo](https://berlin-ev-charging-platform-kdxxuctnz8adrhvikxqey7.streamlit.app/) • [📖 Documentation](./docs/) • [🐛 Report Bug](https://github.com/kezia-fernandes/Berlin-EV-Charging-Platform/issues)

</div>
