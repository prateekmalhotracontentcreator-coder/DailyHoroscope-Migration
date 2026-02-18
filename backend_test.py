#!/usr/bin/env python3
"""
Backend API Tests for Daily Horoscope App
Tests all API endpoints for functionality and GPT-5.2 integration
"""

import requests
import sys
import json
from datetime import datetime

class HoroscopeAPITester:
    def __init__(self, base_url="https://zodiac-daily-9.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details="", expected_status=None, actual_status=None):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name} - {details}")
            if expected_status and actual_status:
                print(f"   Expected status: {expected_status}, Got: {actual_status}")
        
        self.test_results.append({
            "name": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

    def test_root_endpoint(self):
        """Test API root endpoint"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=10)
            success = response.status_code == 200
            data = response.json() if success else {}
            self.log_test(
                "Root API endpoint (/api/)", 
                success, 
                f"Response: {data}",
                200, 
                response.status_code
            )
            return success
        except Exception as e:
            self.log_test("Root API endpoint", False, f"Error: {str(e)}")
            return False

    def test_zodiac_signs(self):
        """Test fetching all zodiac signs"""
        try:
            response = requests.get(f"{self.base_url}/signs", timeout=10)
            success = response.status_code == 200
            
            if success:
                signs = response.json()
                # Verify we have 12 signs
                signs_valid = len(signs) == 12
                # Check required fields
                required_fields = ['id', 'name', 'symbol', 'dates', 'element']
                fields_valid = all(all(field in sign for field in required_fields) for sign in signs)
                
                success = signs_valid and fields_valid
                details = f"Found {len(signs)} signs, fields valid: {fields_valid}"
                
                # Print first few signs for verification
                if len(signs) > 0:
                    print(f"   Sample signs: {[s['name'] for s in signs[:3]]}")
            else:
                details = "Failed to fetch signs"
                
            self.log_test(
                "Zodiac signs endpoint (/api/signs)",
                success,
                details,
                200,
                response.status_code
            )
            return success, signs if success else []
        except Exception as e:
            self.log_test("Zodiac signs endpoint", False, f"Error: {str(e)}")
            return False, []

    def test_horoscope_generation(self, sign_id, horoscope_type):
        """Test horoscope generation for a specific sign and type"""
        try:
            response = requests.get(
                f"{self.base_url}/horoscope/{sign_id}/{horoscope_type}", 
                timeout=60  # Longer timeout for LLM calls
            )
            success = response.status_code == 200
            
            if success:
                horoscope = response.json()
                # Verify required fields
                required_fields = ['id', 'sign', 'type', 'content', 'prediction_date', 'created_at']
                fields_valid = all(field in horoscope for field in required_fields)
                
                # Verify content is not empty and seems like a real horoscope
                content_valid = (
                    len(horoscope.get('content', '')) > 50 and
                    horoscope.get('sign') == sign_id and
                    horoscope.get('type') == horoscope_type
                )
                
                success = fields_valid and content_valid
                details = f"Content length: {len(horoscope.get('content', ''))}, Fields valid: {fields_valid}"
                
                # Print preview of content
                content_preview = horoscope.get('content', '')[:100] + "..." if horoscope.get('content', '') else "No content"
                print(f"   Content preview: {content_preview}")
            else:
                details = f"Failed to generate {horoscope_type} horoscope for {sign_id}"
                
            self.log_test(
                f"Horoscope generation ({sign_id} - {horoscope_type})",
                success,
                details,
                200,
                response.status_code
            )
            return success
        except Exception as e:
            self.log_test(f"Horoscope generation ({sign_id} - {horoscope_type})", False, f"Error: {str(e)}")
            return False

    def test_horoscope_caching(self, sign_id, horoscope_type):
        """Test that horoscopes are cached (same day requests should return same content)"""
        try:
            # First request
            response1 = requests.get(f"{self.base_url}/horoscope/{sign_id}/{horoscope_type}", timeout=60)
            if response1.status_code != 200:
                self.log_test(f"Horoscope caching test ({sign_id} - {horoscope_type})", False, "First request failed")
                return False
            
            horoscope1 = response1.json()
            
            # Second request (should be cached)
            response2 = requests.get(f"{self.base_url}/horoscope/{sign_id}/{horoscope_type}", timeout=10)
            if response2.status_code != 200:
                self.log_test(f"Horoscope caching test ({sign_id} - {horoscope_type})", False, "Second request failed")
                return False
            
            horoscope2 = response2.json()
            
            # Verify same content and ID (indicating caching)
            content_match = horoscope1.get('content') == horoscope2.get('content')
            id_match = horoscope1.get('id') == horoscope2.get('id')
            
            success = content_match and id_match
            details = f"Content match: {content_match}, ID match: {id_match}"
            
            self.log_test(
                f"Horoscope caching ({sign_id} - {horoscope_type})",
                success,
                details
            )
            return success
        except Exception as e:
            self.log_test(f"Horoscope caching ({sign_id} - {horoscope_type})", False, f"Error: {str(e)}")
            return False

    def test_invalid_sign(self):
        """Test API behavior with invalid zodiac sign"""
        try:
            response = requests.get(f"{self.base_url}/horoscope/invalid_sign/daily", timeout=10)
            success = response.status_code == 400  # Should return bad request
            
            self.log_test(
                "Invalid sign handling",
                success,
                f"Correctly rejected invalid sign",
                400,
                response.status_code
            )
            return success
        except Exception as e:
            self.log_test("Invalid sign handling", False, f"Error: {str(e)}")
            return False

    def test_invalid_type(self):
        """Test API behavior with invalid horoscope type"""
        try:
            response = requests.get(f"{self.base_url}/horoscope/aries/invalid_type", timeout=10)
            success = response.status_code in [400, 422]  # Should return validation error
            
            self.log_test(
                "Invalid type handling",
                success,
                f"Correctly rejected invalid type",
                "400 or 422",
                response.status_code
            )
            return success
        except Exception as e:
            self.log_test("Invalid type handling", False, f"Error: {str(e)}")
            return False

def main():
    print("🔮 Starting Daily Horoscope API Tests")
    print("=" * 50)
    
    tester = HoroscopeAPITester()
    
    # Test 1: Root endpoint
    print("\n📌 Testing basic connectivity...")
    root_works = tester.test_root_endpoint()
    
    # Test 2: Zodiac signs
    print("\n📌 Testing zodiac signs...")
    signs_works, signs = tester.test_zodiac_signs()
    
    if not signs_works:
        print("❌ Cannot proceed without signs endpoint working")
        print(f"\n📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
        return 1
    
    # Test 3: Horoscope generation for different types
    print("\n📌 Testing horoscope generation (using GPT-5.2)...")
    test_sign = "aries"  # Use first sign for testing
    
    # Test all three types
    for horoscope_type in ["daily", "weekly", "monthly"]:
        print(f"\n   Testing {horoscope_type} horoscope...")
        tester.test_horoscope_generation(test_sign, horoscope_type)
    
    # Test 4: Caching functionality
    print("\n📌 Testing horoscope caching...")
    tester.test_horoscope_caching(test_sign, "daily")
    
    # Test 5: Error handling
    print("\n📌 Testing error handling...")
    tester.test_invalid_sign()
    tester.test_invalid_type()
    
    # Results
    print("\n" + "=" * 50)
    success_rate = (tester.tests_passed / tester.tests_run) * 100
    print(f"📊 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed ({success_rate:.1f}%)")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All backend tests passed! API is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the details above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())