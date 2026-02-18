"""
Backend API Tests for Daily Horoscope App
Testing: API endpoints, Razorpay payment, premium access, authentication
"""
import pytest
import requests
import os
import time

# Use the backend URL from environment
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://birth-chart-staging.preview.emergentagent.com')
API = f"{BASE_URL}/api"

# Test session token created via mongosh
TEST_SESSION_TOKEN = "test_session_1771413362301"

class TestRootAndBasicEndpoints:
    """Test basic API endpoints"""
    
    def test_root_endpoint(self):
        """Test API root returns 200"""
        response = requests.get(f"{API}/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print(f"✅ Root endpoint working: {data}")
    
    def test_zodiac_signs_endpoint(self):
        """Test zodiac signs endpoint returns all 12 signs"""
        response = requests.get(f"{API}/signs")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 12
        
        # Verify each sign has required fields
        for sign in data:
            assert "id" in sign
            assert "name" in sign
            assert "symbol" in sign
            assert "dates" in sign
            assert "element" in sign
        
        print(f"✅ Zodiac signs endpoint working: {len(data)} signs returned")


class TestHoroscopeGeneration:
    """Test horoscope generation endpoints"""
    
    def test_get_daily_horoscope_aries(self):
        """Test daily horoscope generation for Aries"""
        response = requests.get(f"{API}/horoscope/aries/daily", timeout=90)
        assert response.status_code == 200
        data = response.json()
        assert "sign" in data
        assert data["sign"] == "aries"
        assert "type" in data
        assert data["type"] == "daily"
        assert "content" in data
        assert len(data["content"]) > 50  # Should have meaningful content
        print(f"✅ Daily horoscope for Aries: {len(data['content'])} chars")
    
    def test_generate_horoscope_weekly(self):
        """Test weekly horoscope generation"""
        response = requests.post(
            f"{API}/horoscope/generate",
            json={"sign": "leo", "type": "weekly"},
            timeout=90
        )
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "weekly"
        assert len(data["content"]) > 50
        print(f"✅ Weekly horoscope generated: {len(data['content'])} chars")
    
    def test_generate_horoscope_monthly(self):
        """Test monthly horoscope generation"""
        response = requests.post(
            f"{API}/horoscope/generate",
            json={"sign": "scorpio", "type": "monthly"},
            timeout=90
        )
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "monthly"
        print(f"✅ Monthly horoscope generated: {len(data['content'])} chars")
    
    def test_invalid_zodiac_sign(self):
        """Test error handling for invalid zodiac sign"""
        response = requests.get(f"{API}/horoscope/invalid/daily")
        assert response.status_code == 400
        print("✅ Invalid zodiac sign returns 400")


class TestBirthProfile:
    """Test birth profile CRUD operations"""
    
    @pytest.fixture(scope="class")
    def test_profile(self):
        """Create a test birth profile"""
        profile_data = {
            "name": "TEST_Profile_User",
            "date_of_birth": "1990-05-15",
            "time_of_birth": "10:30",
            "location": "New Delhi, India"
        }
        response = requests.post(f"{API}/profile/birth", json=profile_data)
        assert response.status_code == 200
        data = response.json()
        print(f"✅ Created test profile: {data['id']}")
        return data
    
    def test_create_birth_profile(self, test_profile):
        """Test birth profile creation"""
        assert "id" in test_profile
        assert "name" in test_profile
        assert test_profile["name"] == "TEST_Profile_User"
        print("✅ Birth profile creation verified")
    
    def test_get_birth_profile(self, test_profile):
        """Test getting birth profile by ID"""
        profile_id = test_profile["id"]
        response = requests.get(f"{API}/profile/birth/{profile_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == profile_id
        print(f"✅ Birth profile retrieval working: {data['name']}")
    
    def test_list_birth_profiles(self):
        """Test listing all birth profiles"""
        response = requests.get(f"{API}/profile/birth")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        print(f"✅ Birth profiles list: {len(data)} profiles found")


class TestBirthChart:
    """Test birth chart generation - Premium feature"""
    
    @pytest.fixture(scope="class")
    def profile_with_chart(self):
        """Create profile and generate chart"""
        # Create profile first
        profile_data = {
            "name": "TEST_BirthChart_User",
            "date_of_birth": "1985-08-20",
            "time_of_birth": "14:45",
            "location": "Mumbai, India"
        }
        profile_response = requests.post(f"{API}/profile/birth", json=profile_data)
        profile = profile_response.json()
        return profile
    
    def test_generate_birth_chart(self, profile_with_chart):
        """Test birth chart generation with AI"""
        response = requests.post(
            f"{API}/birthchart/generate",
            json={"profile_id": profile_with_chart["id"]},
            timeout=120  # LLM generation can take time
        )
        assert response.status_code == 200
        data = response.json()
        assert "report_content" in data
        assert len(data["report_content"]) > 100
        print(f"✅ Birth chart generated: {len(data['report_content'])} chars")
    
    def test_get_birth_chart(self, profile_with_chart):
        """Test getting existing birth chart"""
        response = requests.get(f"{API}/birthchart/{profile_with_chart['id']}")
        # Should return 200 if chart exists, 404 if not
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "report_content" in data
            print(f"✅ Birth chart retrieval working")
        else:
            print("⚠️ Birth chart not found (expected if not generated yet)")


class TestKundaliMilan:
    """Test Kundali Milan compatibility report - Premium feature"""
    
    @pytest.fixture(scope="class")
    def two_profiles(self):
        """Create two test profiles for Kundali Milan"""
        profile1_data = {
            "name": "TEST_Person1",
            "date_of_birth": "1992-03-10",
            "time_of_birth": "08:00",
            "location": "Delhi, India"
        }
        profile2_data = {
            "name": "TEST_Person2",
            "date_of_birth": "1993-07-25",
            "time_of_birth": "16:30",
            "location": "Chennai, India"
        }
        
        p1_response = requests.post(f"{API}/profile/birth", json=profile1_data)
        p2_response = requests.post(f"{API}/profile/birth", json=profile2_data)
        
        return {
            "person1": p1_response.json(),
            "person2": p2_response.json()
        }
    
    def test_generate_kundali_milan(self, two_profiles):
        """Test Kundali Milan generation with AI"""
        response = requests.post(
            f"{API}/kundali-milan/generate",
            json={
                "person1_id": two_profiles["person1"]["id"],
                "person2_id": two_profiles["person2"]["id"]
            },
            timeout=120  # LLM generation can take time
        )
        assert response.status_code == 200
        data = response.json()
        assert "compatibility_score" in data
        assert "detailed_analysis" in data
        assert 0 <= data["compatibility_score"] <= 36
        print(f"✅ Kundali Milan generated: Score {data['compatibility_score']}/36")


class TestRazorpayPayment:
    """Test Razorpay payment integration - CRITICAL"""
    
    def test_create_payment_order_birth_chart(self):
        """Test Razorpay order creation for birth chart"""
        response = requests.post(
            f"{API}/payment/create-order",
            json={
                "report_type": "birth_chart",
                "report_id": "test-report-123",
                "user_email": "test@example.com"
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify Razorpay order response structure
        assert "order_id" in data
        assert "amount" in data
        assert "currency" in data
        assert "key_id" in data
        
        # Verify correct values
        assert data["amount"] == 799  # Birth chart price in INR
        assert data["currency"] == "INR"
        assert data["key_id"].startswith("rzp_test_")
        assert data["order_id"].startswith("order_")
        
        print(f"✅ Razorpay order created: {data['order_id']} for ₹{data['amount']}")
    
    def test_create_payment_order_kundali_milan(self):
        """Test Razorpay order creation for kundali milan"""
        response = requests.post(
            f"{API}/payment/create-order",
            json={
                "report_type": "kundali_milan",
                "report_id": "test-kundali-456",
                "user_email": "test@example.com"
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        assert data["amount"] == 1199  # Kundali Milan price in INR
        print(f"✅ Razorpay order for Kundali Milan: ₹{data['amount']}")
    
    def test_create_payment_order_premium_monthly(self):
        """Test Razorpay order creation for premium subscription"""
        response = requests.post(
            f"{API}/payment/create-order",
            json={
                "report_type": "premium_monthly",
                "user_email": "premium@example.com"
            }
        )
        assert response.status_code == 200
        data = response.json()
        
        assert data["amount"] == 1599  # Premium monthly price in INR
        print(f"✅ Razorpay order for Premium Monthly: ₹{data['amount']}")
    
    def test_invalid_report_type(self):
        """Test error handling for invalid report type"""
        response = requests.post(
            f"{API}/payment/create-order",
            json={
                "report_type": "invalid_type",
                "report_id": "test-123",
                "user_email": "test@example.com"
            }
        )
        assert response.status_code == 400
        print("✅ Invalid report type returns 400")


class TestPremiumAccess:
    """Test premium access check endpoint"""
    
    def test_check_premium_access_no_access(self):
        """Test premium check returns false for unpaid user"""
        response = requests.get(
            f"{API}/premium/check",
            params={
                "user_email": "free.user@example.com",
                "report_type": "birth_chart",
                "report_id": "random-123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "has_premium_access" in data
        assert data["has_premium_access"] == False
        print("✅ Premium check returns false for unpaid user")


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_user(self):
        """Test user registration with email/password"""
        import random
        random_suffix = random.randint(10000, 99999)
        email = f"test_user_{random_suffix}@example.com"
        
        response = requests.post(
            f"{API}/auth/register",
            json={
                "email": email,
                "name": f"Test User {random_suffix}",
                "password": "TestPass123!"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert data["email"] == email
        print(f"✅ User registration working: {email}")
    
    def test_login_user(self):
        """Test user login - requires existing user from register test"""
        # First register a new user
        import random
        random_suffix = random.randint(10000, 99999)
        email = f"login_test_{random_suffix}@example.com"
        password = "TestPass123!"
        
        # Register
        requests.post(
            f"{API}/auth/register",
            json={
                "email": email,
                "name": f"Login Test {random_suffix}",
                "password": password
            }
        )
        
        # Login
        response = requests.post(
            f"{API}/auth/login",
            json={
                "email": email,
                "password": password
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        print(f"✅ User login working: {email}")
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = requests.post(
            f"{API}/auth/login",
            json={
                "email": "invalid@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
        print("✅ Invalid login returns 401")
    
    def test_get_current_user_with_session(self):
        """Test getting current user with valid session cookie"""
        response = requests.get(
            f"{API}/auth/me",
            cookies={"session_token": TEST_SESSION_TOKEN}
        )
        # Should return user data or 401 if session expired
        assert response.status_code in [200, 401]
        if response.status_code == 200:
            data = response.json()
            assert "email" in data
            print(f"✅ Current user endpoint working: {data['email']}")
        else:
            print("⚠️ Session may have expired (expected behavior)")


class TestShareLinks:
    """Test share link functionality"""
    
    def test_create_share_link(self):
        """Test creating a shareable link for a report"""
        response = requests.post(
            f"{API}/share/create",
            params={
                "report_type": "birth_chart",
                "report_id": "test-share-123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert len(data["token"]) > 20
        print(f"✅ Share link created: {data['token'][:20]}...")
    
    def test_get_share_link_invalid(self):
        """Test getting non-existent share link"""
        response = requests.get(f"{API}/share/invalid_token_12345")
        assert response.status_code == 404
        print("✅ Invalid share token returns 404")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
