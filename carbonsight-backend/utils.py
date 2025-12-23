from decimal import Decimal

def floats_to_decimal(arr):
    """
    Convert a list of Python floats into Decimal so DynamoDB can store them.
    """
    return [Decimal(str(x)) for x in arr]
