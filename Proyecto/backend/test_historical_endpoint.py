"""
Test script for the new 7-day historical endpoint.
This script tests the endpoint without requiring authentication.
"""

import requests
from datetime import date, timedelta

# API Base URL
BASE_URL = "http://localhost:8000/api/v1"

def test_7_day_historical():
    """Test the 7-day historical endpoint."""

    print("=" * 60)
    print("Testing 7-Day Historical Data Endpoint")
    print("=" * 60)

    # Test with station_id = 1 (you may need to adjust this)
    station_id = 1

    # Test 1: Without end_date (should default to today)
    print("\n1. Testing without end_date (defaults to today)...")
    url = f"{BASE_URL}/air-quality/historical/7-days?station_id={station_id}"

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("\n✅ Success!")
            print(f"Station: {data['station']['name']}")
            print(f"City: {data['station']['city']}")
            print(f"Date Range: {data['start_date']} to {data['end_date']}")
            print(f"\nPollutants found: {len(data['pollutants_data'])}")

            for pollutant_data in data['pollutants_data']:
                pollutant = pollutant_data['pollutant']
                data_points = pollutant_data['data_points']
                print(f"\n  - {pollutant['name']} ({pollutant['unit']})")
                print(f"    Data points: {len(data_points)}")
                if data_points:
                    print(f"    Sample: {data_points[0]}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

    # Test 2: With specific end_date
    print("\n" + "=" * 60)
    print("2. Testing with specific end_date...")
    end_date = date.today().isoformat()
    url = f"{BASE_URL}/air-quality/historical/7-days?station_id={station_id}&end_date={end_date}"

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"Date Range: {data['start_date']} to {data['end_date']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

    # Test 3: With invalid station_id
    print("\n" + "=" * 60)
    print("3. Testing with invalid station_id (should return 404)...")
    url = f"{BASE_URL}/air-quality/historical/7-days?station_id=99999"

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 404:
            print("✅ Correctly returns 404 for invalid station")
        else:
            print(f"❌ Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    print("\n⚠️  Make sure the backend is running on http://localhost:8000\n")
    test_7_day_historical()

