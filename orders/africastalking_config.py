# api/africastalking_config.py
import africastalking

# Initialize SDK
USERNAME = "sandbox"  
API_KEY = "atsk_f54b2d29acc220fb26db61768e76d18c78c0dc18fc481bcd0ce29e788020e8f6fb66a291"
africastalking.initialize(USERNAME, API_KEY)
sms = africastalking.SMS
