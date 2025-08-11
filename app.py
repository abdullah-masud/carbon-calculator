import streamlit as st
import pandas as pd
import altair as alt
import factors as fx

st.set_page_config(page_title="Personal Carbon Calculator", layout="centered")
st.title("Personal Carbon Footprint Calculator")
st.write("Estimate your annual CO₂ emissions from electricity, natural gas, car travel, and flights.")

# ---- Sidebar inputs ----
with st.sidebar:
    st.header("Inputs (annual)")
    electricity_kwh = st.number_input("Electricity (kWh)", min_value=0.0, value=3000.0, step=100.0)
    gas_kwh        = st.number_input("Natural gas (kWh)", min_value=0.0, value=1000.0, step=50.0)
    car_km         = st.number_input("Car travel (km)",   min_value=0.0, value=12000.0, step=100.0)
    flight_km      = st.number_input("Air travel (km)",   min_value=0.0, value=3000.0, step=100.0)

    st.divider()
    st.subheader("Emission factor presets")
    preset = st.selectbox(
        "Choose a preset",
        ["Baseline (default)", "Low-carbon grid example", "Custom (enter values)"],
        help="Presets set the factors below. Choose Custom to type your own."
    )

    # Defaults from factors.py
    elec_factor  = fx.ELECTRICITY_KG_PER_KWH
    gas_factor   = fx.GAS_KG_PER_KWH
    car_factor   = fx.CAR_KG_PER_KM
    flight_factor= fx.FLIGHT_KG_PER_KM

    # Apply preset
    if preset == "Low-carbon grid example":
        # Example: hypothetical cleaner electricity grid
        elec_factor = 0.20  # kg CO2/kWh (example only)
    # Baseline keeps defaults from factors.py

    # Allow manual override only when Custom chosen
    st.subheader("Advanced (optional)")
    if preset == "Custom (enter values)":
        elec_factor  = st.number_input("Electricity factor (kg CO₂/kWh)", min_value=0.0, value=elec_factor, step=0.01)
        gas_factor   = st.number_input("Gas factor (kg CO₂/kWh)",         min_value=0.0, value=gas_factor, step=0.01)
        car_factor   = st.number_input("Car factor (kg CO₂/km)",          min_value=0.0, value=car_factor, step=0.01)
        flight_factor= st.number_input("Flight factor (kg CO₂/km)",       min_value=0.0, value=flight_factor, step=0.01)
    else:
        st.caption("Preset active. Switch to **Custom** to edit the numbers manually.")


    submitted = st.button("Calculate")


def compute_emissions(electricity_kwh, gas_kwh, car_km, flight_km, factors_dict):
    data = {
        "Electricity": electricity_kwh * factors_dict["electricity"],
        "Natural Gas": gas_kwh        * factors_dict["gas"],
        "Car Travel":  car_km         * factors_dict["car"],
        "Flights":     flight_km      * factors_dict["flight"],
    }
    df = pd.DataFrame({"Category": list(data.keys()),
                       "Emissions (kg CO₂)": list(data.values())})
    return df, float(df["Emissions (kg CO₂)"].sum())

if submitted:
    df, total_kg = compute_emissions(
        electricity_kwh, gas_kwh, car_km, flight_km,
        {"electricity": elec_factor, "gas": gas_factor, "car": car_factor, "flight": flight_factor}
    )
    total_t = total_kg / 1000.0

    st.header("Your Results")
    st.metric("Total emissions", f"{total_t:,.2f} t CO₂e")

    au = fx.AU_PER_CAPITA_TONNES
    world = fx.WORLD_PER_CAPITA_TONNES
    st.write(f"Compared to **Australia** average ({au:.2f} t): **{100*total_t/au:.1f}%**")
    st.write(f"Compared to **Global** average ({world:.2f} t): **{100*total_t/world:.1f}%**")

    # verdict (from previous step)
    if total_t < (0.75 * fx.WORLD_PER_CAPITA_TONNES):
        st.success("🌱 Low footprint — You’re well below the world average. Keep it up!")
    elif total_t <= fx.WORLD_PER_CAPITA_TONNES:
        st.info("🙂 Average footprint — Around the world average. Small changes can make you a low emitter.")
    else:
        st.error("⚠ High footprint — Above the world average. Consider reducing your biggest emission sources.")

    # Chart
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Category", title=None),
        y=alt.Y("Emissions (kg CO₂)", title="kg CO₂"),
        color=alt.Color("Category", legend=None),
        tooltip=["Category", alt.Tooltip("Emissions (kg CO₂)", format=",.1f")]
    ).properties(title="Emissions by category")
    st.altair_chart(chart, use_container_width=True)

    # Table
    st.subheader("Breakdown")
    st.dataframe(df.style.format({"Emissions (kg CO₂)": "{:,.1f}"}))

    # Export CSV
    st.subheader("Export")
    csv_df = df.copy()
    csv_df.loc[len(csv_df)] = ["TOTAL", total_kg]
    st.download_button(
        "⬇️ Download results (CSV)",
        data=csv_df.to_csv(index=False).encode("utf-8"),
        file_name="carbon_footprint_results.csv",
        mime="text/csv",
    )

st.caption("Note: Factors are generic baselines; real intensity varies by region and year. Use Advanced to adjust.")
