def calculate_total(array):
    total = 0
    for order in array:
        total += (order.product.price * order.quantity)
    return total