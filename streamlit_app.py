import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Vermischung Mantel Krusten Reservoir", page_icon="🪨", layout="wide")

CRUST_COLOR = "#A52A2A"
MANTLE_COLOR = "#006400"
MIX_COLOR = "#1E90FF"

ROCK_COMPOSITIONS = {
    "Basalt": {"SiO2": 48.0, "MgO": 8.0},
    "Andesit": {"SiO2": 58.0, "MgO": 3.0},
    "Dazit": {"SiO2": 65.0, "MgO": 2.0},
    "Rhyolith": {"SiO2": 75.0, "MgO": 0.5},
}

PLUTONIC_REFERENCE_ROCKS = {
    "Peridotit": {"SiO2": 42.0, "MgO": 40.0, "color": "#7A3E1A"},
    "Gabbro": {"SiO2": 50.0, "MgO": 8.0, "color": "#B5651D"},
    "Diorit": {"SiO2": 57.0, "MgO": 4.0, "color": "#D4A017"},
    "Granodiorit": {"SiO2": 66.0, "MgO": 2.5, "color": "#6A8E23"},
    "Granit": {"SiO2": 73.0, "MgO": 0.8, "color": "#C0C0C0"},
}


def calculate_mixing(f_crust, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo):
    f_mantle = 1 - f_crust
    mixed_sio2 = f_crust * crust_sio2 + f_mantle * mantle_sio2
    mixed_mgo = f_crust * crust_mgo + f_mantle * mantle_mgo
    return mixed_sio2, mixed_mgo


def find_closest_rock_type(mixed_sio2, mixed_mgo):
    best_name = None
    best_distance = float("inf")
    for rock_name, comp in ROCK_COMPOSITIONS.items():
        distance = np.sqrt((mixed_sio2 - comp["SiO2"]) ** 2 + (mixed_mgo - comp["MgO"]) ** 2)
        if distance < best_distance:
            best_distance = distance
            best_name = rock_name
    return best_name, best_distance


def find_closest_plutonic_rock(mixed_sio2, mixed_mgo):
    best_name = None
    best_distance = float("inf")
    for rock_name, comp in PLUTONIC_REFERENCE_ROCKS.items():
        distance = np.sqrt((mixed_sio2 - comp["SiO2"]) ** 2 + (mixed_mgo - comp["MgO"]) ** 2)
        if distance < best_distance:
            best_distance = distance
            best_name = rock_name
    return best_name, best_distance


def create_line_plot(f_crust, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo):
    f_values = np.linspace(0, 1, 120)
    sio2_curve = []
    mgo_curve = []
    for value in f_values:
        sio2, mgo = calculate_mixing(value, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo)
        sio2_curve.append(sio2)
        mgo_curve.append(mgo)

    mixed_sio2, mixed_mgo = calculate_mixing(f_crust, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(f_values * 100, sio2_curve, color=MIX_COLOR, linewidth=2, label="SiO2")
    ax.plot(f_values * 100, mgo_curve, color=CRUST_COLOR, linewidth=2, linestyle="--", label="MgO")
    ax.scatter([f_crust * 100], [mixed_sio2], s=60, color=MIX_COLOR, label="Aktueller SiO2-Wert", zorder=5)
    ax.scatter([f_crust * 100], [mixed_mgo], s=60, color=CRUST_COLOR, label="Aktueller MgO-Wert", zorder=5)
    ax.set_title("Mischungskurven: SiO2 und MgO gegen Krustenanteil")
    ax.set_xlabel("Krustenanteil (%)")
    ax.set_ylabel("Konzentration (Gew. %)")
    ax.legend()
    fig.tight_layout()
    return fig


def create_bar_plot(crust_sio2, crust_mgo, mantle_sio2, mantle_mgo, mixed_sio2, mixed_mgo):
    categories = ["SiO2", "MgO"]
    crust_vals = [crust_sio2, crust_mgo]
    mantle_vals = [mantle_sio2, mantle_mgo]
    mix_vals = [mixed_sio2, mixed_mgo]

    x = np.arange(len(categories))
    width = 0.25
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(x - width, crust_vals, width, label="Kruste", color=CRUST_COLOR)
    ax.bar(x, mantle_vals, width, label="Mantel", color=MANTLE_COLOR)
    ax.bar(x + width, mix_vals, width, label="Mischung", color=MIX_COLOR)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_title("Vergleich der Reservoir-Zusammensetzungen")
    ax.set_xlabel("Komponente")
    ax.set_ylabel("Konzentration (Gew. %)")
    ax.legend()
    fig.tight_layout()
    return fig


def create_ratio_plot(f_crust, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo):
    f_values = np.linspace(0, 1, 120)
    sio2_line = []
    mgo_line = []
    mg_si_line = []
    for value in f_values:
        sio2, mgo = calculate_mixing(value, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo)
        sio2_line.append(sio2)
        mgo_line.append(mgo)
        mg_si_line.append(mgo / sio2 if sio2 else float("nan"))

    mixed_sio2, mixed_mgo = calculate_mixing(f_crust, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo)
    mixed_ratio = mixed_mgo / mixed_sio2 if mixed_sio2 else float("nan")
    
    closest_plutonic_rock, _ = find_closest_plutonic_rock(mixed_sio2, mixed_mgo)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(mg_si_line, mgo_line, color="gray", linestyle=":", label="Mischungslinie")
    ax.scatter([mixed_ratio], [mixed_mgo], s=500, color=(30/255,144/255,255/255,0.15), zorder=2)
    ax.scatter([mixed_ratio], [mixed_mgo], s=80, color=MIX_COLOR, edgecolors="white", linewidths=1.5, zorder=3, label="Aktuelle Mischung")
    ax.scatter([mantle_mgo / mantle_sio2 if mantle_sio2 else float("nan")], [mantle_mgo], s=60, color=MANTLE_COLOR, label="Mantel")
    ax.scatter([crust_mgo / crust_sio2 if crust_sio2 else float("nan")], [crust_mgo], s=60, color=CRUST_COLOR, label="Kruste")

    for rock_name, comp in PLUTONIC_REFERENCE_ROCKS.items():
        is_closest = rock_name == closest_plutonic_rock and rock_name != "Peridotit"
        size = 120 if is_closest else 60
        edge = "yellow" if is_closest else "black"
        ax.scatter([comp["MgO"] / comp["SiO2"] if comp["SiO2"] else float("nan")], [comp["MgO"]], s=size, color=comp["color"], edgecolors=edge, linewidths=1.2, zorder=4)

    ax.set_title("MgO gegen Mg/Si-Verhältnis")
    ax.set_xlabel("Mg/Si-Verhältnis")
    ax.set_ylabel("MgO (Gew. %)")
    ax.legend()
    fig.tight_layout()
    return fig


def create_mg_si_plot(f_crust, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo):
    f_values = np.linspace(0, 1, 120)
    si_values = []
    mg_values = []
    for value in f_values:
        sio2, mgo = calculate_mixing(value, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo)
        si_values.append(sio2)
        mg_values.append(mgo)

    mixed_sio2, mixed_mgo = calculate_mixing(f_crust, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo)
    
    closest_plutonic_rock, _ = find_closest_plutonic_rock(mixed_sio2, mixed_mgo)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(si_values, mg_values, color="gray", linestyle=":", label="Mischungslinie")
    ax.scatter([mantle_sio2], [mantle_mgo], s=80, color=MANTLE_COLOR, label="Mantel")
    ax.scatter([crust_sio2], [crust_mgo], s=80, color=CRUST_COLOR, label="Kruste")
    ax.scatter([mixed_sio2], [mixed_mgo], s=500, color=(30/255,144/255,255/255,0.15), zorder=2)
    ax.scatter([mixed_sio2], [mixed_mgo], s=100, color=MIX_COLOR, edgecolors="white", linewidths=1.5, zorder=3, label="Aktuelle Mischung")

    for rock_name, comp in PLUTONIC_REFERENCE_ROCKS.items():
        is_closest = rock_name == closest_plutonic_rock and rock_name != "Peridotit"
        size = 120 if is_closest else 60
        edge = "yellow" if is_closest else "black"
        ax.scatter([comp["SiO2"]], [comp["MgO"]], s=size, color=comp["color"], edgecolors=edge, linewidths=1.2, zorder=4)

    ax.set_title("Mg gegen Si")
    ax.set_xlabel("Si (Gew. %)")
    ax.set_ylabel("Mg (Gew. %)")
    ax.legend()
    fig.tight_layout()
    return fig


st.title("Vermischung Mantel Krusten Reservoir")
st.write("Diese App zeigt, wie sich die Zusammensetzung einer Mischung aus Kruste und Mantel mit den Schiebereglern verändert.")

with st.sidebar:
    st.header("Eingaben")
    f_crust = st.slider("Krustenanteil (%)", 0, 100, 0) / 100
    crust_sio2 = st.slider("Kruste: SiO2 (Gew. %)", 40.0, 80.0, 75.0, 0.1)
    crust_mgo = st.slider("Kruste: MgO (Gew. %)", 0.5, 10.0, 0.5, 0.1)
    mantle_sio2 = st.slider("Mantel: SiO2 (Gew. %)", 35.0, 55.0, 35.0, 0.1)
    mantle_mgo = st.slider("Mantel: MgO (Gew. %)", 20.0, 50.0, 50.0, 0.1)

mixed_sio2, mixed_mgo = calculate_mixing(f_crust, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo)
closest_rock, distance = find_closest_rock_type(mixed_sio2, mixed_mgo)
closest_plutonic_rock, plutonic_distance = find_closest_plutonic_rock(mixed_sio2, mixed_mgo)
mg_si_ratio = mixed_mgo / mixed_sio2 if mixed_sio2 else float("nan")

col1, col2, col3 = st.columns(3)
col1.metric("Krustenanteil", f"{f_crust * 100:.0f}%")
col2.metric("Gemischtes SiO2", f"{mixed_sio2:.2f} Gew.%")
col3.metric("Mg/Si-Verhältnis", f"{mg_si_ratio:.3f}")

st.caption(f"Die aktuelle Mischung ähnelt am ehesten {closest_rock} (Abstand: {distance:.2f}).")
st.info(f"Bei diesen Mischwerten entsteht im Reservoir am ehesten {closest_plutonic_rock} (Abstand zu den Referenzpunkten: {plutonic_distance:.2f}).")

st.subheader("1. Mischungskurven")
st.pyplot(create_line_plot(f_crust, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo))
st.write("**Geologische Bedeutung:** Die Mischungskurven zeigen, wie sich die Elementkonzentrationen linear zwischen reinem Mantel (0%) und reiner Kruste (100%) ändern. Dies ist das Grundprinzip der Magmenmischung: Wenn krustenähnliches und mantelähnliches Material vermischt werden, entsteht eine neue Zusammensetzung auf der geraden Linie zwischen den Endgliedern.")

st.subheader("2. Vergleich der Reservoir-Zusammensetzungen")
st.pyplot(create_bar_plot(crust_sio2, crust_mgo, mantle_sio2, mantle_mgo, mixed_sio2, mixed_mgo))
st.write("**Geologische Bedeutung:** Der Vergleich zeigt deutlich die chemischen Unterschiede zwischen Kruste und Mantel. Die Kruste ist SiO₂-reich (felsisch, leicht) und MgO-arm, während der Mantel umgekehrt zusammengesetzt ist (mafisch, schwer). Bei einer Mischung erzeugt der unterschiedliche Gehalt an diesen Oxiden ein neues Material mit Zwischeneigenschaften.")

st.subheader("3. MgO gegen Mg/Si-Verhältnis")
st.pyplot(create_ratio_plot(f_crust, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo))
st.write("**Geologische Bedeutung:** Das Mg/Si-Verhältnis ist ein wichtiger geochemischer Index: Höhere Werte deuten auf mafische (magnesiumreiche) Magmen hin, die aus dem Mantel stammen, während niedrige Werte felsische (kieselsäurereichere) Magmen anzeigen. Die Mischungslinie zeigt, wie dieser Index bei der Vermischung von Kruste und Mantel variiert.")

st.subheader("4. Mg gegen Si")
st.pyplot(create_mg_si_plot(f_crust, crust_sio2, crust_mgo, mantle_sio2, mantle_mgo))
st.write("**Geologische Bedeutung:** Dies ist das klassische geochemische Diagramm für Magmenherkunft. Die Position eines Magmas zwischen den Endgliedern (Kruste und Mantel) zeigt seinen Ursprung oder seine Mischungsgeschichte. Je näher die Mischung zum Mantel-Punkt, desto magnesiumreicher und primitiver ist das Magma; je näher zur Kruste, desto differenzierter und felsischer ist es.")
