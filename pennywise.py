import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION (Clean, uncluttered UI per Reverse Thinking notes) ---
st.set_page_config(
    page_title="PennyWise | Smart Checkout & Fare Navigator",
    page_icon="🪙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean cards and badges
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #2e7d32;
        margin-bottom: 12px;
        color: #1f2937;
    }
    .best-badge {
        background-color: #d4edda;
        color: #155724;
        padding: 4px 8px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 0.85em;
    }
    .rank-badge {
        background-color: #e3f2fd;
        color: #0d47a1;
        padding: 4px 8px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 0.85em;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: FLIGHT-NAVIGATION CONDITIONS & PREFERENCES ---
with st.sidebar:
    st.title("🪙 PennyWise")
    st.caption("Smart All-In Price & Fare Navigator")
    st.divider()
    
    domain = st.radio(
        "Select Category",
        [
            "🛒 Quick-Commerce & Groceries", 
            "🚕 Ride-Hailing & Local Cabs",
            "✈️ Flights",
            "🛍️ Shopping & Apparel",
            "🏨 Hotels & Stays"
        ],
        index=4
    )
    
    st.divider()
    st.subheader("🧭 Navigation Conditions")
    st.caption("Adjust real-world factors affecting final checkout prices:")
    
    weather = st.select_slider(
        "Current Weather",
        options=["Clear", "Light Rain", "Heavy Rain / Storm"],
        value="Light Rain"
    )
    
    demand = st.select_slider(
        "Demand / Rush Level",
        options=["Off-Peak", "Normal", "Peak Rush / Festival"],
        value="Normal"
    )
    
    st.divider()
    
    priority = st.radio(
        "What matters most right now?",
        ["💰 Lowest Final Price", "⚡ Fastest & Most Reliable", "🏪 Local / In-Person Option"],
        index=0
    )

# --- HEADER ---
st.title("🪙 PennyWise")
st.markdown("Compare **true all-in checkout prices** across apps, local stores, airlines, apparel brands, and hotels—including hidden taxes, service charges, and smarter alternatives.")

# Surge Multiplier Logic
weather_mult = {"Clear": 1.0, "Light Rain": 1.15, "Heavy Rain / Storm": 1.35}[weather]
demand_mult = {"Off-Peak": 0.95, "Normal": 1.0, "Peak Rush / Festival": 1.25}[demand]
total_mult = round(weather_mult * demand_mult, 2)

# Condition Banner
col_status1, col_status2 = st.columns([3, 1])
with col_status1:
    if total_mult > 1.1:
        st.warning(f"⚠️ **High Price Turbulence:** {weather} + {demand} is adding extra surge, convenience, or peak-occupancy fees.")
    else:
        st.success(f"✅ **Smooth Conditions:** {weather} & {demand}. Hidden fees and surge pricing are currently minimal.")
with col_status2:
    st.metric(
        "Price Forecast (Next 30m)", 
        "Dropping ↓" if total_mult > 1.2 else "Stable →", 
        delta="-₹30 expected" if total_mult > 1.2 else "Good time to book"
    )

st.divider()

# ==============================================================================
# MODE 1: QUICK-COMMERCE & LOCAL GROCERY STORES
# ==============================================================================
if "Groceries" in domain:
    st.subheader("🛒 Universal Cart Simulator")
    
    item_prices = {
        "Blinkit": {
            "Milk": 62, "Eggs": 84, "Apples": 160, "Bread": 45, 
            "Oranges": 95, "Lemons": 30, "Bananas": 50, "Yogurt": 40, "Paneer": 95
        },
        "Zepto": {
            "Milk": 60, "Eggs": 82, "Apples": 155, "Bread": 48, 
            "Oranges": 90, "Lemons": 28, "Bananas": 48, "Yogurt": 42, "Paneer": 92
        },
        "Swiggy Instamart": {
            "Milk": 64, "Eggs": 86, "Apples": 165, "Bread": 45, 
            "Oranges": 98, "Lemons": 32, "Bananas": 52, "Yogurt": 38, "Paneer": 98
        },
        "Ratnadeep Retail": {
            "Milk": 60, "Eggs": 80, "Apples": 150, "Bread": 45, 
            "Oranges": 88, "Lemons": 25, "Bananas": 45, "Yogurt": 40, "Paneer": 90
        },
        "Agarwal Stores": {
            "Milk": 58, "Eggs": 75, "Apples": 145, "Bread": 42, 
            "Oranges": 82, "Lemons": 20, "Bananas": 40, "Yogurt": 35, "Paneer": 85
        },
        "Thumkunta Local Mart": {
            "Milk": 58, "Eggs": 74, "Apples": 140, "Bread": 40, 
            "Oranges": 80, "Lemons": 18, "Bananas": 38, "Yogurt": 35, "Paneer": 84
        },
        "Omkar Super Bazaar": {
            "Milk": 59, "Eggs": 76, "Apples": 142, "Bread": 42, 
            "Oranges": 85, "Lemons": 22, "Bananas": 42, "Yogurt": 36, "Paneer": 86
        }
    }

    grocery_options = ["Milk", "Eggs", "Apples", "Bread", "Oranges", "Lemons", "Bananas", "Yogurt", "Paneer"]
    
    selected_items = st.multiselect(
        "Select Grocery Items (choose one or more):",
        options=grocery_options,
        default=["Milk", "Eggs", "Bread", "Paneer"]
    )
    
    if not selected_items:
        st.info("👆 Select one or more grocery items from the dropdown above to see stores ranked by collective lowest cost.")
    else:
        def calc_cart(store_name):
            return sum(item_prices[store_name][item] for item in selected_items)

        stores = [
            {
                "Store / App": "Blinkit",
                "Type": "Quick-Commerce App",
                "Items Base Total": calc_cart("Blinkit"),
                "Delivery Fee": int(25 * total_mult),
                "Handling & Rain Fee": int(18 * weather_mult),
                "Coupon Discount": -20 if len(selected_items) >= 3 else 0,
                "ETA (mins)": 12,
                "Reliability": "98%"
            },
            {
                "Store / App": "Zepto",
                "Type": "Quick-Commerce App",
                "Items Base Total": calc_cart("Zepto"),
                "Delivery Fee": int(30 * total_mult),
                "Handling & Rain Fee": int(22 * weather_mult),
                "Coupon Discount": -15 if len(selected_items) >= 3 else 0,
                "ETA (mins)": 10,
                "Reliability": "95%"
            },
            {
                "Store / App": "Swiggy Instamart",
                "Type": "Quick-Commerce App",
                "Items Base Total": calc_cart("Swiggy Instamart"),
                "Delivery Fee": int(15 * total_mult),
                "Handling & Rain Fee": int(15 * weather_mult),
                "Coupon Discount": -25 if len(selected_items) >= 4 else 0,
                "ETA (mins)": 18,
                "Reliability": "92%"
            },
            {
                "Store / App": "Ratnadeep Retail",
                "Type": "Local Supermarket",
                "Items Base Total": calc_cart("Ratnadeep Retail"),
                "Delivery Fee": 20,
                "Handling & Rain Fee": 0,
                "Coupon Discount": -10 if len(selected_items) >= 3 else 0,
                "ETA (mins)": 25,
                "Reliability": "99%"
            },
            {
                "Store / App": "Agarwal Stores",
                "Type": "Local Store",
                "Items Base Total": calc_cart("Agarwal Stores"),
                "Delivery Fee": 0,
                "Handling & Rain Fee": 0,
                "Coupon Discount": 0,
                "ETA (mins)": 20,
                "Reliability": "100%"
            },
            {
                "Store / App": "Thumkunta Local Mart",
                "Type": "Local Store",
                "Items Base Total": calc_cart("Thumkunta Local Mart"),
                "Delivery Fee": 0,
                "Handling & Rain Fee": 0,
                "Coupon Discount": 0,
                "ETA (mins)": 15,
                "Reliability": "100%"
            },
            {
                "Store / App": "Omkar Super Bazaar",
                "Type": "Local Store",
                "Items Base Total": calc_cart("Omkar Super Bazaar"),
                "Delivery Fee": 10,
                "Handling & Rain Fee": 0,
                "Coupon Discount": -5 if len(selected_items) >= 3 else 0,
                "ETA (mins)": 22,
                "Reliability": "99%"
            }
        ]
        
        df = pd.DataFrame(stores)
        df["Collective Final Total (₹)"] = (
            df["Items Base Total"] + 
            df["Delivery Fee"] + 
            df["Handling & Rain Fee"] + 
            df["Coupon Discount"]
        )
        
        if "Lowest Final Price" in priority:
            df = df.sort_values(by="Collective Final Total (₹)", ascending=True)
        elif "Fastest" in priority:
            df = df.sort_values(by="ETA (mins)", ascending=True)
        else:
            df = df[df["Type"].str.contains("Local")].sort_values(by="Collective Final Total (₹)", ascending=True)
            
        df.insert(0, "Rank", [f"#{i+1}" for i in range(len(df))])
        
        best = df.iloc[0]
        worst_total = df["Collective Final Total (₹)"].max()
        savings = worst_total - best["Collective Final Total (₹)"]

        st.markdown(f"""
        <div class="metric-card">
            <span class="best-badge">★ #1 PENNYWISE PICK ({priority.split(' ', 1)[1].upper()})</span>
            <h3>{best['Store / App']} — ₹{best['Collective Final Total (₹)']} All-In ({len(selected_items)} items)</h3>
            <p><b>Items:</b> {', '.join(selected_items)}<br>
            <b>Type:</b> {best['Type']} | <b>ETA:</b> {best['ETA (mins)']} mins | <b>Hidden Fees:</b> ₹{best['Delivery Fee'] + best['Handling & Rain Fee']} | <b>You Save:</b> ₹{savings} vs highest option</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"#### Ranked Options for Your {len(selected_items)}-Item Basket")
        st.dataframe(
            df[["Rank", "Store / App", "Type", "Items Base Total", "Delivery Fee", "Handling & Rain Fee", "Coupon Discount", "Collective Final Total (₹)", "ETA (mins)", "Reliability"]],
            use_container_width=True,
            hide_index=True
        )
        
        with st.expander("🔍 View Item-by-Item Price Breakdown Across Stores"):
            breakdown_data = {store: {item: item_prices[store][item] for item in selected_items} for store in item_prices}
            breakdown_df = pd.DataFrame(breakdown_data).T
            breakdown_df["Items Subtotal (₹)"] = breakdown_df.sum(axis=1)
            st.dataframe(breakdown_df.sort_values(by="Items Subtotal (₹)"), use_container_width=True)

        st.divider()
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("#### 👻 Ghost-Cart Optimizer")
            st.info(
                "**Split-Order Insight:** Picking up bulk items from **Thumkunta Local Mart / Agarwal Stores** and ordering urgent items on **Zepto** "
                "avoids surge markups while keeping delivery fast."
            )
            if st.button("Simulate Split Ghost-Cart"):
                st.success("Ghost-Cart activated! Combined basket total optimized.")
                
        with col_g2:
            st.markdown("#### 🏘️ Neighbor Order Syncing")
            st.info(
                "**2 neighbors** near you are placing a group order with **Ratnadeep / Omkar**. "
                "Sync your cart to waive delivery charges."
            )
            if st.button("Sync with Neighbor Cart (-₹20)"):
                st.success("Synced! Delivery fees waived.")

# ==============================================================================
# MODE 2: RIDE-HAILING & LOCAL HYDERABAD/SECUNDERABAD CABS
# ==============================================================================
elif "Cabs" in domain:
    st.subheader("🚕 Ride-Hailing & Local Cab Navigator")
    
    stops_list = [
        "Secunderabad Station",
        "Kachiguda",
        "Hyderabad Deccan",
        "RGIA",
        "Begumpet",
        "BITS Hyderabad"
    ]
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        pickup = st.selectbox("Pickup Stop", stops_list, index=0)
    with col_r2:
        dropoff = st.selectbox("Destination Stop", stops_list, index=3)
        
    if pickup == dropoff:
        st.warning("Pickup and Destination stops are the same. Please select two different stops.")
    else:
        long_routes = {
            ("Secunderabad Station", "RGIA"), ("RGIA", "Secunderabad Station"),
            ("BITS Hyderabad", "RGIA"), ("RGIA", "BITS Hyderabad"),
            ("Kachiguda", "RGIA"), ("RGIA", "Kachiguda"),
            ("Hyderabad Deccan", "RGIA"), ("RGIA", "Hyderabad Deccan"),
            ("Begumpet", "RGIA"), ("RGIA", "Begumpet"),
            ("BITS Hyderabad", "Kachiguda"), ("Kachiguda", "BITS Hyderabad"),
            ("BITS Hyderabad", "Hyderabad Deccan"), ("Hyderabad Deccan", "BITS Hyderabad")
        }
        
        is_long_route = (pickup, dropoff) in long_routes
        base_km_fare = 650 if is_long_route else 240
        base_eta = 12 if is_long_route else 6

        rides = [
            {
                "Provider": "Uber Go",
                "Category": "App Aggregator",
                "Base Fare": base_km_fare,
                "Surge & Weather Fee": int(base_km_fare * 0.25 * (total_mult - 0.85)),
                "Platform/Toll Fee": 45 if is_long_route else 15,
                "Pickup ETA (mins)": base_eta - 2,
                "Cancellation Risk": "Medium (15%)"
            },
            {
                "Provider": "Ola Mini",
                "Category": "App Aggregator",
                "Base Fare": base_km_fare - 15,
                "Surge & Weather Fee": int(base_km_fare * 0.30 * (total_mult - 0.85)),
                "Platform/Toll Fee": 50 if is_long_route else 20,
                "Pickup ETA (mins)": base_eta,
                "Cancellation Risk": "High (22%)"
            },
            {
                "Provider": "Rapido Cab",
                "Category": "App Aggregator",
                "Base Fare": base_km_fare - 25,
                "Surge & Weather Fee": int(base_km_fare * 0.18 * (total_mult - 0.85)),
                "Platform/Toll Fee": 35 if is_long_route else 10,
                "Pickup ETA (mins)": base_eta - 1,
                "Cancellation Risk": "Low (9%)"
            },
            {
                "Provider": "Royal Destiny Tours",
                "Category": "Local Cab",
                "Base Fare": base_km_fare - 10,
                "Surge & Weather Fee": 0,
                "Platform/Toll Fee": 30 if is_long_route else 0,
                "Pickup ETA (mins)": base_eta + 5,
                "Cancellation Risk": "Very Low (2%)"
            },
            {
                "Provider": "Venkat Travels",
                "Category": "Local Cab",
                "Base Fare": base_km_fare - 30,
                "Surge & Weather Fee": 0,
                "Platform/Toll Fee": 30 if is_long_route else 0,
                "Pickup ETA (mins)": base_eta + 7,
                "Cancellation Risk": "Very Low (3%)"
            },
            {
                "Provider": "Ayush Travels",
                "Category": "Local Cab",
                "Base Fare": base_km_fare - 20,
                "Surge & Weather Fee": 0,
                "Platform/Toll Fee": 30 if is_long_route else 0,
                "Pickup ETA (mins)": base_eta + 4,
                "Cancellation Risk": "Very Low (2%)"
            },
            {
                "Provider": "Krishna Swamy Good Cabs",
                "Category": "Local Cab",
                "Base Fare": base_km_fare - 25,
                "Surge & Weather Fee": 0,
                "Platform/Toll Fee": 30 if is_long_route else 0,
                "Pickup ETA (mins)": base_eta + 6,
                "Cancellation Risk": "None (1%)"
            },
            {
                "Provider": "Jai Hanuman Travels",
                "Category": "Local Cab",
                "Base Fare": base_km_fare - 35,
                "Surge & Weather Fee": 0,
                "Platform/Toll Fee": 30 if is_long_route else 0,
                "Pickup ETA (mins)": base_eta + 8,
                "Cancellation Risk": "Very Low (3%)"
            }
        ]
        
        df_rides = pd.DataFrame(rides)
        df_rides["Final Fare (₹)"] = df_rides["Base Fare"] + df_rides["Surge & Weather Fee"] + df_rides["Platform/Toll Fee"]
        
        if "Lowest Final Price" in priority:
            df_rides = df_rides.sort_values(by="Final Fare (₹)")
        elif "Fastest" in priority:
            df_rides = df_rides.sort_values(by="Pickup ETA (mins)")
        else:
            df_rides = df_rides[df_rides["Category"] == "Local Cab"].sort_values(by="Final Fare (₹)")

        df_rides.insert(0, "Rank", [f"#{i+1}" for i in range(len(df_rides))])

        best_ride = df_rides.iloc[0]
        st.markdown(f"""
        <div class="metric-card">
            <span class="best-badge">★ #1 PENNYWISE BEST ROUTE ({pickup} ➔ {dropoff})</span>
            <h3>{best_ride['Provider']} — ₹{best_ride['Final Fare (₹)']} All-In</h3>
            <p><b>Category:</b> {best_ride['Category']} | <b>Pickup ETA:</b> {best_ride['Pickup ETA (mins)']} mins | <b>Cancellation Risk:</b> {best_ride['Cancellation Risk']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            df_rides[["Rank", "Provider", "Category", "Base Fare", "Surge & Weather Fee", "Platform/Toll Fee", "Final Fare (₹)", "Pickup ETA (mins)", "Cancellation Risk"]],
            use_container_width=True,
            hide_index=True
        )
        
        st.divider()
        st.markdown("#### 🚗 Group Car-Pooling Sync")
        st.info(
            f"**3 verified commuters** at **{pickup}** are also heading toward **{dropoff}** within 15 mins. "
            f"Splitting a sedan with **Krishna Swamy Good Cabs** or **Royal Destiny Tours** reduces your fare to **₹{int(best_ride['Final Fare (₹)'] / 3)}/person**."
        )

# ==============================================================================
# MODE 3: FLIGHTS (ALL-IN FARE & HIDDEN FEE NAVIGATOR)
# ==============================================================================
elif "Flights" in domain:
    st.subheader("✈️ Flight All-In Fare Navigator")
    
    cities = [
        "Mumbai", "Delhi", "Hyderabad", "Chennai", "Lucknow", "Guwahati",
        "Kochi", "Kolkata", "Bengaluru", "Varanasi", "Ahemdabad", "Jaipur"
    ]
    
    col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
    with col_f1:
        origin = st.selectbox("Origin City", cities, index=2)
    with col_f2:
        destination = st.selectbox("Destination City", cities, index=1)
    with col_f3:
        include_addons = st.checkbox("Include Cabin/Check-in Bag & Seat", value=True)
        
    if origin == destination:
        st.warning("Origin and Destination cities are the same. Please select two different cities.")
    else:
        long_haul_cities = {"Guwahati", "Kochi", "Kolkata", "Delhi", "Lucknow", "Varanasi", "Jaipur"}
        short_haul_cities = {"Mumbai", "Bengaluru", "Chennai", "Ahemdabad"}
        
        if (origin in long_haul_cities and destination in short_haul_cities) or (destination in long_haul_cities and origin in short_haul_cities):
            route_base = 4600
            flight_mins = 145
        elif origin == "Guwahati" or destination == "Guwahati":
            route_base = 5400
            flight_mins = 175
        else:
            route_base = 3400
            flight_mins = 95

        airlines_data = [
            {
                "Airline": "Indigo",
                "Stops": "Non-Stop",
                "Base Ticket (₹)": int(route_base * total_mult),
                "Airport & Fuel Tax (₹)": 780,
                "OTA Convenience Fee (₹)": 399,
                "Seat & Baggage Add-on (₹)": 650 if include_addons else 0,
                "Duration (mins)": flight_mins,
                "On-Time Score": "91%"
            },
            {
                "Airline": "Air India",
                "Stops": "Non-Stop",
                "Base Ticket (₹)": int((route_base + 450) * total_mult),
                "Airport & Fuel Tax (₹)": 820,
                "OTA Convenience Fee (₹)": 350,
                "Seat & Baggage Add-on (₹)": 0,
                "Duration (mins)": flight_mins + 5,
                "On-Time Score": "84%"
            },
            {
                "Airline": "Vistara",
                "Stops": "Non-Stop",
                "Base Ticket (₹)": int((route_base + 600) * total_mult),
                "Airport & Fuel Tax (₹)": 850,
                "OTA Convenience Fee (₹)": 350,
                "Seat & Baggage Add-on (₹)": 0,
                "Duration (mins)": flight_mins,
                "On-Time Score": "92%"
            },
            {
                "Airline": "Akasa air",
                "Stops": "Non-Stop",
                "Base Ticket (₹)": int((route_base - 250) * total_mult),
                "Airport & Fuel Tax (₹)": 760,
                "OTA Convenience Fee (₹)": 349,
                "Seat & Baggage Add-on (₹)": 600 if include_addons else 0,
                "Duration (mins)": flight_mins + 10,
                "On-Time Score": "90%"
            },
            {
                "Airline": "Air India express",
                "Stops": "1 Stop",
                "Base Ticket (₹)": int((route_base - 400) * total_mult),
                "Airport & Fuel Tax (₹)": 790,
                "OTA Convenience Fee (₹)": 349,
                "Seat & Baggage Add-on (₹)": 550 if include_addons else 0,
                "Duration (mins)": flight_mins + 85,
                "On-Time Score": "82%"
            },
            {
                "Airline": "Spicejet",
                "Stops": "1 Stop",
                "Base Ticket (₹)": int((route_base - 350) * total_mult),
                "Airport & Fuel Tax (₹)": 810,
                "OTA Convenience Fee (₹)": 420,
                "Seat & Baggage Add-on (₹)": 700 if include_addons else 0,
                "Duration (mins)": flight_mins + 95,
                "On-Time Score": "74%"
            }
        ]

        df_flights = pd.DataFrame(airlines_data)
        df_flights["True Checkout Total (₹)"] = (
            df_flights["Base Ticket (₹)"] +
            df_flights["Airport & Fuel Tax (₹)"] +
            df_flights["OTA Convenience Fee (₹)"] +
            df_flights["Seat & Baggage Add-on (₹)"]
        )
        df_flights["Duration"] = df_flights["Duration (mins)"].apply(lambda m: f"{m // 60}h {m % 60}m")

        if "Lowest Final Price" in priority:
            df_flights = df_flights.sort_values(by="True Checkout Total (₹)", ascending=True)
        elif "Fastest" in priority:
            df_flights = df_flights.sort_values(by="Duration (mins)", ascending=True)
        else:
            df_flights = df_flights[df_flights["Stops"] == "Non-Stop"].sort_values(by="True Checkout Total (₹)", ascending=True)

        df_flights.insert(0, "Rank", [f"#{i+1}" for i in range(len(df_flights))])

        best_flight = df_flights.iloc[0]
        hidden_fees = (
            best_flight["Airport & Fuel Tax (₹)"] + 
            best_flight["OTA Convenience Fee (₹)"] + 
            best_flight["Seat & Baggage Add-on (₹)"]
        )

        st.markdown(f"""
        <div class="metric-card">
            <span class="best-badge">★ #1 PENNYWISE FLIGHT PICK ({origin} ➔ {destination})</span>
            <h3>{best_flight['Airline']} — ₹{best_flight['True Checkout Total (₹)']} True Checkout Total</h3>
            <p><b>Route:</b> {best_flight['Stops']} ({best_flight['Duration']}) | <b>On-Time Score:</b> {best_flight['On-Time Score']} | <b>Taxes, Convenience & Add-on Fees Included:</b> ₹{hidden_fees}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Side-by-Side True Checkout Comparison (No Hidden Gateway Surprises)")
        st.dataframe(
            df_flights[[
                "Rank", "Airline", "Stops", "Duration", "Base Ticket (₹)", 
                "Airport & Fuel Tax (₹)", "OTA Convenience Fee (₹)", 
                "Seat & Baggage Add-on (₹)", "True Checkout Total (₹)", "On-Time Score"
            ]],
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        col_fl1, col_fl2 = st.columns(2)
        with col_fl1:
            st.markdown("#### 🧭 Weather & Wind Turbulence Advisory")
            if weather != "Clear":
                st.warning(
                    f"**{weather}** reported on the **{origin} ➔ {destination}** corridor. "
                    "Full-service carriers (**Vistara**, **Air India**) have higher schedule recovery buffers than low-cost carriers."
                )
            else:
                st.success(
                    f"Clear skies on the **{origin} ➔ {destination}** corridor. Low delay risk across all carriers."
                )
        with col_fl2:
            st.markdown("#### 💡 Zero-Convenience-Fee Tip")
            st.info(
                f"Booking directly on **{best_flight['Airline']}**'s app using UPI waives **₹{best_flight['OTA Convenience Fee (₹)']}** in third-party OTA gateway fees."
            )

# ==============================================================================
# MODE 4: SHOPPING & APPAREL (BRAND, CATEGORY & COLOUR COMPARATOR)
# ==============================================================================
elif "Shopping" in domain:
    st.subheader("🛍️ Apparel & Brand True-Price Navigator")
    
    brands_list = [
        "Van huesen", "Manyavar", "HnM", "Zara", "Mango", "Beromoda", 
        "M&S", "Levi's", "Only", "Mohanlal &Sons", "Mohey", "W"
    ]
    clothes_categories = [
        "Kurtas", "Jackets", "lowers", "t shirts", "polos", "shirts", "innerwear"
    ]
    colours_list = ["dark", "light", "vibrant"]
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        selected_categories = st.multiselect(
            "Clothing Categories (one or more):",
            options=clothes_categories,
            default=["Kurtas", "shirts"]
        )
    with col_s2:
        selected_colours = st.multiselect(
            "Colour Palette:",
            options=colours_list,
            default=["dark", "vibrant"]
        )
    with col_s3:
        selected_brands = st.multiselect(
            "Filter Brands (leave empty for all 12):",
            options=brands_list,
            default=[]
        )

    if not selected_categories:
        st.info("👆 Select at least one clothing category above to compare all-in prices across brands and channels.")
    else:
        active_brands = selected_brands if selected_brands else brands_list
        active_colours = selected_colours if selected_colours else colours_list

        cat_base = {
            "Kurtas": 1800,
            "Jackets": 3200,
            "lowers": 1500,
            "t shirts": 900,
            "polos": 1350,
            "shirts": 1750,
            "innerwear": 600
        }

        brand_profiles = {
            "Van huesen": {"mult": 1.15, "specialty": {"shirts", "polos", "Jackets", "innerwear"}, "channel": "Brand App / Mall Store", "local": False, "delivery": 0, "platform_fee": 29, "discount": 0.15, "eta": 45},
            "Manyavar": {"mult": 1.45, "specialty": {"Kurtas", "Jackets", "lowers"}, "channel": "Flagship / Myntra", "local": False, "delivery": 0, "platform_fee": 39, "discount": 0.10, "eta": 60},
            "HnM": {"mult": 1.05, "specialty": {"t shirts", "Jackets", "lowers", "shirts", "innerwear"}, "channel": "HnM App", "local": False, "delivery": 149, "platform_fee": 20, "discount": 0.12, "eta": 90},
            "Zara": {"mult": 1.55, "specialty": {"Jackets", "shirts", "lowers", "t shirts"}, "channel": "Zara Store / App", "local": False, "delivery": 290, "platform_fee": 0, "discount": 0.05, "eta": 120},
            "Mango": {"mult": 1.45, "specialty": {"Jackets", "shirts", "lowers", "t shirts"}, "channel": "Myntra / Ajio", "local": False, "delivery": 99, "platform_fee": 29, "discount": 0.15, "eta": 90},
            "Beromoda": {"mult": 1.00, "specialty": {"t shirts", "lowers", "Jackets", "shirts"}, "channel": "Ajio / Brand Site", "local": False, "delivery": 79, "platform_fee": 19, "discount": 0.20, "eta": 120},
            "M&S": {"mult": 1.35, "specialty": {"shirts", "polos", "innerwear", "lowers", "Jackets"}, "channel": "M&S App / In-Store", "local": False, "delivery": 99, "platform_fee": 20, "discount": 0.15, "eta": 60},
            "Levi's": {"mult": 1.25, "specialty": {"lowers", "t shirts", "Jackets", "shirts"}, "channel": "Levi's Store / Ajio", "local": False, "delivery": 0, "platform_fee": 29, "discount": 0.18, "eta": 60},
            "Only": {"mult": 1.10, "specialty": {"Jackets", "t shirts", "lowers", "shirts"}, "channel": "Myntra / Only App", "local": False, "delivery": 79, "platform_fee": 25, "discount": 0.20, "eta": 90},
            "Mohanlal &Sons": {"mult": 1.10, "specialty": {"Kurtas", "Jackets", "shirts", "lowers"}, "channel": "Local Heritage Store", "local": True, "delivery": 0, "platform_fee": 0, "discount": 0.12, "eta": 30},
            "Mohey": {"mult": 1.50, "specialty": {"Kurtas", "Jackets", "lowers"}, "channel": "Mohey Store / Manyavar", "local": False, "delivery": 0, "platform_fee": 39, "discount": 0.10, "eta": 60},
            "W": {"mult": 1.12, "specialty": {"Kurtas", "lowers", "Jackets"}, "channel": "W Store / Ajio", "local": True, "delivery": 49, "platform_fee": 19, "discount": 0.22, "eta": 45},
        }

        colour_mult = {"dark": 1.00, "light": 0.98, "vibrant": 1.04}
        avg_colour_mult = sum(colour_mult[c] for c in active_colours) / len(active_colours)

        apparel_rows = []
        for brand in active_brands:
            prof = brand_profiles[brand]
            raw_mrp = sum(cat_base[cat] * prof["mult"] * avg_colour_mult for cat in selected_categories)
            effective_discount_rate = prof["discount"] * (0.75 if demand == "Peak Rush / Festival" else 1.15 if demand == "Off-Peak" else 1.0)
            discount_amt = -int(raw_mrp * effective_discount_rate)
            shipping_fee = 0 if prof["local"] else int(prof["delivery"] * weather_mult)
            platform_fee = prof["platform_fee"]
            matched_cats = len(set(selected_categories) & prof["specialty"])
            match_label = f"{matched_cats}/{len(selected_categories)} Specialty Match"

            apparel_rows.append({
                "Brand": brand,
                "Best Channel": prof["channel"],
                "Category Match": match_label,
                "Colours": ", ".join(active_colours),
                "MRP Subtotal (₹)": int(raw_mrp),
                "Brand/Season Discount (₹)": discount_amt,
                "Shipping & Convenience Fee (₹)": shipping_fee + platform_fee,
                "Final Checkout Total (₹)": int(raw_mrp) + discount_amt + shipping_fee + platform_fee,
                "Delivery / Pickup (mins)": prof["eta"],
                "Is Local": prof["local"]
            })

        df_shop = pd.DataFrame(apparel_rows)

        if "Lowest Final Price" in priority:
            df_shop = df_shop.sort_values(by="Final Checkout Total (₹)", ascending=True)
        elif "Fastest" in priority:
            df_shop = df_shop.sort_values(by="Delivery / Pickup (mins)", ascending=True)
        else:
            local_df = df_shop[df_shop["Is Local"]]
            df_shop = (local_df if not local_df.empty else df_shop).sort_values(by="Final Checkout Total (₹)", ascending=True)

        df_shop.insert(0, "Rank", [f"#{i+1}" for i in range(len(df_shop))])

        best_shop = df_shop.iloc[0]
        max_shop_total = df_shop["Final Checkout Total (₹)"].max()
        shop_savings = max_shop_total - best_shop["Final Checkout Total (₹)"]

        st.markdown(f"""
        <div class="metric-card">
            <span class="best-badge">★ #1 PENNYWISE APPAREL PICK ({', '.join(selected_categories).upper()})</span>
            <h3>{best_shop['Brand']} — ₹{best_shop['Final Checkout Total (₹)']} All-In ({best_shop['Best Channel']})</h3>
            <p><b>Colours:</b> {best_shop['Colours']} | <b>Match:</b> {best_shop['Category Match']} | <b>Hidden Shipping/Platform Fees:</b> ₹{best_shop['Shipping & Convenience Fee (₹)']} | <b>You Save:</b> ₹{shop_savings} vs highest brand</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Ranked Brands by Collective Checkout Total")
        st.dataframe(
            df_shop[[
                "Rank", "Brand", "Best Channel", "Category Match", "Colours",
                "MRP Subtotal (₹)", "Brand/Season Discount (₹)", 
                "Shipping & Convenience Fee (₹)", "Final Checkout Total (₹)", 
                "Delivery / Pickup (mins)"
            ]],
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        col_sh1, col_sh2 = st.columns(2)
        with col_sh1:
            st.markdown("#### 👻 Ghost-Cart Wardrobe Split")
            st.info(
                "**Multi-Brand Insight:** Buying ethnic **Kurtas** from **Mohanlal &Sons** (zero shipping/platform fee) "
                "and casual **t shirts / lowers** from **Beromoda** or **HnM** avoids high-MRP markups."
            )
        with col_sh2:
            st.markdown("#### 🏪 In-Store vs. App Fee Alert")
            st.info(
                f"Brands like **Zara** and **HnM** add up to **₹149–₹290** in delivery fees on smaller carts. "
                f"Switching sidebar priority to **Local / In-Person Option** highlights walk-in stores with **₹0** shipping."
            )

# ==============================================================================
# MODE 5: HOTELS & STAYS (ROOM TYPE, BELL-BOY & MEAL PLAN NAVIGATOR)
# ==============================================================================
else:
    st.subheader("🏨 Hotels & Stays All-In Checkout Navigator")
    
    room_types = [
        "Suite", "junior suite", "deluxe", "double bed", 
        "king bed", "queen bed", "single bed"
    ]
    meal_options = ["Breakfast", "Lunch", "Dinner"]
    
    col_h1, col_h2, col_h3 = st.columns([2, 2, 1.5])
    with col_h1:
        selected_room = st.selectbox("Select Room Type:", room_types, index=2)  # Default: deluxe
    with col_h2:
        selected_meals = st.multiselect(
            "Include Meals (per night):",
            options=meal_options,
            default=["Breakfast"]
        )
    with col_h3:
        nights = st.number_input("Nights", min_value=1, max_value=14, value=1)
        include_bellboy = st.checkbox("Include Bell-Boy Service", value=True)

    # Room tier multipliers
    room_mult = {
        "Suite": 2.40,
        "junior suite": 1.85,
        "deluxe": 1.35,
        "king bed": 1.25,
        "queen bed": 1.15,
        "double bed": 1.05,
        "single bed": 0.80
    }[selected_room]

    # Hotels list: Taj, Radison, Oyo + 3 well-known local Secunderabad hotels
    hotels_catalog = [
        {
            "Hotel": "Taj (Taj Tristar / Taj Krishna)",
            "Category": "5-Star Luxury",
            "Is Local": False,
            "base_nightly": 6200,
            "bellboy_fee": 0,  # Complimentary at Taj
            "meal_rates": {"Breakfast": 650, "Lunch": 1100, "Dinner": 1300},
            "ota_fee": 450,
            "gst_rate": 0.18,
            "Check-in ETA (mins)": 15,
            "Guest Rating": "4.8 ★"
        },
        {
            "Hotel": "Radison (Radisson Blu / Plaza)",
            "Category": "Upscale Chain",
            "Is Local": False,
            "base_nightly": 4800,
            "bellboy_fee": 150,
            "meal_rates": {"Breakfast": 500, "Lunch": 850, "Dinner": 950},
            "ota_fee": 380,
            "gst_rate": 0.18,
            "Check-in ETA (mins)": 15,
            "Guest Rating": "4.6 ★"
        },
        {
            "Hotel": "Minerva Grand Secunderabad (S.D. Road)",
            "Category": "Local Secunderabad Hotel",
            "Is Local": True,
            "base_nightly": 3400,
            "bellboy_fee": 100,
            "meal_rates": {"Breakfast": 280, "Lunch": 450, "Dinner": 500},
            "ota_fee": 0,  # Direct local booking
            "gst_rate": 0.12,
            "Check-in ETA (mins)": 10,
            "Guest Rating": "4.4 ★"
        },
        {
            "Hotel": "Hotel Suprabhat Residency (Secunderabad Station)",
            "Category": "Local Secunderabad Hotel",
            "Is Local": True,
            "base_nightly": 1850,
            "bellboy_fee": 80,
            "meal_rates": {"Breakfast": 150, "Lunch": 250, "Dinner": 280},
            "ota_fee": 0,
            "gst_rate": 0.12,
            "Check-in ETA (mins)": 8,
            "Guest Rating": "4.1 ★"
        },
        {
            "Hotel": "Hotel Baseraa (S.D. Road, Secunderabad)",
            "Category": "Local Secunderabad Hotel",
            "Is Local": True,
            "base_nightly": 2750,
            "bellboy_fee": 100,
            "meal_rates": {"Breakfast": 220, "Lunch": 380, "Dinner": 420},
            "ota_fee": 0,
            "gst_rate": 0.12,
            "Check-in ETA (mins)": 10,
            "Guest Rating": "4.3 ★"
        },
        {
            "Hotel": "Oyo (Super Townhouse Secunderabad)",
            "Category": "Budget Aggregator",
            "Is Local": False,
            "base_nightly": 1250,
            "bellboy_fee": 120,
            "meal_rates": {"Breakfast": 140, "Lunch": 220, "Dinner": 240},
            "ota_fee": 199,
            "gst_rate": 0.12,
            "Check-in ETA (mins)": 20,
            "Guest Rating": "3.8 ★"
        }
    ]

    hotel_rows = []
    for h in hotels_catalog:
        room_cost = int(h["base_nightly"] * room_mult * total_mult) * nights
        bellboy_cost = (h["bellboy_fee"] * nights) if include_bellboy else 0
        meals_cost = sum(h["meal_rates"][m] for m in selected_meals) * nights
        subtotal = room_cost + bellboy_cost + meals_cost
        taxes_and_ota = int(subtotal * h["gst_rate"]) + h["ota_fee"]
        final_total = subtotal + taxes_and_ota

        hotel_rows.append({
            "Hotel": h["Hotel"],
            "Category": h["Category"],
            "Room Type": selected_room,
            f"Room Base ({nights}N) (₹)": room_cost,
            "Bell-Boy Fee (₹)": bellboy_cost,
            f"Meals ({len(selected_meals)}/day) (₹)": meals_cost,
            "GST & OTA Fees (₹)": taxes_and_ota,
            "Final Checkout Total (₹)": final_total,
            "Check-in ETA (mins)": h["Check-in ETA (mins)"],
            "Rating": h["Guest Rating"],
            "Is Local": h["Is Local"]
        })

    df_hotels = pd.DataFrame(hotel_rows)

    if "Lowest Final Price" in priority:
        df_hotels = df_hotels.sort_values(by="Final Checkout Total (₹)", ascending=True)
    elif "Fastest" in priority:
        df_hotels = df_hotels.sort_values(by="Check-in ETA (mins)", ascending=True)
    else:
        df_hotels = df_hotels[df_hotels["Is Local"]].sort_values(by="Final Checkout Total (₹)", ascending=True)

    df_hotels.insert(0, "Rank", [f"#{i+1}" for i in range(len(df_hotels))])

    best_hotel = df_hotels.iloc[0]
    max_hotel_total = df_hotels["Final Checkout Total (₹)"].max()
    hotel_savings = max_hotel_total - best_hotel["Final Checkout Total (₹)"]
    meals_summary = ", ".join(selected_meals) if selected_meals else "Room Only (No Meals)"

    st.markdown(f"""
    <div class="metric-card">
        <span class="best-badge">★ #1 PENNYWISE STAY PICK ({selected_room.upper()} | {nights} NIGHT{'S' if nights > 1 else ''})</span>
        <h3>{best_hotel['Hotel']} — ₹{best_hotel['Final Checkout Total (₹)']} All-In</h3>
        <p><b>Room:</b> {selected_room} | <b>Meals:</b> {meals_summary} | <b>Bell-Boy:</b> {'Included' if include_bellboy else 'Not Included'} | <b>Taxes & Fees Included:</b> ₹{best_hotel['GST & OTA Fees (₹)']} | <b>You Save:</b> ₹{hotel_savings} vs highest option</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Side-by-Side Hotel True Checkout Breakdown")
    st.dataframe(
        df_hotels[[
            "Rank", "Hotel", "Category", "Room Type",
            f"Room Base ({nights}N) (₹)", "Bell-Boy Fee (₹)",
            f"Meals ({len(selected_meals)}/day) (₹)", "GST & OTA Fees (₹)",
            "Final Checkout Total (₹)", "Rating"
        ]],
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    col_ht1, col_ht2 = st.columns(2)
    with col_ht1:
        st.markdown("#### 🛎️ Service & Add-On Transparency")
        st.info(
            "**Hidden Fee Insight:** Luxury chains like **Taj** include complimentary bell-boy service in the room tariff, "
            "whereas budget aggregators like **Oyo** add separate service & OTA convenience fees at checkout."
        )
    with col_ht2:
        st.markdown("#### 🍽️ Meal-Plan vs. Local Dining Tip")
        st.info(
            "Adding all 3 meals (**Breakfast, Lunch, Dinner**) at **Taj** or **Radison** adds **₹2,300–₹3,050/night**. "
            "Booking **Minerva Grand** or **Hotel Baseraa** on S.D. Road gives you iconic Secunderabad dining at a fraction of the cost."
        )