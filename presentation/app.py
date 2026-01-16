import sys
import os

# Add project root to Python path for Streamlit Cloud compatibility
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import streamlit as st
import folium
from streamlit_folium import st_folium

# Discovery Context
from contexts.discovery.application.use_cases.search_stations_use_case import SearchStationsUseCase
from contexts.discovery.infrastructure.repositories.in_memory_station_repository import InMemoryStationRepository
from contexts.discovery.infrastructure.data.ladesaeulenregister_loader import LadesaeulenregisterLoader

# Reporting Context
from contexts.reporting.domain.services.malfunction_report_service import MalfunctionReportService
from contexts.reporting.infrastructure.repositories.in_memory_report_repository import InMemoryReportRepository
from contexts.reporting.domain.enums.malfunction_type import MalfunctionType
from contexts.reporting.domain.enums.report_status import ReportStatus

# Reporting Application Layer (Use Cases & DTOs)
from contexts.reporting.application.use_cases.create_malfunction_report_use_case import CreateMalfunctionReportUseCase
from contexts.reporting.application.use_cases.resolve_malfunction_use_case import ResolveMalfunctionUseCase
from contexts.reporting.application.dtos.create_report_dto import CreateReportRequest
from contexts.reporting.application.dtos.resolve_report_dto import ResolveReportRequest

# Shared
from contexts.shared_kernel.common.station_id import StationId


# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Berlin EV Charging Network",
    layout="wide",
    page_icon="🔌"
)

# --- INITIALIZE SYSTEM (Cached) ---
@st.cache_resource
def init_system():
    """Initialize repositories, load data, and create service"""
    station_repo = InMemoryStationRepository()
    report_repo = InMemoryReportRepository()
    
    # Load real Berlin stations from CSV
    loader = LadesaeulenregisterLoader()
    berlin_stations = loader.load_berlin_stations()
    
    for station in berlin_stations:
        station_repo.save(station)
    
    service = MalfunctionReportService(report_repo, station_repo)
    
    return service, station_repo

service, station_repo = init_system()

# --- AUTHENTICATION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Initialize session state for report form
if 'selected_postal_code' not in st.session_state:
    st.session_state.selected_postal_code = None
if 'selected_station_id' not in st.session_state:
    st.session_state.selected_station_id = None

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🔌 Berlin EV Network")
page = st.sidebar.radio(
    "Navigation",
    ["🔍 Search Stations", "📢 Report Issue", "👷 Operator Dashboard"]
)

st.sidebar.divider()

# Get real-time stats
all_reports = service.get_all_reports()
open_reports = [r for r in all_reports if r.status != ReportStatus.RESOLVED]
defective_stations = [s for s in station_repo.find_all() if s.status.value == "defective"]

st.sidebar.info(
    f"**📊 Network Status**\n\n"
    f"Total Stations: {len(station_repo.find_all())}\n\n"
    f"Active Reports: {len(open_reports)}\n\n"
    f"Defective Stations: {len(defective_stations)}"
)

# ============================================================================
# PAGE 1: SEARCH CHARGING STATIONS (Public)
# ============================================================================
if page == "🔍 Search Stations":
    st.title("🔍 Search Berlin Charging Stations")
    st.markdown("Find available charging stations by postal code")
    
    # Search input
    col1, col2 = st.columns([3, 1])
    with col1:
        postal_code = st.text_input(
            "Enter Postal Code",
            placeholder="e.g., 10115, 10178, 10785",
            help="Berlin postal codes start with 1",
            key="postal_code_search"
        )
    
    with col2:
        search_button = st.button("🔍 Search", use_container_width=True, type="primary")
    
    # Search using Use Case (handles validation via PostalCode value object)
    if search_button:
        if not postal_code:
            st.error("❌ Please enter a postal code")
        else:
            try:
                # Use the SearchStationsUseCase (proper DDD architecture)
                search_use_case = SearchStationsUseCase(station_repo)
                stations = search_use_case.execute_by_postal_code(postal_code)
                
                if not stations:
                    st.warning(f"⚠️ No charging stations found in postal code {postal_code}")
                else:
                    st.success(f"✅ Found {len(stations)} charging station(s) in {postal_code}")
                    
                    # Create map with ALL stations as pins
                    stations_with_coords = [s for s in stations if s.latitude and s.longitude]
                    
                    if stations_with_coords:
                        st.subheader("📍 Station Locations Map")
                        
                        # Calculate bounds to fit all stations
                        lats = [s.latitude for s in stations_with_coords]
                        lons = [s.longitude for s in stations_with_coords]
                        
                        # Center of all stations
                        center_lat = sum(lats) / len(lats)
                        center_lon = sum(lons) / len(lons)
                        
                        # Create map
                        m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
                        
                        # Add markers for each station
                        for station in stations_with_coords:
                            if station.status.value == "available":
                                icon_color = "green"
                                icon = "ok-sign"
                            elif station.status.value == "defective":
                                icon_color = "red"
                                icon = "remove-sign"
                            elif station.status.value == "in_use":
                                icon_color = "blue"
                                icon = "time"
                            else:
                                icon_color = "gray"
                                icon = "question-sign"
                            
                            popup_text = f"""
                            <b>{station.name}</b><br>
                            Address: {station.address or 'N/A'}<br>
                            Status: <b>{station.status.value.upper()}</b><br>
                            ID: {station.station_id.value}
                            """
                            
                            folium.Marker(
                                location=[station.latitude, station.longitude],
                                popup=popup_text,
                                icon=folium.Icon(color=icon_color)
                            ).add_to(m)
                        
                        # Display the map
                        map_html = m._repr_html_()
                        st.components.v1.html(map_html, height=400)
                        st.caption(f"🗺️ Showing {len(stations_with_coords)} stations | 🟢 Available | 🔴 Defective | 🔵 In Use")
                    else:
                        st.warning("⚠️ No GPS coordinates available for stations in this area")
                    
                    st.divider()
                    st.subheader("📋 Station Details")
                    
                    # Display stations as expandable cards
                    for i, station in enumerate(stations, 1):
                        with st.expander(f"📍 {station.name}", expanded=i<=3):
                            col_a, col_b = st.columns([2, 1])
                            
                            with col_a:
                                st.write(f"**Address:** {station.address or 'Berlin'}")
                                st.write(f"**Postal Code:** {station.postal_code}")
                                st.write(f"**Station ID:** {station.station_id.value}")
                                
                                if station.latitude and station.longitude:
                                    st.write(f"**Coordinates:** {station.latitude:.4f}, {station.longitude:.4f}")
                            
                            with col_b:
                                # Status indicator
                                if station.status.value == "available":
                                    st.success("🟢 **AVAILABLE**")
                                    st.caption("Ready to charge")
                                elif station.status.value == "defective":
                                    st.error("🔴 **DEFECTIVE**")
                                    st.caption("Under maintenance")
                                elif station.status.value == "in_use":
                                    st.info("🔵 **IN USE**")
                                    st.caption("Currently charging")
                                
                                        
            except ValueError as e:
                # PostalCode validation errors (from value object)
                st.error(f"❌ {str(e)}")
    
    # Display default Berlin map if no search button was pressed
    else:
        if not postal_code:
            st.info("🗺️ Enter a postal code to search for charging stations in that area")
            
            # Create default Berlin overview map
            berlin_center = [52.5200, 13.4050]  # Berlin center coordinates
            default_map = folium.Map(
                location=berlin_center, 
                zoom_start=11,
                tiles='OpenStreetMap'
            )
            
            # Add a marker for Berlin center
            folium.Marker(
                location=berlin_center,
                popup="<b>Berlin City Center</b><br>Search by postal code to find charging stations",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(default_map)
            
            # Display the map
            st.subheader("📍 Berlin Overview Map")
            map_html = default_map._repr_html_()
            st.components.v1.html(map_html, height=400)
            st.caption("🔍 Enter a postal code above to find charging stations in specific areas")

# ============================================================================
# PAGE 2: REPORT MALFUNCTION (Public)
# ============================================================================
elif page == "📢 Report Issue":
    st.title("📢 Report Station Malfunction")
    st.markdown("Help us maintain the charging network by reporting issues")
    
    # Step 1: Find station by postal code
    st.subheader("🔍 Step 1: Find Your Station")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        postal_input = st.text_input(
            "Enter Postal Code",
            value=st.session_state.selected_postal_code or "",
            placeholder="e.g., 10115, 10178",
            help="Enter the postal code where the station is located"
        )
    
    with col2:
        find_button = st.button("🔍 Find Stations", use_container_width=True)
    
    available_stations = []
    
    if find_button or st.session_state.selected_postal_code:
        if postal_input:
            try:
                # Use SearchStationsUseCase
                search_use_case = SearchStationsUseCase(station_repo)
                all_stations = search_use_case.execute_by_postal_code(postal_input)
                
                # Filter only operational (not already defective)
                available_stations = [s for s in all_stations if s.is_operational]
                
                if not available_stations:
                    st.warning(f"⚠️ No operational stations found in postal code {postal_input}")
                else:
                    st.success(f"✅ Found {len(available_stations)} operational station(s)")
                    st.session_state.selected_postal_code = postal_input
                    
            except ValueError as e:
                st.error(f"❌ {str(e)}")
        else:
            st.info("👆 Enter a postal code to find stations")
    
    # Step 2: Select station and report issue
    if available_stations or st.session_state.selected_postal_code:
        st.divider()
        st.subheader("⚠️ Step 2: Report the Issue")
        
        # If we have stations, show the form
        if available_stations:
            with st.form("malfunction_report_form"):
                st.write("**Select Station and Describe the Problem**")
                
                # Station selection
                station_options = {
                    f"{s.name} - {s.address or 'Berlin'} ({s.station_id.value})": s.station_id.value 
                    for s in available_stations
                }
                
                # Pre-select if coming from search page
                default_index = 0
                if st.session_state.selected_station_id:
                    try:
                        matching_keys = [k for k, v in station_options.items() 
                                       if v == st.session_state.selected_station_id]
                        if matching_keys:
                            default_index = list(station_options.keys()).index(matching_keys[0])
                    except:
                        pass
                
                selected_station = st.selectbox(
                    "Select Station",
                    options=list(station_options.keys()),
                    index=default_index,
                    help="Choose the station with the malfunction"
                )
                
                selected_id = station_options[selected_station]
                
                # Malfunction type
                m_type = st.selectbox(
                    "Malfunction Type",
                    options=[
                        MalfunctionType.NOT_CHARGING,
                        MalfunctionType.PAYMENT_FAILURE,
                        MalfunctionType.CONNECTOR_ISSUE,
                        MalfunctionType.PHYSICAL_DAMAGE,
                        MalfunctionType.DISPLAY_MALFUNCTION,
                        MalfunctionType.OTHER
                    ],
                    format_func=lambda x: x.value.replace('_', ' ').title(),
                    help="Select the type of issue you're experiencing"
                )
                
                # Description
                description = st.text_area(
                    "Description (10-500 characters)",
                    placeholder="Please describe the issue in detail...",
                    help="Minimum 10 characters, maximum 500 characters",
                    max_chars=500
                )
                
                # Character counter
                if description:
                    char_count = len(description)
                    if char_count < 10:
                        st.warning(f"⚠️ {10 - char_count} more characters needed")
                    else:
                        st.success(f"✅ {char_count}/500 characters")
                
                email = st.text_input(
                    "Your Email (Optional)",
                    placeholder="email@example.com",
                    help="We'll notify you when the issue is resolved"
                )
                
                submit = st.form_submit_button(
                    "🚀 Submit Report",
                    use_container_width=True,
                    type="primary"
                )
                
                if submit:
                    try:
                        # Use the CreateMalfunctionReportUseCase (proper DDD architecture)
                        create_use_case = CreateMalfunctionReportUseCase(service)
                        
                        request = CreateReportRequest(
                            station_id=selected_id,
                            malfunction_type=m_type,
                            description=description,
                            reported_by=email if email else None
                        )
                        
                        result = create_use_case.execute(request)
                        
                        if result.success:
                            st.success(
                                f"✅ **Report Submitted Successfully!**\n\n"
                                f"Ticket ID: `{result.ticket_id[:8]}...`\n\n"
                                f"The station has been marked as defective and maintenance has been notified."
                            )
                            st.balloons()
                            
                            # Reset form
                            st.session_state.selected_postal_code = None
                            st.session_state.selected_station_id = None
                        else:
                            st.error(
                                f"❌ **Validation Failed**\n\n" +
                                "\n".join(f"- {error}" for error in result.errors)
                            )
                            
                    except ValueError as e:
                        st.error(f"⚠️ **Validation Error:** {str(e)}")
        else:
            st.info("👆 Enter a postal code above to find stations in that area")

# ============================================================================
# PAGE 3: OPERATOR DASHBOARD (Login Required)
# ============================================================================
elif page == "👷 Operator Dashboard":
    
    # Authentication check
    if not st.session_state.authenticated:
        st.title("🔐 Operator Login")
        st.markdown("Please login to access the operator dashboard")
        
        col_login1, col_login2, col_login3 = st.columns([1, 2, 1])
        
        with col_login2:
            with st.form("login_form"):
                st.write("**System Operator Access**")
                username = st.text_input("Username", placeholder="operator")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                login_button = st.form_submit_button("🔓 Login", use_container_width=True, type="primary")
                
                if login_button:
                    # Simple authentication (demo)
                    if username == "operator" and password == "berlin2025":
                        st.session_state.authenticated = True
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
            
            st.divider()
            
            with st.expander("ℹ️ Demo Credentials", expanded=True):
                st.code("Username: operator\nPassword: berlin2025")
                st.caption("""
                **Note:** In a production system, credentials would be:
                - Stored securely in a database (hashed with bcrypt/argon2)
                - Use JWT tokens or session management
                - Support multiple operators with role-based access
                - Include 2FA for security
                
                For this demo/assignment, hardcoded credentials are acceptable
                to demonstrate the authentication flow.
                """)
    
    else:
        # Authenticated - show dashboard
        col_header1, col_header2 = st.columns([4, 1])
        
        with col_header1:
            st.title("👷 Operator Dashboard")
            st.markdown("**Berlin-Wide Network Management** - All stations across Berlin")
        
        with col_header2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()
        
        # Get reports
        all_reports = service.get_all_reports()
        open_reports = [r for r in all_reports if r.status != ReportStatus.RESOLVED]
        resolved_reports = [r for r in all_reports if r.status == ReportStatus.RESOLVED]
        
        # Metrics
        metric1, metric2, metric3, metric4 = st.columns(4)
        metric1.metric("📊 Total Reports", len(all_reports))
        metric2.metric("🔴 Open Tickets", len(open_reports))
        metric3.metric("✅ Resolved", len(resolved_reports))
        
        defective_count = len([s for s in station_repo.find_all() if s.status.value == "defective"])
        metric4.metric("⚠️ Defective Stations", defective_count)
        
        st.divider()
        
        # Open Tickets Section
        st.subheader("🔴 Open Tickets - Requires Attention")
        
        if not open_reports:
            st.success("✅ No open tickets! All stations across Berlin are operational.")
            st.balloons()
        else:
            st.warning(f"⚠️ {len(open_reports)} station(s) need maintenance")
            
            for report in open_reports:
                station = station_repo.find_by_id(report.station_id)
                
                with st.expander(
                    f"🎫 Ticket: {str(report.ticket_id)[:8]}... | {station.name} ({station.postal_code})",
                    expanded=True
                ):
                    col_a, col_b = st.columns([2, 1])
                    
                    with col_a:
                        st.write(f"**Station:** {station.name}")
                        st.write(f"**Address:** {station.address or 'Berlin'}")
                        st.write(f"**Station ID:** {report.station_id.value}")
                        st.write(f"**Report ID:** {report.report_id}")
                        st.write(f"**Malfunction Type:** {report._malfunction_type.value.replace('_', ' ').title()}")
                        st.write(f"**Description:** {report._description.value}")
                        st.write(f"**Reported By:** {report._reported_by or 'Anonymous'}")
                        st.write(f"**Created:** {report._created_at.strftime('%Y-%m-%d %H:%M')}")
                        st.write(f"**Status:** {report.status.value.upper()}")
                    
                    with col_b:
                        operator_notes = st.text_area(
                            "Resolution Notes",
                            placeholder="Describe what was fixed...\ne.g., 'Replaced connector cable. Tested charging cycle.'",
                            key=f"notes_{report.report_id}",
                            height=120
                        )
                        
                        if st.button(
                            "✅ Mark as Resolved",
                            key=f"resolve_{report.report_id}",
                            use_container_width=True,
                            type="primary"
                        ):
                            if report.ticket_id:
                                # Use the ResolveMalfunctionUseCase (proper DDD architecture)
                                resolve_use_case = ResolveMalfunctionUseCase(service)
                                
                                request = ResolveReportRequest(
                                    ticket_id=str(report.ticket_id),
                                    operator_notes=operator_notes or "Issue resolved by operator"
                                )
                                
                                response = resolve_use_case.execute(request)
                                
                                if response.success:
                                    st.success(f"✅ {response.message}")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {response.message}")
        
        st.divider()