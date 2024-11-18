# import africastalking

# africastalking.initialize('sandbox', 'your_api_key')
# sms = africastalking.SMS

# def send_sms_alert(phone_number, message):
#     sms.send(message, [phone_number])

import africastalking

# Initialize the Africa's Talking SDK
africastalking.initialize('sandbox', 'your_api_key')  # Replace 'your_api_key' with your actual sandbox API key.

# Create an instance of the SMS service
sms = africastalking.SMS

def send_sms_alert(phone_number, message):
    try:
        # Send the SMS
        response = sms.send(message, [phone_number])
        print(f"SMS sent successfully: {response}")
    except Exception as e:
        print(f"Error while sending SMS: {e}")

# Example usage
send_sms_alert("+254712345678", "Hello, this is a test message!")
