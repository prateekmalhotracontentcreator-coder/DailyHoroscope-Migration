import requests
import sys
import json
from datetime import datetime

class HoroscopeAPITester:
    def __init__(self, base_url="https://cosmic-reports-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"
        self.session_token = None
        self.session_cookies = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_user_email = f"test_{datetime.now().strftime('%H%M%S')}@example.com"
        self.test_user_password = "TestPass123!"
        self.test_user_name = "Test User"

    def log_test(self, test_name, success, details=""):
        """Log test results"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name} - PASSED {details}")
        else:
            print(f"❌ {test_name} - FAILED {details}")
        return success

    def test_api_root(self):
        """Test API root endpoint"""
        try:
            response = requests.get(f"{self.api_base}/", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success and response.json():
                details += f", Response: {response.json()}"
            return self.log_test("API Root Endpoint", success, details)
        except Exception as e:
            return self.log_test("API Root Endpoint", False, f"Error: {str(e)}")

    def test_user_registration(self):
        """Test user registration endpoint"""
        try:
            data = {
                "email": self.test_user_email,
                "password": self.test_user_password,
                "name": self.test_user_name
            }
            response = requests.post(f"{self.api_base}/auth/register", json=data, timeout=15)
            success = response.status_code == 200
            
            if success:
                user_data = response.json()
                self.session_cookies = response.cookies
                details = f"Status: {response.status_code}, User created: {user_data.get('email')}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
                
            return self.log_test("User Registration", success, details)
        except Exception as e:
            return self.log_test("User Registration", False, f"Error: {str(e)}")

    def test_user_login(self):
        """Test user login endpoint"""
        try:
            data = {
                "email": self.test_user_email,
                "password": self.test_user_password
            }
            response = requests.post(f"{self.api_base}/auth/login", json=data, timeout=15)
            success = response.status_code == 200
            
            if success:
                user_data = response.json()
                self.session_cookies = response.cookies
                details = f"Status: {response.status_code}, Logged in: {user_data.get('email')}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
                
            return self.log_test("User Login", success, details)
        except Exception as e:
            return self.log_test("User Login", False, f"Error: {str(e)}")

    def test_get_current_user(self):
        """Test get current user endpoint"""
        try:
            response = requests.get(f"{self.api_base}/auth/me", cookies=self.session_cookies, timeout=10)
            success = response.status_code == 200
            
            if success:
                user_data = response.json()
                details = f"Status: {response.status_code}, User: {user_data.get('email')}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
                
            return self.log_test("Get Current User", success, details)
        except Exception as e:
            return self.log_test("Get Current User", False, f"Error: {str(e)}")

    def test_logout(self):
        """Test logout endpoint"""
        try:
            response = requests.post(f"{self.api_base}/auth/logout", cookies=self.session_cookies, timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                self.session_cookies = None
                
            return self.log_test("User Logout", success, details)
        except Exception as e:
            return self.log_test("User Logout", False, f"Error: {str(e)}")

    def test_zodiac_signs(self):
        """Test zodiac signs endpoint"""
        try:
            response = requests.get(f"{self.api_base}/signs", timeout=10)
            success = response.status_code == 200
            
            if success:
                signs = response.json()
                details = f"Status: {response.status_code}, Signs count: {len(signs)}"
                if len(signs) != 12:
                    success = False
                    details += " (Expected 12 signs)"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
                
            return self.log_test("Zodiac Signs API", success, details)
        except Exception as e:
            return self.log_test("Zodiac Signs API", False, f"Error: {str(e)}")

    def test_horoscope_generation(self):
        """Test horoscope generation for different types"""
        types = ["daily", "weekly", "monthly"]
        sign = "aries"
        
        for horo_type in types:
            try:
                response = requests.get(f"{self.api_base}/horoscope/{sign}/{horo_type}", timeout=30)
                success = response.status_code == 200
                
                if success:
                    horoscope = response.json()
                    details = f"Status: {response.status_code}, Type: {horo_type}, Length: {len(horoscope.get('content', ''))}"
                else:
                    details = f"Status: {response.status_code}, Error: {response.text}"
                    
                self.log_test(f"Horoscope Generation ({horo_type})", success, details)
            except Exception as e:
                self.log_test(f"Horoscope Generation ({horo_type})", False, f"Error: {str(e)}")

    def test_birth_profile_creation(self):
        """Test birth profile creation"""
        try:
            data = {
                "name": "Test Profile",
                "date_of_birth": "1990-01-15",
                "time_of_birth": "10:30 AM",
                "location": "Mumbai, India"
            }
            response = requests.post(f"{self.api_base}/profile/birth", json=data, timeout=15)
            success = response.status_code == 200
            
            if success:
                profile = response.json()
                self.test_profile_id = profile.get('id')
                details = f"Status: {response.status_code}, Profile ID: {self.test_profile_id}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
                
            return self.log_test("Birth Profile Creation", success, details)
        except Exception as e:
            return self.log_test("Birth Profile Creation", False, f"Error: {str(e)}")

    def test_birth_chart_generation(self):
        """Test birth chart generation (FIXED - timeout parameter removed)"""
        if not hasattr(self, 'test_profile_id'):
            return self.log_test("Birth Chart Generation", False, "No profile ID available")
            
        try:
            data = {"profile_id": self.test_profile_id}
            response = requests.post(f"{self.api_base}/birthchart/generate", json=data, timeout=90)
            success = response.status_code == 200
            
            if success:
                chart = response.json()
                details = f"Status: {response.status_code}, Chart ID: {chart.get('id')}, Content length: {len(chart.get('report_content', ''))}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
                
            return self.log_test("Birth Chart Generation", success, details)
        except Exception as e:
            return self.log_test("Birth Chart Generation", False, f"Error: {str(e)}")

    def test_kundali_milan_generation(self):
        """Test Kundali Milan generation"""
        try:
            # Create two profiles
            profile1_data = {
                "name": "Person 1",
                "date_of_birth": "1990-01-15",
                "time_of_birth": "10:30 AM",
                "location": "Mumbai, India"
            }
            profile2_data = {
                "name": "Person 2", 
                "date_of_birth": "1992-05-20",
                "time_of_birth": "02:15 PM",
                "location": "Delhi, India"
            }
            
            profile1_response = requests.post(f"{self.api_base}/profile/birth", json=profile1_data, timeout=15)
            profile2_response = requests.post(f"{self.api_base}/profile/birth", json=profile2_data, timeout=15)
            
            if profile1_response.status_code != 200 or profile2_response.status_code != 200:
                return self.log_test("Kundali Milan Generation", False, "Failed to create profiles")
            
            person1_id = profile1_response.json().get('id')
            person2_id = profile2_response.json().get('id')
            
            # Generate Kundali Milan
            data = {
                "person1_id": person1_id,
                "person2_id": person2_id
            }
            response = requests.post(f"{self.api_base}/kundali-milan/generate", json=data, timeout=90)
            success = response.status_code == 200
            
            if success:
                milan = response.json()
                score = milan.get('compatibility_score', 0)
                details = f"Status: {response.status_code}, Score: {score}/36, Analysis length: {len(milan.get('detailed_analysis', ''))}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
                
            return self.log_test("Kundali Milan Generation", success, details)
        except Exception as e:
            return self.log_test("Kundali Milan Generation", False, f"Error: {str(e)}")

    def test_payment_intent_creation(self):
        """Test payment intent creation"""
        try:
            data = {
                "report_type": "birth_chart",
                "report_id": "test_report_123",
                "user_email": self.test_user_email
            }
            response = requests.post(f"{self.api_base}/payment/create-intent", json=data, timeout=15)
            success = response.status_code == 200
            
            if success:
                intent = response.json()
                details = f"Status: {response.status_code}, Amount: ${intent.get('amount')}"
            else:
                details = f"Status: {response.status_code}, Error: {response.text}"
                
            return self.log_test("Payment Intent Creation", success, details)
        except Exception as e:
            return self.log_test("Payment Intent Creation", False, f"Error: {str(e)}")

    def run_all_tests(self):
        """Run all API tests"""
        print("🧪 Starting Horoscope API Tests...")
        print("=" * 60)
        
        # Test basic API
        self.test_api_root()
        self.test_zodiac_signs()
        
        # Test authentication flow
        self.test_user_registration()
        self.test_user_login()
        self.test_get_current_user()
        
        # Test horoscope functionality  
        self.test_horoscope_generation()
        
        # Test birth profiles and reports
        self.test_birth_profile_creation()
        self.test_birth_chart_generation()
        self.test_kundali_milan_generation()
        
        # Test payment system
        self.test_payment_intent_creation()
        
        # Test logout
        self.test_logout()
        
        print("=" * 60)
        print(f"📊 Final Results: {self.tests_passed}/{self.tests_run} tests passed")
        print(f"🎯 Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        return self.tests_passed == self.tests_run

def main():
    """Main test execution"""
    tester = HoroscopeAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ ALL TESTS PASSED! Backend APIs are working correctly.")
        return 0
    else:
        print(f"\n❌ SOME TESTS FAILED. {tester.tests_passed}/{tester.tests_run} passed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())