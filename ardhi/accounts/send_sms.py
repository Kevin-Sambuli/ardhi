import africastalking

# TODO: Initialize Africa's Talking

# africastalking.initialize(
#     username='[rundalis]',
#     api_key='[1c2f60bceb80f2f8666092cd97b40dbe73a82193c0937fcfc64b2b8f95a1e1cd4]'
# )

username = 'rundalis'
api_key = '1c2f60bceb80f2f8666092cd97b40dbe73a82193c0937fcfc64b2b8f95a1e1cd4'
africastalking.initialize(username, api_key)

sms = africastalking.SMS


class send_sms:
    # sms = africastalking.SMS

    def send(self):
        # TODO: Send message
        # Set the numbers in international format
        recipients = ["+254729759023"]
        # Set your message
        message = "Hey AT Ninja!"
        # Set your shortCode or senderId
        sender = "AFRICASTALKING"
        try:
            response = self.sms.send(message, recipients, sender)
            print(response['SMSMessageData'])
        except Exception as e:
            print(f'Sambuli, we have a problem: {e}')

send_sms.send()
