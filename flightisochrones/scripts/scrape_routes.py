# This script scrapes flight routes and durations for each of the airports of interest from FlightsFrom

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup
import os

def duration_to_minutes(duration_str):
    """Converts duration from format 'Xh Ym' to total minutes."""
    duration_str = duration_str.replace('DURATION:', '').strip()

    hours = 0
    minutes = 0
    if 'h' in duration_str:
        hours = int(duration_str.split('h')[0])
        minutes_part = duration_str.split('h')[1]
        if 'm' in minutes_part:
            minutes = int(minutes_part.split('m')[0])
    elif 'm' in duration_str:
        minutes = int(duration_str.split('m')[0])
    return hours * 60 + minutes

def scrape_flights_for_airports(airport_codes):

    script_dir = os.path.dirname(os.path.abspath(__file__))

    for airport_code in airport_codes:
        print(f"Scraping flights for {airport_code}")
        scrape_flights(airport_code)

        # Construct file path
        file_name = f"{airport_code}_flights_data.csv"
        file_path = os.path.join(script_dir, file_name)  
        
        # After scraping, print where the file is saved
        print(f"Data for {airport_code} saved to: {file_path}")

    print("Scraping Complete!")

# Scrape the reverse flight time
def get_reverse_flight_time(driver, destination, airport_code):
    # Navigate to the reverse flight page
    reverse_url = f"https://www.flightsfrom.com/{destination}-{airport_code}"
    driver.get(reverse_url)
    
    # Handle consent button if it appears
    try:
        consent_button = driver.find_element(By.CLASS_NAME, 'fc-button.fc-cta-consent.fc-primary-button')
        consent_button.click()
    except Exception:
        pass  # If it's not found, continue with the scraping

    # Wait for the page to load (adjust as necessary)
    time.sleep(0.1)

    # Parse the page content
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Locate the flight time text
    try:
        flight_time_minutes = soup.find('div', string="Flight time").find_next_sibling().get_text(strip=True)
    except Exception:
        flight_time_minutes = "N/A"  # If flight time is not found, return N/A
    
    try:
        distance_text = soup.find('div', string="Distance").find_next_sibling().get_text(strip=True)
        distance_km = distance_text.split('·')[1].replace('km', '').strip()
    except Exception:
        distance_km = "N/A"

    return flight_time_minutes, distance_km
        
def scrape_flights(airport_code):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # Initialize Chrome WebDriver with the WebDriver Manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the website
    url = f"https://www.flightsfrom.com/{airport_code}"
    driver.get(url)

    # Wait for the page to load
    time.sleep(2)

    # Find and click the "Consent" button
    try:
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "fc-cta-consent"))
        )
        consent_button.click()
        print("Clicked 'Consent' button")
    except Exception as e:
        print("Could not find or click 'Consent' button", e)

    # Find and click the "Show all destinations" element using a more refined selector
    try:
        show_all_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'ff-show-all')]"))
        )
        show_all_button.click()
        print("Clicked 'Show all destinations' button")
    except Exception as e:
        print("Could not find or click 'Show all destinations' button", e)

    time.sleep(1)

    # Scrape flight data
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    flights_data = []

    # Find all the list items in the <ul> element with class 'uk-list'
    flights = soup.select('ul.uk-list li.ff-li-list')

    for flight in flights:
        # Extract the destination info (split into code and name)
        destination_info = flight.select_one('a').get_text(strip=True)
        destination_code = destination_info[:3]  # First three characters are the airport code
        destination_name = destination_info[3:].strip()  # Rest is the city name

        # Extract the airline and flight duration
        airline = flight.select_one('.ff-image-airline').get('alt')
        duration_text = flight.select_one('.ff-row-duration-mobile').get_text(strip=True).replace('DURATION: ', '')
        duration_in_minutes = duration_to_minutes(duration_text)

        # Extract the number of flights per day and clean it up
        flights_per_day = flight.select_one('.ff-flights-daily')
        if flights_per_day:
            flights_per_day_text = flights_per_day.get_text(strip=True)
            if "1 flight per day" in flights_per_day_text:
                flights_per_day = "1"  # Keep it as 1
            elif "flights per day" in flights_per_day_text:
                flights_per_day = flights_per_day_text.replace(" flights per day", "")
            else:
                flights_per_day = "N/A"
        else:
            flights_per_day = "N/A"

        reverse_flight_time, distance_km = get_reverse_flight_time(driver, destination_code, airport_code)
        reverse_flight_time_minutes = duration_to_minutes(reverse_flight_time)
        distance_km = distance_km.replace('(', '').replace(' )', '').strip()

        flights_data.append([airport_code, destination_code, destination_name, airline, duration_in_minutes, reverse_flight_time_minutes, distance_km, flights_per_day])

    # Convert to DataFrame and save
    df = pd.DataFrame(flights_data, columns=['Departure Airport', 'Destination Code', 'Destination Name', 'Airline', 'Duration (minutes)', 'Reverse Duration (minutes)', 'Distance (km)', 'Flights per Day'])
    print(df)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, f'{airport_code}_flight_routes.csv')
    df.to_csv(file_path, index=False)

    driver.quit()

if __name__ == "__main__":
    airport_codes_list = [
        "ZRH",  # Zurich Airport
        "IST",   # Istanbul Airport
        "YYZ",  # Toronto Pearson International
        "HKG",  # Hong Kong International
        "LAX",  # Los Angeles International
        "LHR",  # London Heathrow
        "DXB",  # Dubai International
        "SIN",  # Singapore Changi
        "JFK",  # John F. Kennedy International, New York
        "CDG",  # Charles de Gaulle, Paris
        "SYD",  # Sydney Kingsford Smith
        "GRU",  # São Paulo-Guarulhos International
        "NRT",  # Narita International, Tokyo
        "DOH",  # Hamad International, Doha
        "AMS",  # Amsterdam Schiphol
        "ATL",  # Hartsfield-Jackson Atlanta International
        "JNB",  # O.R. Tambo International, Johannesburg
        "SFO",  # San Francisco International
        "ICN",  # Incheon International, Seoul
        "FRA",  # Frankfurt International
        "BKK",  # Suvarnabhumi International, Bangkok
        "MEX",  # Mexico City International
    ]

    scrape_flights_for_airports(airport_codes_list)
