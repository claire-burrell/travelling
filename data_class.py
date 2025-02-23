import pickle
import os
from collections import OrderedDict, defaultdict
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic
import csv

class TravelData:
    """
    TravelData Class - Manages travel plans, locations, and associated details.
    
    FUNCTIONS SUMMARY:
    ---------------------------------------------------
    # DATA STORAGE & MANAGEMENT
    - __init__(self, file_path): Initializes the class, loads stored travel data, and sets up geolocation services.
    - save_data(self): Saves the current travel data to a Pickle file.
    - load_data(self): Loads travel data from a Pickle file, or initializes fresh data if not found.
    - clear_data(self): Clears all stored travel data, resetting it to an empty dictionary.
    
    # LOCATION MANAGEMENT
    - get_lat_lon(self, location): Fetches latitude and longitude using OpenStreetMap (geopy) API.
    - add_location(self, name, country, days, transport, position, after_place): Adds a new location, automatically retrieving its coordinates.
    - remove_location(self, name): Removes a location from the travel plan.
    - move_location(self, name, new_position, after_place): Moves a location to the start, end, or after another location.
    
    # DATA MODIFICATION
    - change_days(self, name, new_days): Updates the number of days spent at a location.
    - change_transport(self, name, new_transport): Updates the transport method for a location.
    - change_country(self, name, new_country): Changes the country of a location.
    - change_location_name(self, old_name, new_name): Renames a location while keeping all other details.
    
    # ITINERARY ANALYSIS
    - total_days(self): Calculates and displays the total number of travel days.
    - days_per_country(self): Calculates and displays the total days spent in each country.
    - calculate_total_distance(self): Computes the total travel distance (km) between all locations.
    
    # DISPLAY & EXPORT
    - list_locations(self): Lists all stored travel locations in order.
    - display_data(self): Displays detailed information about each location.
    - export_to_csv(self, filename): Exports travel data to a CSV file for easy sharing.
    """

    def __init__(self, file_path):
        """Initialize the class with an empty ordered dictionary and a file path for storage."""
        self.file_path = file_path
        self.data = OrderedDict()  # Maintain order of locations
        self.geolocator = Nominatim(user_agent="travel_planner")  # Geolocation API
        self.load_data()  # Load existing data if available

    def save_data(self):
        """Save the current travel data to a Pickle file."""
        try:
            with open(self.file_path, 'wb') as f:
                pickle.dump(self.data, f)
            print("✅ Travel data saved successfully.")
        except Exception as e:
            print(f"❌ Error saving data: {e}")

    def load_data(self):
        """Load travel data from a Pickle file (if it exists)."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'rb') as f:
                    self.data = pickle.load(f)
                print("✅ Travel data loaded successfully.")
            except Exception as e:
                print(f"❌ Error loading data: {e}")
                self.data = OrderedDict()
        else:
            print("⚠️ No existing data found. Starting fresh.")

    def get_lat_lon(self, location):
        """Fetch latitude and longitude for a given location using OpenStreetMap API."""
        try:
            geo_info = self.geolocator.geocode(location)
            if geo_info:
                return geo_info.latitude, geo_info.longitude
            else:
                print(f"⚠️ Could not find coordinates for '{location}'.")
                return None, None
        except GeocoderTimedOut:
            print("⏳ Geolocation request timed out. Try again.")
            return None, None

    def add_location(self, name, country, days, transport="Unknown", position="end", after_place=None):
        """Add a new travel location at a specific position in the list, fetching coordinates automatically."""
        lat, lon = self.get_lat_lon(f"{name}, {country}")

        if lat is None or lon is None:
            print(f"⚠️ Skipping '{name}' as coordinates could not be found.")
            return

        new_entry = (country, lat, lon, days, transport)
        updated_data = OrderedDict()

        if position == "start":
            updated_data[name] = new_entry
            updated_data.update(self.data)
            self.data = updated_data
        elif position == "after" and after_place in self.data:
            for key, value in self.data.items():
                updated_data[key] = value
                if key == after_place:
                    updated_data[name] = new_entry
            self.data = updated_data
        else:
            self.data[name] = new_entry

        print(f"➕ Added {name} ({days} days) with transport: {transport}. Coordinates: ({lat}, {lon})")
        self.save_data()

    def remove_location(self, name):
        """Remove a travel location if it exists."""
        if name in self.data:
            del self.data[name]
            print(f"❌ Removed {name}.")
            self.save_data()
        else:
            print(f"⚠️ {name} not found in data.")

    def move_location(self, name, new_position="end", after_place=None):
        """
        Move an existing location to a new position: "start", "end", or after another location.
        """
        if name not in self.data:
            print(f"⚠️ {name} not found in the travel list.")
            return

        # Extract the location details
        location_details = self.data.pop(name)
        updated_data = OrderedDict()

        if new_position == "start":
            # Move to the beginning
            updated_data[name] = location_details
            updated_data.update(self.data)

        elif new_position == "after" and after_place in self.data:
            # Move after a specific place
            for key, value in self.data.items():
                updated_data[key] = value
                if key == after_place:
                    updated_data[name] = location_details

        else:
            # Default: Move to the end
            self.data[name] = location_details
            updated_data = self.data

        self.data = updated_data
        print(f"🔄 Moved {name} to position: {new_position}.")
        self.save_data()

    def clear_data(self):
        """Clear all travel data, resetting to an empty dictionary."""
        self.data = OrderedDict()
        self.save_data()
        print("🗑️ All travel data has been cleared.")

    def display_data(self):
        """Print the stored travel data in a readable format."""
        if self.data:
            print("\n🔹 Current Travel Data:")
            for place, details in self.data.items():
                print(f"{place}: {details}")
        else:
            print("⚠️ No travel data available.")

    def list_locations(self):
        """List all stored locations in order."""
        if not self.data:
            print("⚠️ No travel locations stored.")
            return
        print("\n📍 List of Travel Locations:")
        for i, place in enumerate(self.data.keys(), start=1):
            print(f"{i}. {place}")

    def total_days(self):
        """Calculate and display the total number of days across all locations."""
        total = sum(details[3] for details in self.data.values())
        print(f"\n📅 Total Travel Days: {total} days")
        return total
    
    def days_per_country(self):
        """Calculate and display the total number of days spent in each country."""
        country_days = defaultdict(int)

        for place, details in self.data.items():
            country = details[0]  # Extract country name
            days = details[3]  # Extract number of days
            country_days[country] += days  # Sum up days per country

        print("\n🌍 Days Spent in Each Country:")
        for country, days in sorted(country_days.items(), key=lambda x: -x[1]):  # Sort by most days first
            print(f"  {country}: {days} days")
        
        return country_days

    def change_days(self, name, new_days):
        """Change the number of days spent at a specific location."""
        if name in self.data:
            country, lat, lon, _ = self.data[name]  # Keep existing data except days
            self.data[name] = (country, lat, lon, new_days)
            print(f"🕒 Updated {name}: Now spending {new_days} days.")
            self.save_data()
        else:
            print(f"⚠️ {name} not found in the travel list.")
            
    def change_transport(self, name, new_transport):
        """Change the transport method for a specific location."""
        if name in self.data:
            country, lat, lon, days, _ = self.data[name]  # Keep existing data except transport
            self.data[name] = (country, lat, lon, days, new_transport)
            print(f"🚗 Updated transport for {name}: Now using {new_transport}.")
            self.save_data()
        else:
            print(f"⚠️ {name} not found in the travel list.")
            
    def change_country(self, name, new_country):
        """Change the country of a specific location."""
        if name in self.data:
            _, lat, lon, days, transport = self.data[name]  # Keep all other details unchanged
            self.data[name] = (new_country, lat, lon, days, transport)
            print(f"🌍 Updated country for {name}: Now in {new_country}.")
            self.save_data()
        else:
            print(f"⚠️ {name} not found in the travel list.")
            
    def change_location_name(self, old_name, new_name):
        """Rename a location while keeping all other details the same."""
        if old_name in self.data:
            self.data[new_name] = self.data.pop(old_name)  # Rename key while keeping details
            print(f"✏️ Renamed '{old_name}' to '{new_name}'.")
            self.save_data()
        else:
            print(f"⚠️ '{old_name}' not found in the travel list.")
    
    def calculate_total_distance(self):
        """Calculates the total travel distance from location to location."""
        if len(self.data) < 2:
            print("⚠️ Not enough locations to calculate distance.")
            return 0
    
        locations = list(self.data.keys())
        total_distance = 0
    
        for i in range(len(locations) - 1):
            loc1 = (self.data[locations[i]][1], self.data[locations[i]][2])
            loc2 = (self.data[locations[i + 1]][1], self.data[locations[i + 1]][2])
            total_distance += geodesic(loc1, loc2).km
    
        print(f"🌍 Total Travel Distance: {round(total_distance, 2)} km")
        return total_distance
    

    def export_to_csv(self, filename="travel_data.csv"):
        """Exports travel data to a CSV file."""
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Location", "Country", "Latitude", "Longitude", "Days", "Transport"])
    
            for place, details in self.data.items():
                writer.writerow([place, *details])
    
        print(f"📂 Travel data exported to {filename}.")

