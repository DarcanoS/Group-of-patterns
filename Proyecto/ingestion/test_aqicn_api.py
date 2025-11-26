#!/usr/bin/env python3
"""
Quick test script for AQICN API
Tests the API connection and retrieves sample data for Bogotá
"""
import requests
import json
from datetime import datetime

# AQICN API Configuration
API_KEY = "56de3cea9ff0128d2aca8e86f4ff5b20bd8ddc4e"
BASE_URL = "https://api.waqi.info"

def test_city_feed(city: str = "bogota"):
    """Test getting air quality data for a city"""
    
    print("=" * 74)
    print("AQICN API - CITY FEED TEST")
    print("=" * 74)
    print(f"\n🌍 Testing city: {city}")
    
    url = f"{BASE_URL}/feed/{city}/"
    params = {"token": API_KEY}
    
    print(f"📡 URL: {url}")
    print(f"🔑 Using API token: {API_KEY[:20]}...")
    
    try:
        print("\n⏳ Making API request...")
        response = requests.get(url, params=params, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "ok":
                print("✅ API Response: SUCCESS\n")
                
                # Extract key information
                station_data = data.get("data", {})
                
                print("=" * 74)
                print("STATION INFORMATION")
                print("=" * 74)
                print(f"  Station ID:   {station_data.get('idx')}")
                print(f"  Station Name: {station_data.get('city', {}).get('name')}")
                
                geo = station_data.get('city', {}).get('geo', [])
                if geo:
                    print(f"  Coordinates:  {geo[0]}, {geo[1]}")
                
                print(f"  AQI:          {station_data.get('aqi')}")
                print(f"  Dominant:     {station_data.get('dominentpol', 'N/A')}")
                
                # Time information
                time_data = station_data.get('time', {})
                print(f"  Timestamp:    {time_data.get('s')} (UTC: {time_data.get('iso')})")
                
                # Individual pollutants
                iaqi = station_data.get('iaqi', {})
                if iaqi:
                    print("\n" + "=" * 74)
                    print("POLLUTANT MEASUREMENTS (Individual AQI)")
                    print("=" * 74)
                    for pollutant, value_data in iaqi.items():
                        print(f"  {pollutant.upper():6s}: {value_data.get('v')}")
                
                # Attribution
                attributions = station_data.get('attributions', [])
                if attributions:
                    print("\n" + "=" * 74)
                    print("DATA SOURCE")
                    print("=" * 74)
                    for attr in attributions[:2]:  # Show first 2
                        print(f"  • {attr.get('name')}")
                        if attr.get('url'):
                            print(f"    {attr.get('url')}")
                
                print("\n" + "=" * 74)
                print("RAW JSON RESPONSE (first 500 chars)")
                print("=" * 74)
                print(json.dumps(data, indent=2)[:500] + "...")
                
                return True
            else:
                print(f"❌ API Error: {data.get('status')}")
                print(f"   Message: {data.get('data', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Error: Request timeout after 10 seconds")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

def test_geo_feed(lat: float = 4.6097, lon: float = -74.0817):
    """Test getting air quality data by coordinates"""
    
    print("\n\n" + "=" * 74)
    print("AQICN API - GEO FEED TEST")
    print("=" * 74)
    print(f"\n📍 Testing coordinates: {lat}, {lon} (Bogotá)")
    
    url = f"{BASE_URL}/feed/geo:{lat};{lon}/"
    params = {"token": API_KEY}
    
    try:
        print("\n⏳ Making API request...")
        response = requests.get(url, params=params, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "ok":
                print("✅ API Response: SUCCESS\n")
                
                station_data = data.get("data", {})
                print(f"  Nearest Station: {station_data.get('city', {}).get('name')}")
                print(f"  AQI: {station_data.get('aqi')}")
                
                return True
            else:
                print(f"❌ API Error: {data.get('status')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_search_stations(keyword: str = "bogota"):
    """Test searching for stations"""
    
    print("\n\n" + "=" * 74)
    print("AQICN API - SEARCH STATIONS TEST")
    print("=" * 74)
    print(f"\n🔍 Searching for: {keyword}")
    
    url = f"{BASE_URL}/search/"
    params = {
        "token": API_KEY,
        "keyword": keyword
    }
    
    try:
        print("\n⏳ Making API request...")
        response = requests.get(url, params=params, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "ok":
                print("✅ API Response: SUCCESS\n")
                
                stations = data.get("data", [])
                print(f"  Found {len(stations)} stations\n")
                
                print("=" * 74)
                print("STATIONS FOUND")
                print("=" * 74)
                for i, station in enumerate(stations[:5], 1):  # Show first 5
                    print(f"\n{i}. {station.get('station', {}).get('name')}")
                    print(f"   URL: {station.get('station', {}).get('url')}")
                    geo = station.get('station', {}).get('geo', [])
                    if geo:
                        print(f"   Coordinates: {geo[0]}, {geo[1]}")
                    print(f"   Current AQI: {station.get('aqi')}")
                
                return True
            else:
                print(f"❌ API Error: {data.get('status')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("\n🧪 AQICN API TEST SUITE")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = []
    
    # Test 1: City feed
    results.append(("City Feed (Bogotá)", test_city_feed("bogota")))
    
    # Test 2: Geo feed
    results.append(("Geo Feed (Coordinates)", test_geo_feed()))
    
    # Test 3: Search stations
    results.append(("Search Stations", test_search_stations("bogota")))
    
    # Summary
    print("\n\n" + "=" * 74)
    print("TEST SUMMARY")
    print("=" * 74)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    print(f"\n  Total: {total_passed}/{len(results)} tests passed")
    print("=" * 74 + "\n")
