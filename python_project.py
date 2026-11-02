purchases = {
    "Amit": ["Laptop", "Mouse", "Keyboard"],
    "Bina": ["Laptop", "Mouse", "Headphones"],
    "Chetan": ["Phone", "Charger"],
    "Divya": ["Laptop", "Keyboard", "Monitor", "Webcam"],
}


def jaccard_similarity(set_a, set_b):
    union = set_a | set_b
    if len(union) == 0:
        return 0.0
    return len(set_a & set_b) / len(union)


def find_customer(name):
    for customer in purchases:
        if customer.lower() == name.lower():
            return customer
    return None


def get_score(pair):
    return pair[1]


def calculate_scores(customer):
    my_products = set(purchases[customer])
    scores = []
    for other, products in purchases.items():
        if other != customer:
            score = jaccard_similarity(my_products, set(products))
            scores.append((other, score))
    scores.sort(key=get_score, reverse=True)
    return scores


def most_popular_product():
    counts = {}
    for products in purchases.values():
        for product in products:
            counts[product] = counts.get(product, 0) + 1
    best_product = max(counts, key=counts.get)
    return best_product, counts[best_product]


def recommend(customer):
    scores = calculate_scores(customer)
    best_customer, best_score = scores[0]

    if best_score == 0:
        product, count = most_popular_product()
        print("No similar customers found.")
        print(f"Popular product: {product} (bought by {count} customers)")
        return

    print("Similarity scores:")
    for other, score in scores:
        print(f"{other} : {score:.2f}")
    print(f"Most similar customer: {best_customer}")

    new_products = []
    for product in purchases[best_customer]:
        if product not in purchases[customer]:
            new_products.append(product)

    if new_products:
        print("Recommended:", ", ".join(new_products))
    else:
        print("No new products to recommend.")


def main():
    name = input("Recommend for: ").strip()

    if name == "":
        print("Name cannot be empty.")
        return

    customer = find_customer(name)
    if customer is None:
        print(f"Customer '{name}' not found.")
        return

    recommend(customer)


main()