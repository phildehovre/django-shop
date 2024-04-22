def calculate_total(array):
    total = 0
    for item in array:
        total += item.product.price
    return total