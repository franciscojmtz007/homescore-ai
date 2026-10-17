import streamlit as st

from translations.en import TEXT as EN
from translations.es import TEXT as ES

from src.demo_data import DEMO_HOMES
from src.engine import calculate_home_result
from src.ranking import group_and_rank_homes
from src.validation import validate_buyer, validate_home

# ============================================
# Validation Message Translations
# ============================================

VALIDATION_TRANSLATIONS = {
    "Property name cannot be empty.":
        "El nombre de la vivienda no puede estar vacío.",

    "Property square footage must be greater than zero.":
        "La superficie de la vivienda debe ser mayor que cero.",

    "Down payment cannot exceed the home's price.":
        "El pago inicial no puede superar el precio de la vivienda.",

    "Maximum home price must be greater than target price.":
        "El precio máximo debe ser mayor que el precio objetivo.",

    "Target square footage must be greater than minimum square footage.":
        "La superficie objetivo debe ser mayor que la superficie mínima.",
}


def translate_validation_message(message, language):
    if language == "English":
        return message

    return VALIDATION_TRANSLATIONS.get(message, message)

def translate_violation(message, text):
    """Translate a scoring-engine violation for display."""

    violation_keys = {
        "Price exceeds maximum": "violation_price",
        "Commute exceeds maximum": "violation_commute",
        "Below minimum size": "violation_size",
        "Missing Garage": "violation_garage",
        "Missing Home Office": "violation_home_office",
    }

    key = violation_keys.get(message)

    if key is None:
        return message

    return text.get(key, message)

# Configure the application
st.set_page_config(
    page_title="HomeScore AI",
    page_icon="🏠",
    layout="wide",
)

def show_score_explanation(home, text, buyer):
    """Display the HomeScore breakdown and requirement warnings."""

    st.markdown(f"### {text['score_breakdown']}")

    # -----------------------------------------
    # Overall dimension scores
    # -----------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            text["affordability_score"],
            f"{home['affordability_fit']:.1f}",
        )

    with col2:
        st.metric(
            text["location_score"],
            f"{home['location_fit']:.1f}",
        )

    with col3:
        st.metric(
            text["property_score"],
            f"{home['property_fit']:.1f}",
        )

    # -----------------------------------------
    # Normalized weights
    # -----------------------------------------

    st.markdown(f"### {text['your_priorities']}")

    affordability_importance = buyer["affordability_importance"]
    location_importance = buyer["location_importance"]
    property_importance = buyer["property_importance"]

    total_importance = (
        affordability_importance
        + location_importance
        + property_importance
    )

    if total_importance > 0:
        affordability_weight = affordability_importance / total_importance
        location_weight = location_importance / total_importance
        property_weight = property_importance / total_importance
    else:
        affordability_weight = 0
        location_weight = 0
        property_weight = 0

    st.write(
        f"**{text['affordability_score']}** — "
        f"{text['importance_rating']}: {affordability_importance}/5 | "
        f"{text['weight_percentage']}: {affordability_weight:.1%}"
    )

    st.write(
        f"**{text['location_score']}** — "
        f"{text['importance_rating']}: {location_importance}/5 | "
        f"{text['weight_percentage']}: {location_weight:.1%}"
    )

    st.write(
        f"**{text['property_score']}** — "
        f"{text['importance_rating']}: {property_importance}/5 | "
        f"{text['weight_percentage']}: {property_weight:.1%}"
    )

    # -----------------------------------------
    # Final calculation
    # -----------------------------------------

    st.markdown(f"### {text['final_calculation']}")

    st.code(
        f"({home['affordability_fit']:.2f} × {affordability_weight:.2%}) +\n"
        f"({home['location_fit']:.2f} × {location_weight:.2%}) +\n"
        f"({home['property_fit']:.2f} × {property_weight:.2%})\n"
        f"= {home['homescore']:.2f}"
    )

    st.divider()

    # -----------------------------------------
    # Affordability details
    # -----------------------------------------

    st.markdown(f"**{text['affordability_score']}**")

    st.write(
        f"{text['price_fit_label']}: "
        f"{home['price_fit']:.1f}"
    )

    st.write(
        f"{text['monthly_fit_label']}: "
        f"{home['monthly_cost_fit']:.1f}"
    )

    # -----------------------------------------
    # Location details
    # -----------------------------------------

    st.markdown(f"**{text['location_score']}**")

    st.write(
        f"{text['school_fit_label']}: "
        f"{home['school_fit']:.1f}"
    )

    st.write(
        f"{text['safety_fit_label']}: "
        f"{home['safety_fit']:.1f}"
    )

    st.write(
        f"{text['commute_fit_label']}: "
        f"{home['commute_fit']:.1f}"
    )

    # -----------------------------------------
    # Property details
    # -----------------------------------------

    st.markdown(f"**{text['property_score']}**")

    st.write(
        f"{text['size_fit_label']}: "
        f"{home['size_fit']:.1f}"
    )

    st.write(
        f"{text['amenities_fit_label']}: "
        f"{home['amenities_fit']:.1f}"
    )

    st.divider()

    # -----------------------------------------
    # Requirement violations
    # -----------------------------------------

    if home["violations"]:

        for violation in home["violations"]:
            translated_message = translate_violation(
                violation,
                text,
            )

            st.warning(translated_message)

    else:
        st.success(text["requirements_met"])

    st.caption(text["score_explanation_note"])

# Language selection
language = st.sidebar.selectbox(
    "Language / Idioma",
    ["English", "Español"],
)

# Select translation dictionary
if language == "Español":
    text = ES
else:
    text = EN


# Application header
st.title("🏠 " + text["app_title"])

st.subheader(text["tagline"])

st.divider()


# Welcome section
st.header(text["welcome"])

st.write(text["description"])


# Application overview
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💰 " + text["affordability"])
    st.write(
        "Budget, mortgage payments, and monthly housing costs."
        if language == "English"
        else "Presupuesto, hipoteca y costos mensuales de vivienda."
    )

with col2:
    st.subheader("📍 " + text["location"])
    st.write(
        "Schools, safety, and commute preferences."
        if language == "English"
        else "Escuelas, seguridad y preferencias de traslado."
    )

with col3:
    st.subheader("🏡 " + text["property"])
    st.write(
        "Home size and desired amenities."
        if language == "English"
        else "Tamaño de la vivienda y características deseadas."
    )


st.divider()


# Start button
if st.button(
    text["start"],
    type="primary",
):
    st.session_state["started"] = True


# Buyer Preferences
if st.session_state.get("started", False):

    st.divider()

    st.header(text["buyer_preferences"])

    if language == "English":
        st.write(
            "Rate how important each category is to you "
            "on a scale from 0 to 5."
        )
        st.caption(
            "0 = Not important | 5 = Extremely important"
        )
    else:
        st.write(
            "Califica qué tan importante es cada categoría "
            "para ti en una escala del 0 al 5."
        )
        st.caption(
            "0 = Nada importante | 5 = Extremadamente importante"
        )

    affordability_importance = st.slider(
        text["affordability"],
        min_value=0,
        max_value=5,
        value=5,
        key="affordability_importance",
    )

    location_importance = st.slider(
        text["location"],
        min_value=0,
        max_value=5,
        value=4,
        key="location_importance",
    )

    property_importance = st.slider(
        text["property"],
        min_value=0,
        max_value=5,
        value=3,
        key="property_importance",
    )

    st.subheader(
        "Your Selected Priorities"
        if language == "English"
        else "Tus prioridades seleccionadas"
    )

    st.write({
        "affordability_importance": affordability_importance,
        "location_importance": location_importance,
        "property_importance": property_importance,
    })

    st.write({
        "affordability_importance": affordability_importance,
        "location_importance": location_importance,
        "property_importance": property_importance,
    })
        # Affordability Preferences
    if affordability_importance > 0:

        st.divider()

        st.subheader(text["affordability_preferences"])
        st.write(text["affordability_help"])

        col1, col2 = st.columns(2)

        with col1:
            target_price = st.number_input(
                text["target_price"],
                min_value=0,
                value=450000,
                step=10000,
                key="target_price",
            )

            target_monthly_cost = st.number_input(
                text["target_monthly_cost"],
                min_value=0,
                value=3500,
                step=100,
                key="target_monthly_cost",
            )

            price_importance = st.slider(
                text["price_importance"],
                min_value=0,
                max_value=5,
                value=3,
                key="price_importance",
            )

        with col2:
            maximum_price = st.number_input(
                text["maximum_price"],
                min_value=0,
                value=600000,
                step=10000,
                key="maximum_price",
            )

            maximum_monthly_cost = st.number_input(
                text["maximum_monthly_cost"],
                min_value=0,
                value=4500,
                step=100,
                key="maximum_monthly_cost",
            )

            monthly_cost_importance = st.slider(
                text["monthly_cost_importance"],
                min_value=0,
                max_value=5,
                value=5,
                key="monthly_cost_importance",
            )

        down_payment = st.number_input(
            text["down_payment"],
            min_value=0,
            value=100000,
            step=5000,
            key="down_payment",
        )

        with st.expander(text["advanced_financing"]):

            interest_rate = st.number_input(
                text["interest_rate"],
                min_value=0.0,
                max_value=30.0,
                value=6.25,
                step=0.25,
                key="interest_rate",
            )

            loan_term = st.number_input(
                text["loan_term"],
                min_value=1,
                max_value=50,
                value=30,
                step=1,
                key="loan_term",
            )

        # Validate affordability inputs
        affordability_valid = True

        if maximum_price <= target_price:
            st.error(
                "Maximum home price must be greater than target price."
                if language == "English"
                else "El precio máximo debe ser mayor que el precio objetivo."
            )
            affordability_valid = False

        if maximum_monthly_cost <= target_monthly_cost:
            st.error(
                "Maximum monthly cost must be greater than target monthly cost."
                if language == "English"
                else "El costo mensual máximo debe ser mayor que el costo objetivo."
            )
            affordability_valid = False

        if price_importance == 0 and monthly_cost_importance == 0:
            st.warning(
                "Both affordability subcategories have zero importance."
                if language == "English"
                else "Ambas subcategorías de asequibilidad tienen importancia cero."
            )

        if affordability_valid:
            st.success(
                "Affordability preferences saved."
                if language == "English"
                else "Preferencias de asequibilidad guardadas."
            )
    # Location & Lifestyle Preferences
    if location_importance > 0:

        st.divider()

        st.subheader(text["location_preferences"])
        st.write(text["location_help"])

        col1, col2, col3 = st.columns(3)

        with col1:
            school_importance = st.slider(
                text["school_importance"],
                min_value=0,
                max_value=5,
                value=5,
                key="school_importance",
            )

            minimum_school_rating = st.number_input(
                text["minimum_school_rating"],
                min_value=1,
                max_value=10,
                value=6,
                step=1,
                key="minimum_school_rating",
            )

        with col2:
            safety_importance = st.slider(
                text["safety_importance"],
                min_value=0,
                max_value=5,
                value=4,
                key="safety_importance",
            )

            minimum_safety_rating = st.number_input(
                text["minimum_safety_rating"],
                min_value=1,
                max_value=10,
                value=6,
                step=1,
                key="minimum_safety_rating",
            )

        with col3:
            commute_importance = st.slider(
                text["commute_importance"],
                min_value=0,
                max_value=5,
                value=2,
                key="commute_importance",
            )

            maximum_commute_minutes = st.number_input(
                text["maximum_commute_minutes"],
                min_value=1,
                max_value=180,
                value=45,
                step=5,
                key="maximum_commute_minutes",
            )

        if (
            school_importance == 0
            and safety_importance == 0
            and commute_importance == 0
        ):
            st.warning(
                "All location subcategories have zero importance."
                if language == "English"
                else "Todas las subcategorías de ubicación tienen importancia cero."
            )
        else:
            st.success(
                "Location preferences entered."
                if language == "English"
                else "Preferencias de ubicación ingresadas."
            ) 
    # -----------------------------------------
    # Property Preferences
    # -----------------------------------------

    if property_importance > 0:

        st.divider()

        st.subheader(text["property_preferences"])
        st.write(text["property_help"])

        col1, col2 = st.columns(2)

        with col1:

            size_importance = st.slider(
                text["size_importance"],
                min_value=0,
                max_value=5,
                value=4,
                key="size_importance",
            )

            minimum_square_feet = st.number_input(
                text["minimum_square_feet"],
                min_value=0,
                value=1800,
                step=100,
                key="minimum_square_feet",
            )

        with col2:

            amenities_importance = st.slider(
                text["amenities_importance"],
                min_value=0,
                max_value=5,
                value=3,
                key="amenities_importance",
            )

            target_square_feet = st.number_input(
                text["target_square_feet"],
                min_value=0,
                value=2500,
                step=100,
                key="target_square_feet",
            ) 
        # -----------------------------------------
        # Amenities Preferences
        # -----------------------------------------

        st.subheader(text["amenities_preferences"])
        st.write(text["amenities_help"])

        amenity_options = {
            0: text["dont_care"],
            1: text["nice_to_have"],
            2: text["must_have"],
        }

        amenity_keys = [
            "garage",
            "pool",
            "large_yard",
            "home_office",
            "updated_kitchen",
            "first_floor_primary",
        ]

        default_amenities = {
            "garage": 2,
            "pool": 0,
            "large_yard": 1,
            "home_office": 2,
            "updated_kitchen": 1,
            "first_floor_primary": 0,
        }

        amenity_preferences = {}

        for amenity in amenity_keys:

            preference = st.selectbox(
                label=text[amenity],
                options=[0, 1, 2],
                index=default_amenities[amenity],
                format_func=lambda value: amenity_options[value],
                key=f"amenity_{amenity}",
            )

            amenity_preferences[amenity] = preference  
            # -----------------------------------------
        # Property Validation
        # -----------------------------------------

        property_valid = True

        if target_square_feet <= minimum_square_feet:

            st.error(
                "Target property size must be greater than "
                "minimum property size."
                if language == "English"
                else
                "El tamaño objetivo debe ser mayor que "
                "el tamaño mínimo de la vivienda."
            )

            property_valid = False

        if size_importance == 0 and amenities_importance == 0:

            st.warning(
                "Both property subcategories have zero importance."
                if language == "English"
                else
                "Ambas subcategorías de vivienda tienen "
                "importancia cero."
            )

        if property_valid:

            st.success(text["property_preferences_saved"])

    # -----------------------------------------
    # Complete Buyer Profile
    # -----------------------------------------

    buyer = {
        # Main importance ratings
        "affordability_importance": affordability_importance,
        "location_importance": location_importance,
        "property_importance": property_importance,

        # Affordability
        "target_price": st.session_state.get("target_price", 450000),
        "maximum_price": st.session_state.get("maximum_price", 600000),
        "target_monthly_cost": st.session_state.get(
            "target_monthly_cost", 3500
        ),
        "maximum_monthly_cost": st.session_state.get(
            "maximum_monthly_cost", 4500
        ),
        "down_payment": st.session_state.get("down_payment", 100000),
        "annual_interest_rate": (
            st.session_state.get("interest_rate", 6.25) / 100
        ),
        "loan_term_years": st.session_state.get("loan_term", 30),
        "price_importance": st.session_state.get("price_importance", 3),
        "monthly_cost_importance": st.session_state.get(
            "monthly_cost_importance", 5
        ),

        # Location & Lifestyle
        "school_importance": st.session_state.get("school_importance", 5),
        "safety_importance": st.session_state.get("safety_importance", 4),
        "commute_importance": st.session_state.get("commute_importance", 2),
        "minimum_school_rating": st.session_state.get(
            "minimum_school_rating", 6
        ),
        "minimum_safety_rating": st.session_state.get(
            "minimum_safety_rating", 6
        ),
        "maximum_commute_minutes": st.session_state.get(
            "maximum_commute_minutes", 45
        ),

        # Property
        "size_importance": st.session_state.get("size_importance", 4),
        "amenities_importance": st.session_state.get(
            "amenities_importance", 3
        ),
        "minimum_square_feet": st.session_state.get(
            "minimum_square_feet", 1800
        ),
        "target_square_feet": st.session_state.get(
            "target_square_feet", 2500
        ),

        # Amenities
        "amenity_preferences": {
            "garage": st.session_state.get("amenity_garage", 2),
            "pool": st.session_state.get("amenity_pool", 0),
            "large_yard": st.session_state.get("amenity_large_yard", 1),
            "home_office": st.session_state.get("amenity_home_office", 2),
            "updated_kitchen": st.session_state.get(
                "amenity_updated_kitchen", 1
            ),
            "first_floor_primary": st.session_state.get(
                "amenity_first_floor_primary", 0
            ),
        },
    }

    st.session_state["buyer_profile"] = buyer

    # Validate buyer preferences
    buyer_errors = validate_buyer(buyer)

    if buyer_errors:
        st.error(
            "Please correct your buyer preferences:"
            if language == "English"
            else "Corrige tus preferencias de comprador:"
        )

        for error in buyer_errors:
            st.warning(error) 

    # Store the buyer profile for later calculations
    st.session_state["buyer"] = buyer

    # Display buyer profile for development testing
    with st.expander(
        "Buyer Profile (Development View)"
        if language == "English"
        else "Perfil del comprador (Vista de desarrollo)"
    ):
        st.json(buyer)


# ============================================
# Property Comparison Mode
# ============================================

st.divider()

st.header(text["entry_mode"])

comparison_mode = st.radio(
    text["entry_mode"],
    options=["demo", "manual"],
    format_func=lambda mode: (
        text["demo_mode"]
        if mode == "demo"
        else text["manual_mode"]
    ),
    horizontal=True,
    key="comparison_mode",
)

if comparison_mode == "manual":
    st.subheader(text["manual_entry_title"])

    st.write(text["manual_entry_help"])

    number_of_homes = st.number_input(
        text["number_of_homes"],
        min_value=1,
        max_value=5,
        value=3,
        step=1,
        key="number_of_homes",
    )

    st.info(
        f"{number_of_homes} "
        + (
            "homes selected for comparison."
            if language == "English"
            else "viviendas seleccionadas para comparar."
        )
    )
  
    # ============================================
    # Manual Property Entry
    # ============================================

    st.divider()

    manual_homes = []

    for i in range(int(number_of_homes)):

        st.subheader(
            f"{'Home' if language == 'English' else 'Vivienda'} {i + 1}"
        )

        home_name = st.text_input(
            "Property Name" if language == "English"
            else "Nombre de la vivienda",
            value=f"Home {i + 1}",
            key=f"home_name_{i}",
        )

        price = st.number_input(
            "Home Price ($)" if language == "English"
            else "Precio de la vivienda ($)",
            min_value=0,
            value=400000,
            step=5000,
            key=f"home_price_{i}",
        )

        square_feet = st.number_input(
            "Square Feet" if language == "English"
            else "Pies cuadrados",
            min_value=0,
            value=2000,
            step=100,
            key=f"home_sqft_{i}",
        )

        # ============================================
        # Financial Information
        # ============================================

        st.markdown(
            "**Financial Information**"
            if language == "English"
            else "**Información financiera**"
        )

        annual_property_tax = st.number_input(
            "Annual Property Taxes ($)"
            if language == "English"
            else "Impuestos anuales de propiedad ($)",
            min_value=0,
            value=7000,
            step=500,
            key=f"home_tax_{i}",
        )

        annual_insurance = st.number_input(
            "Annual Home Insurance ($)"
            if language == "English"
            else "Seguro anual de vivienda ($)",
            min_value=0,
            value=2000,
            step=100,
            key=f"home_insurance_{i}",
        )

        monthly_hoa = st.number_input(
            "Monthly HOA Fees ($)"
            if language == "English"
            else "Cuota mensual de asociación ($)",
            min_value=0,
            value=0,
            step=25,
            key=f"home_hoa_{i}",
        )

        monthly_pmi = st.number_input(
            "Monthly PMI ($)"
            if language == "English"
            else "Seguro hipotecario mensual PMI ($)",
            min_value=0,
            value=0,
            step=25,
            key=f"home_pmi_{i}",
        )

        # ============================================
        # Location & Lifestyle Information
        # ============================================

        st.markdown(
            "**Location & Lifestyle**"
            if language == "English"
            else "**Ubicación y estilo de vida**"
        )

        school_rating = st.number_input(
            "School Rating (0–10)"
            if language == "English"
            else "Calificación de escuelas (0–10)",
            min_value=0,
            max_value=10,
            value=7,
            step=1,
            key=f"home_school_{i}",
        )

        safety_rating = st.number_input(
            "Safety Rating (0–10)"
            if language == "English"
            else "Calificación de seguridad (0–10)",
            min_value=0,
            max_value=10,
            value=7,
            step=1,
            key=f"home_safety_{i}",
        )

        commute_minutes = st.number_input(
            "Commute Time (minutes)"
            if language == "English"
            else "Tiempo de traslado (minutos)",
            min_value=0,
            value=30,
            step=5,
            key=f"home_commute_{i}",
        )

        # ============================================
        # Property Amenities
        # ============================================

        st.markdown(
            "**Property Amenities**"
            if language == "English"
            else "**Características de la vivienda**"
        )

        amenity_labels = {
            "garage": ("Garage", "Garaje"),
            "pool": ("Swimming Pool", "Piscina"),
            "large_yard": ("Large Yard", "Patio grande"),
            "home_office": ("Home Office", "Oficina en casa"),
            "updated_kitchen": ("Updated Kitchen", "Cocina renovada"),
            "first_floor_primary": (
                "First-Floor Primary Bedroom",
                "Dormitorio principal en planta baja",
            ),
        }

        home_amenities = {}

        for amenity_key, labels in amenity_labels.items():

            label = labels[0] if language == "English" else labels[1]

            home_amenities[amenity_key] = st.checkbox(
                label,
                value=False,
                key=f"home_{i}_{amenity_key}",
            )

        manual_homes.append(
            {
                "name": home_name,
                "price": price,
                "square_feet": square_feet,
                "annual_property_tax": annual_property_tax,
                "annual_insurance": annual_insurance,
                "monthly_hoa": monthly_hoa,
                "monthly_pmi": monthly_pmi,
                "school_rating": school_rating,
                "safety_rating": safety_rating,
                "commute_minutes": commute_minutes,
                "amenities": home_amenities,
            }
        )

        st.divider()

        # ============================================
        # Calculate Manually Entered Homes
        # ============================================

if st.button(
    "Calculate My HomeScores"
    if language == "English"
    else "Calcular mis HomeScores",
    type="primary",
    key="calculate_manual_button",
):

    # Clear previous results so stale rankings are not shown
    st.session_state.pop("manual_results", None)

    # Check that a buyer profile exists
    buyer = st.session_state.get("buyer_profile")

    if buyer is None:
        st.error(
            "Please complete your buyer preferences first."
            if language == "English"
            else "Primero completa tus preferencias de comprador."
        )

    else:
        # Validate buyer preferences
        errors = validate_buyer(buyer)

        # Validate each manually entered home
        for home in manual_homes:
            home_errors = validate_home(home, buyer)

            for error in home_errors:
                translated_error = translate_validation_message(error, language)

                if home["name"].strip():
                    errors.append(f"{home['name']}: {translated_error}")
                else:
                    errors.append(translated_error)
        if errors:
            st.error(
                "Please correct the following information:"
                if language == "English"
                else "Corrige la siguiente información:"
            )

            for error in errors:
                st.warning(error)
        else:
            # All inputs are valid — calculate scores
            results = []

            for home in manual_homes:
                result = calculate_home_result(home, buyer)
                results.append(result)

            best_matches, other_homes = group_and_rank_homes(
                results
            )

            st.session_state["manual_results"] = {
                "best_matches": best_matches,
                "other_homes": other_homes,
            }

            st.success(
                "HomeScores calculated successfully!"
                if language == "English"
                else "HomeScores calculados correctamente!"
            )
            
            best_matches, other_homes = group_and_rank_homes(results)

            st.session_state["manual_results"] = {
                "best_matches": best_matches,
                "other_homes": other_homes,
            }

            st.success(
                "HomeScores calculated successfully!"
                if language == "English"
                else "¡HomeScores calculados correctamente!"
            )

# ============================================
# Display Manual HomeScore Results
# ============================================

if (
    comparison_mode == "manual"
    and "manual_results" in st.session_state
):

    manual_results = st.session_state["manual_results"]

    st.divider()

    st.header(
        "Your HomeScore Results"
        if language == "English"
        else "Tus resultados de HomeScore"
    )

    # Best Matches
    st.subheader(text["best_matches"])

    if not manual_results["best_matches"]:
        st.info(
            "No homes meet all your requirements."
            if language == "English"
            else "Ninguna vivienda cumple todos tus requisitos."
        )

    for home in manual_results["best_matches"]:

        st.markdown(
            f"### #{home['rank']} — {home['name']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                text["homescore_label"],
                f"{home['homescore']:.1f}"
            )

        with col2:
            st.metric(
                text["monthly_cost_label"],
                f"${home['monthly_housing_cost']:,.0f}"
            )

        with col3:
            st.metric(
                text["constraint_label"],
                home["constraint_count"]
            )

        with st.expander(
            text["why_score"] + f" — {home['name']}"
        ):
            show_score_explanation(home, text, buyer)

        st.divider()

    # Other Homes
    st.subheader(text["other_homes"])

    if not manual_results["other_homes"]:
        st.info(
            "All homes meet your requirements."
            if language == "English"
            else "Todas las viviendas cumplen tus requisitos."
        )

    for home in manual_results["other_homes"]:

        st.markdown(
            f"### #{home['rank']} — {home['name']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                text["homescore_label"],
                f"{home['homescore']:.1f}"
            )

        with col2:
            st.metric(
                text["monthly_cost_label"],
                f"${home['monthly_housing_cost']:,.0f}"
            )

        with col3:
            st.metric(
                text["constraint_label"],
                home["constraint_count"]
            )

        with st.expander(
            text["why_score"] + f" — {home['name']}"
        ):
            show_score_explanation(home, text, buyer)

        st.divider()

if comparison_mode == "demo":
    st.header(text["demo_results"])
    st.write(text["demo_description"])
    st.caption(text["demo_disclaimer"])

    if st.button(
        text["calculate_demo"],
        type="primary",
        key="calculate_demo_button",
    ):

        # Calculate each home's results
        results = []

        for home in DEMO_HOMES:
            result = calculate_home_result(home, buyer)
            results.append(result)

        # Separate and rank homes
        best_matches, other_homes = group_and_rank_homes(results)

        # Save results for display
        st.session_state["demo_results"] = {
            "best_matches": best_matches,
            "other_homes": other_homes,
        }

    # Display results after calculation
    if "demo_results" in st.session_state:

        demo_results = st.session_state["demo_results"]

        st.subheader(text["best_matches"])

        if not demo_results["best_matches"]:
            st.info(
                "No homes meet all requirements."
                if language == "English"
                else "Ninguna vivienda cumple todos los requisitos."
            )

        for home in demo_results["best_matches"]:

            st.markdown(
                f"### #{home['rank']} — {home['name']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    text["homescore_label"],
                    f"{home['homescore']:.1f}",
                )

            with col2:
                st.metric(
                    text["monthly_cost_label"],
                    f"${home['monthly_housing_cost']:,.0f}",
                )

            with col3:
                st.metric(
                    text["constraint_label"],
                    home["constraint_count"],
                )

            with st.expander(

                text["why_score"] + f" — {home['name']}"

            ):

                show_score_explanation(home, text, buyer)

 
            st.divider()

        st.subheader(text["other_homes"])

        if not demo_results["other_homes"]:
            st.info(
                "All homes meet your requirements."
                if language == "English"
                else "Todas las viviendas cumplen tus requisitos."
            )

        for home in demo_results["other_homes"]:

            st.markdown(
                f"### #{home['rank']} — {home['name']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    text["homescore_label"],
                    f"{home['homescore']:.1f}",
                )

            with col2:
                st.metric(
                    text["monthly_cost_label"],
                    f"${home['monthly_housing_cost']:,.0f}",
                )

            with col3:
                st.metric(
                    text["constraint_label"],
                    home["constraint_count"],
                )

            with st.expander(
                text["why_score"] + f" — {home['name']}"
            ):
                show_score_explanation(home, text, buyer)

            st.divider()