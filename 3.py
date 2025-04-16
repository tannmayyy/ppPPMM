def convert_to_camel_case(input_list):
    return ['_'.join(part.capitalize() for part in item.lower().split('_')) for item in input_list]

# Example input
input_strings = ["PERSON_ID", "TRADE_ID", "CUSTOMER_ACCOUNT_NUMBER"]
converted_strings = convert_to_camel_case(input_strings)

print(converted_strings)