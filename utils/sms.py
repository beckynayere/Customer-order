import africastalking

africastalking.initialize('sandbox', 'your_api_key')
sms = africastalking.SMS

def send_sms_alert(phone_number, message):
    sms.send(message, [phone_number])