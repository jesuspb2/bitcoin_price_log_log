import boto3
from twilio.rest import Client
from bitcoin_price_common import define_object_bitcoin
from indicators.cycle_pi_indicator import (calculate_pi_cycle_indicator,
                                           find_pi_cycle_crossovers,
                                           proximity_indicator)


# AWS Systems Manager
def get_parameter(param_name):
    ssm = boto3.client('ssm', region_name='us-west-2')
    parameter = ssm.get_parameter(Name=param_name, WithDecryption=True)
    return parameter['Parameter']['Value']


my_phone_number = get_parameter('my_phone_number')
twilio_account_id = get_parameter('twilio_account_id')
twilio_auth_token = get_parameter('twilio_auth_token')
twilio_phone_number = get_parameter('twilio_phone_number')


# AWS Lambda
def lambda_handler(event, context):

    df_combined_data = define_object_bitcoin()
    df_combined_data = calculate_pi_cycle_indicator(df_combined_data)
    crossover_points = find_pi_cycle_crossovers(df_combined_data)
    last_day_proximity = proximity_indicator(df_combined_data)
    client = Client(twilio_account_id, twilio_auth_token)

    def send_twilio_message(body):
        message = client.messages.create(
            body=body,
            from_=twilio_phone_number,
            to=my_phone_number
        )
        print(f"Message sent with SID: {message.sid}")

    if len(crossover_points) == 9:
        send_twilio_message(last_day_proximity)
    else:
        send_twilio_message("New Pi Cycle Top!!! GO!!! https://www.lookintobitcoin.com/charts/pi-cycle-top-indicator/")
        send_twilio_message(last_day_proximity)

    return {
        'statusCode': 200,
        'body': {
            'message': 'Process completed successfully.'
        }
    }