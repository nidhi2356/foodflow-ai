import requests
import streamlit as st


# -----------------------------------------
# Configuration
# -----------------------------------------

API_URL = "http://127.0.0.1:8000/api/search"


# -----------------------------------------
# Page Configuration
# -----------------------------------------

st.set_page_config(
    page_title="FoodFlow AI",
    page_icon="🍽️",
    layout="wide"
)


# -----------------------------------------
# Header
# -----------------------------------------

st.title("🍽️ FoodFlow AI")

st.write(
    "Find the best food based on your preferences, "
    "budget, cuisine, dietary requirements, and more."
)


# -----------------------------------------
# Search Input
# -----------------------------------------

query = st.text_input(
    "What are you looking for?",
    placeholder="e.g. healthy high protein vegetarian dinner under ₹400"
)


top_k = st.slider(
    "Number of results",
    min_value=1,
    max_value=10,
    value=5
)


# -----------------------------------------
# Search Button
# -----------------------------------------

if st.button("🔍 Search", type="primary"):

    if not query.strip():

        st.error(
            "Please enter a food search query."
        )

    else:

        try:

            with st.spinner("Finding the best food for you..."):

                response = requests.post(
                    API_URL,
                    json={
                        "query": query,
                        "top_k": top_k
                    },
                    timeout=120
                )

            # -----------------------------------------
            # Handle API Errors
            # -----------------------------------------

            if response.status_code != 200:

                try:
                    error_data = response.json()

                    st.error(
                        error_data.get(
                            "detail",
                            "Search request failed."
                        )
                    )

                except ValueError:

                    st.error(
                        f"Search failed with status "
                        f"code {response.status_code}."
                    )

            else:

                data = response.json()

                results = data.get(
                    "results",
                    []
                )

                recommendation = data.get(
                    "recommendation",
                    ""
                )

                # -----------------------------------------
                # No Results
                # -----------------------------------------

                if not results:

                    st.warning(
                        "No food items found matching "
                        "your requirements."
                    )

                else:

                    # -----------------------------------------
                    # AI Recommendation
                    # -----------------------------------------

                    st.subheader("🤖 AI Recommendation")

                    st.info(
                        recommendation
                    )

                    st.divider()

                    # -----------------------------------------
                    # Search Results
                    # -----------------------------------------

                    st.subheader(
                        f"🍴 Search Results ({len(results)})"
                    )

                    for index, result in enumerate(
                        results
                    ):

                        metadata = result.get(
                            "metadata",
                            {}
                        )

                        food_name = metadata.get(
                            "item_name",
                            "Unknown Food"
                        )

                        restaurant_name = metadata.get(
                            "restaurant_name",
                            "Unknown Restaurant"
                        )

                        location = metadata.get(
                            "location",
                            "Unknown Location"
                        )

                        price = metadata.get(
                            "price",
                            "N/A"
                        )

                        rating = metadata.get(
                            "rating",
                            "N/A"
                        )

                        cuisine = metadata.get(
                            "cuisine",
                            "N/A"
                        )

                        category = metadata.get(
                            "category",
                            "N/A"
                        )

                        spice_level = metadata.get(
                            "spice_level",
                            "N/A"
                        )

                        is_veg = metadata.get(
                            "is_veg",
                            False
                        )

                        dietary_tags = metadata.get(
                            "dietary_tags",
                            ""
                        )

                        final_score = result.get(
                            "final_score",
                            0
                        )

                        # -----------------------------------------
                        # Result Card
                        # -----------------------------------------

                        with st.container(
                            border=True
                        ):

                            st.markdown(
                                f"### {index + 1}. {food_name}"
                            )

                            col1, col2, col3 = st.columns(
                                3
                            )

                            with col1:

                                st.write(
                                    f"🏪 **Restaurant:** "
                                    f"{restaurant_name}"
                                )

                                st.write(
                                    f"📍 **Location:** "
                                    f"{location}"
                                )

                                st.write(
                                    f"🍽️ **Cuisine:** "
                                    f"{cuisine}"
                                )

                            with col2:

                                st.write(
                                    f"💰 **Price:** "
                                    f"₹{price}"
                                )

                                st.write(
                                    f"⭐ **Rating:** "
                                    f"{rating}"
                                )

                                st.write(
                                    f"📂 **Category:** "
                                    f"{category}"
                                )

                            with col3:

                                vegetarian_text = (
                                    "Yes"
                                    if is_veg
                                    else "No"
                                )

                                st.write(
                                    f"🥗 **Vegetarian:** "
                                    f"{vegetarian_text}"
                                )

                                st.write(
                                    f"🌶️ **Spice Level:** "
                                    f"{spice_level}"
                                )

                                st.write(
                                    f"🏷️ **Dietary Tags:** "
                                    f"{dietary_tags}"
                                )

                            st.write("")

                            st.write(
                                result.get(
                                    "text",
                                    ""
                                )
                            )

                            # Keep technical ranking information
                            # hidden by default.
                            with st.expander(
                                "View ranking details"
                            ):

                                st.write(
                                    f"Final Score: "
                                    f"{final_score:.4f}"
                                )

                                st.write(
                                    f"Cross Encoder Score: "
                                    f"{result.get('cross_encoder_score', 0):.4f}"
                                )

                                st.write(
                                    f"Metadata Score: "
                                    f"{result.get('metadata_score', 0):.4f}"
                                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the FoodFlow AI API. "
                "Make sure the FastAPI server is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The search request timed out. "
                "Please try again."
            )

        except requests.exceptions.RequestException as e:

            st.error(
                f"Request failed: {e}"
            )

        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )