from data_class import TravelData


file_path = r'C:\Users\cljbu\OneDrive\Documents\Programming\Travel\travel_data_dictionary.pkl'
updated_travel_route = TravelData(file_path)

updated_travel_route.data = {
    "London Gatwick": ("UK", 51.1537, -0.1821, 0, "Plane"),
    "Oslo": ("Norway", 59.9139, 10.7522, 4, "Plane"),
    "Bangkok": ("Thailand", 13.736717, 100.523186, 4, "Bus"),
    "Koh Phangan": ("Thailand", 9.7312, 100.0132, 3, "Bus"),
    "Khao Sok National Park": ("Thailand", 8.9202, 98.5249, 4, "Train"),
    "Krabi": ("Thailand", 8.0863, 98.9063, 3, "Train"),
    "Phuket": ("Thailand", 7.880448, 98.392291, 5, ""),
    "Chiang Mai": ("Thailand", 18.788343, 98.9853, 2, ""),
    "Golden Triangle": ("Thailand", 20.353912, 100.083967, 1, ""),
    "Huay Xai": ("Laos", 20.2771, 100.4139, 2, ""),
    "Luang Prabang": ("Laos", 19.893, 102.135, 2, ""),
    "Vang Vieng": ("Laos", 18.9233, 102.4478, 2, ""),
    "Vientiane": ("Laos", 17.9757, 102.6331, 3, ""),
    "Hanoi": ("Vietnam", 21.0285, 105.8542, 3, ""),
    "Ha Long Bay / Cat Ba": ("Vietnam", 20.9101, 107.1839, 2, ""),
    "Ninh Binh": ("Vietnam", 20.2530, 105.9740, 2, ""),
    "Phong Nha": ("Vietnam", 17.5956, 106.2870, 3, ""),
    "Hue": ("Vietnam", 16.4637, 107.5909, 2, ""),
    "Hoi An": ("Vietnam", 15.8801, 108.3380, 3, ""),
    "4000 Islands (Don Det)": ("Laos", 14.051, 105.832, 4, ""),
    "Siem Reap (Angkor Wat)": ("Cambodia", 13.4125, 103.8668, 3, ""),
    "Phnom Penh": ("Cambodia", 11.5564, 104.9282, 2, ""),
    "Koh Rong / Koh Rong Samloem": ("Cambodia", 10.7136, 103.2342, 3, ""),
    "Ho Chi Minh City (Vietnam)": ("Vietnam", 10.7769, 106.7009, 3, ""),
    "Bali": ("Bali", -8.4095, 115.1889, 18, ""),
    "Singapore": ("Singapore", 1.3521, 103.8198, 4, "")
}

updated_travel_route.list_locations()
updated_travel_route.days_per_country()

r"""
# ✅ Example Usage:
file_path = r'C:\Users\cljbu\OneDrive\Documents\Programming\Travel\travel_data.pkl'
travel_route = TravelData(file_path)

# Add locations
travel_route.add_location("Bangkok", "Thailand", 13.736717, 100.523186, 4)
travel_route.add_location("Bali", "Indonesia", -8.4095, 115.1889, 18)

# Display data
travel_route.display_data()

# Remove a location
travel_route.remove_location("Bangkok")

# Clear all data
# travel_route.clear_data()
"""