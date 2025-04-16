input_string = "parent_trade_id, date"
converted = ', '.join(f'"{item.strip()}"' for item in input_string.split(','))
print(converted)