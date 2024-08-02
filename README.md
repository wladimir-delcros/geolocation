Geolocation Project
This project allows users to reverse geocode coordinates and extract administrative levels using a Flask web application. The data for countries, states, and cities is sourced from the countries-states-cities-database.

Features
Dynamic selection of continent, country, and city.
Reverse geocoding to obtain detailed address information.
Extraction of administrative levels (country, state, county, city).
Display of results in a user-friendly table format.
Installation
Clone the Repository
bash
Copier le code
git clone https://github.com/wladimir-delcros/geolocation.git
cd geolocation
Set Up Virtual Environment (Optional but Recommended)
bash
Copier le code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies
bash
Copier le code
pip install -r requirements.txt
Usage
Running the Flask Application
Start the Flask server:

bash
Copier le code
python app.py
Open your browser and go to http://127.0.0.1:5000.

How to Use the Web Interface
Select Continent: Choose a continent from the dropdown.
Select Country: Based on the selected continent, choose a country.
Select City: Choose a city from the dropdown.
Generate: Click the 'Generate' button to fetch the geolocation data and display the results in a table.
Project Structure
app.py: Main Flask application.
data.json: Contains hierarchical data for continents, countries, and cities.
templates/index.html: Frontend HTML file with JavaScript for dynamic selection.
static/: Contains static files like CSS and JavaScript.
API Endpoints
/get_countries
Method: GET
Parameters: continent
Description: Returns the list of countries for the selected continent.
/get_cities
Method: GET
Parameters: continent, country
Description: Returns the list of cities for the selected country.
/generate
Method: POST
Payload: JSON object with continent, country, city
Description: Returns the geolocation data for the selected city.
Example Data
Here's an example of how the data.json is structured:

json
Copier le code
{
  "Europe": {
    "France": {
      "Paris": {"lat": 48.8566, "lon": 2.3522},
      "Lyon": {"lat": 45.7640, "lon": 4.8357}
    },
    "Germany": {
      "Berlin": {"lat": 52.5200, "lon": 13.4050},
      "Munich": {"lat": 48.1351, "lon": 11.5820}
    }
  },
  "Asia": {
    "Japan": {
      "Tokyo": {"lat": 35.6762, "lon": 139.6503},
      "Osaka": {"lat": 34.6937, "lon": 135.5023}
    }
  }
}
Contributing
Feel free to open issues or submit pull requests with improvements.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Nominatim for the reverse geocoding service.
countries-states-cities-database for the location data.
