# Product Recommendation System

A simple console-based recommendation system written in **Python 3**. It finds the customer whose purchase history is most similar to the chosen customer using **Jaccard similarity**, then recommends the products that the similar customer has bought but the chosen customer has not. If nobody is similar, it shows the most popular product instead.

**Problem Statement No:** PS 75
**Language:** Python 3
**Concepts Used:** Dictionaries, Sets, Lists, Functions

---

## Table of Contents

1. [How It Works](#how-it-works)
2. [Sample Data](#sample-data)
3. [Project Structure](#project-structure)
4. [How to Run](#how-to-run)
5. [Function-by-Function Explanation](#function-by-function-explanation)
6. [Program Flow](#program-flow)
7. [Test Cases](#test-cases)
8. [Requirements and Instructions Followed](#requirements-and-instructions-followed)
9. [Design Choices](#design-choices)
10. [Possible Improvements](#possible-improvements)

---

## How It Works

1. The user enters the name of a customer.
2. The program compares that customer's purchases with every other customer's purchases using Jaccard similarity.
3. Similarity scores are printed with two decimal places, highest first.
4. The most similar customer is picked, and the products they bought that the chosen customer has not are recommended.
5. If every similarity score is `0`, the program shows the most popular product among all customers instead.

### Jaccard Similarity

Jaccard similarity measures how much two sets overlap:

```
J(A, B) = |A ∩ B| / |A ∪ B|
```

That is: the number of **common products** divided by the number of **all different products** across both customers.

**Example (Amit vs Bina):**

- Amit: `{Laptop, Mouse, Keyboard}`
- Bina: `{Laptop, Mouse, Headphones}`
- Common: `{Laptop, Mouse}` → 2
- All different products: `{Laptop, Mouse, Keyboard, Headphones}` → 4
- Similarity = 2 / 4 = **0.50**

A score of `1.00` means identical purchases, and `0.00` means nothing in common.

---

## Sample Data

| Customer | Products Bought |
|----------|-----------------|
| Amit | Laptop, Mouse, Keyboard |
| Bina | Laptop, Mouse, Headphones |
| Chetan | Phone, Charger |
| Divya | Laptop, Keyboard, Monitor, Webcam |

The data is stored in a dictionary where each customer name maps to a list of products:

```python
purchases = {
    "Amit": ["Laptop", "Mouse", "Keyboard"],
    "Bina": ["Laptop", "Mouse", "Headphones"],
    "Chetan": ["Phone", "Charger"],
    "Divya": ["Laptop", "Keyboard", "Monitor", "Webcam"],
}
```

---

## Project Structure

```
product-recommendation-system/
│
├── recommend.py     # Complete program (single Python file)
└── README.md        # Project documentation
```

---

## How to Run

**Requirements:** Python 3.6 or above. No external libraries are needed.

```bash
python recommend.py
```

On some systems you may need:

```bash
python3 recommend.py
```

The program will ask:

```
Recommend for:
```

Type a customer name and press Enter.

---

## Function-by-Function Explanation

### 1. `purchases` (dictionary)

The data store of the program. Each key is a customer name and each value is a list of the products that customer has bought. The lists are converted to sets only when similarity needs to be calculated.

---

### 2. `jaccard_similarity(set_a, set_b)`

Calculates the Jaccard similarity between two sets of products.

| Part | Description |
|------|-------------|
| **Parameters** | `set_a`, `set_b`: two sets of products |
| **Returns** | A float between `0.0` and `1.0` |

**Steps:**
1. Builds the union of both sets using `set_a | set_b`.
2. If the union is empty, returns `0.0` to avoid dividing by zero.
3. Otherwise returns the size of the intersection (`set_a & set_b`) divided by the size of the union.

---

### 3. `find_customer(name)`

Looks for the typed name in the `purchases` dictionary, ignoring upper and lower case.

| Part | Description |
|------|-------------|
| **Parameters** | `name`: the name typed by the user |
| **Returns** | The correctly spelled customer name from the dictionary, or `None` if not found |

**Why it exists:** It lets the user type `amit`, `AMIT` or `Amit` and still get a match. The returned name is always the one stored in the dictionary, so later lookups never fail.

---

### 4. `get_score(pair)`

A tiny helper used for sorting. Each pair looks like `("Bina", 0.5)`, and this function returns the score (index `1`).

| Part | Description |
|------|-------------|
| **Parameters** | `pair`: a tuple of `(customer_name, score)` |
| **Returns** | The score from the tuple |

It is passed as the `key` to `sort()`, so the list is ordered by score instead of by name.

---

### 5. `calculate_scores(customer)`

Calculates the similarity of the chosen customer against every other customer.

| Part | Description |
|------|-------------|
| **Parameters** | `customer`: the chosen customer's name |
| **Returns** | A list of `(other_customer, score)` tuples, sorted from highest to lowest score |

**Steps:**
1. Converts the chosen customer's list of products into a set.
2. Loops over every other customer (the chosen customer is skipped).
3. Converts each other customer's products into a set and calls `jaccard_similarity`.
4. Appends `(other_customer, score)` to a list.
5. Sorts the list by score in descending order using `get_score`.

> If two customers have the same score, they stay in the order they appear in the dictionary, because Python's `sort()` is stable.

---

### 6. `most_popular_product()`

Finds the product bought by the largest number of customers. It is used as the fallback when no similar customer exists.

| Part | Description |
|------|-------------|
| **Parameters** | None |
| **Returns** | A tuple `(product_name, number_of_customers)` |

**Steps:**
1. Creates an empty dictionary called `counts`.
2. Goes through every customer's products and adds 1 to that product's count.
3. Uses `max(counts, key=counts.get)` to pick the product with the highest count.
4. Returns the product and its count.

With the sample data, `Laptop` is the most popular product (bought by Amit, Bina and Divya = 3 customers).

---

### 7. `recommend(customer)`

The main logic of the system. It prints the results for one valid customer.

| Part | Description |
|------|-------------|
| **Parameters** | `customer`: a valid customer name from the dictionary |
| **Returns** | Nothing (prints the output) |

**Steps:**
1. Calls `calculate_scores` to get the sorted scores.
2. Takes the first entry as the most similar customer.
3. **If the best score is `0`:** prints `No similar customers found.`, then prints the most popular product using `most_popular_product()` and stops.
4. **Otherwise:** prints every similarity score (two decimal places, highest first) and the most similar customer.
5. Builds a list of products the similar customer has bought that the chosen customer has not.
6. Prints `Recommended:` followed by those products. If there are none, prints `No new products to recommend.`

---

### 8. `main()`

The entry point. It takes the input and handles invalid cases before calling `recommend`.

**Steps:**
1. Reads the name using `input("Recommend for: ")` and removes extra spaces with `.strip()`.
2. If the name is empty, prints `Name cannot be empty.` and stops.
3. Calls `find_customer`. If it returns `None`, prints `Customer '<name>' not found.` and stops.
4. Otherwise calls `recommend` with the matched customer.

---

## Program Flow

```
Start
  │
  ▼
Read name from user
  │
  ├── Empty? ───────────► "Name cannot be empty."
  │
  ▼
Find customer (case-insensitive)
  │
  ├── Not found? ───────► "Customer 'X' not found."
  │
  ▼
Calculate Jaccard scores with all other customers
  │
  ├── Best score = 0? ──► "No similar customers found."
  │                       + most popular product
  ▼
Print scores (highest first) + most similar customer
  │
  ▼
Recommend products the similar customer has and this customer doesn't
  │
  ▼
End
```

---

## Test Cases

### Test Case 1: Normal Input

**Input:** `Amit`

```
Recommend for: Amit
Similarity scores:
Bina : 0.50
Divya : 0.40
Chetan : 0.00
Most similar customer: Bina
Recommended: Headphones
```

**Why:** Amit and Bina share Laptop and Mouse (2 common out of 4 different = 0.50). Bina has Headphones, which Amit has not bought.

---

### Test Case 2: Boundary / Minimum Input

**Input:** `Chetan`

```
Recommend for: Chetan
No similar customers found.
Popular product: Laptop (bought by 3 customers)
```

**Why:** Chetan (Phone, Charger) has nothing in common with anyone, so every score is 0. The program falls back to the most popular product.

---

### Test Case 3: Invalid Input

**(a) Input:** `Zara`

```
Recommend for: Zara
Customer 'Zara' not found.
```

**(b) Input:** *(empty, just press Enter)*

```
Recommend for:
Name cannot be empty.
```

---

### Test Case 4: Different Valid Scenario

**Input:** `Bina`

```
Recommend for: Bina
Similarity scores:
Amit : 0.50
Divya : 0.17
Chetan : 0.00
Most similar customer: Amit
Recommended: Keyboard
```

**Why:** Bina and Amit share Laptop and Mouse (0.50). Bina and Divya share only Laptop (1 common out of 6 different = 0.17). Amit has Keyboard, which Bina has not bought.

---

### Summary Table

| # | Type | Input | Result |
|---|------|-------|--------|
| 1 | Normal | Amit | Most similar: Bina, Recommended: Headphones |
| 2 | Boundary | Chetan | No similar customers, popular product: Laptop (3 customers) |
| 3a | Invalid | Zara | Customer 'Zara' not found. |
| 3b | Invalid | (empty) | Name cannot be empty. |
| 4 | Different valid | Bina | Most similar: Amit, Recommended: Keyboard |

---

## Requirements and Instructions Followed

### Bare Minimum Requirements

| # | Requirement | How It Is Done |
|---|-------------|----------------|
| 1 | Write the solution in Python 3 (one `.py` file) and run it from the console | The whole program is in `recommend.py` and runs with `python recommend.py` |
| 2 | Store purchases in a dictionary of lists and convert them to sets for comparison | `purchases` is a dictionary of lists, and `set(...)` is applied inside `calculate_scores` |
| 3 | Write a function to calculate Jaccard similarity | `jaccard_similarity(set_a, set_b)` |
| 4 | Show similarity scores with two decimal places, highest first | `f"{score:.2f}"` formatting and `scores.sort(key=get_score, reverse=True)` |
| 5 | Test the program with all four test cases | All four test cases are documented and verified above |

### Project Instructions

| # | Instruction | Status |
|---|-------------|--------|
| 1 | Understand the problem statement and define the problem clearly | Described in [How It Works](#how-it-works) |
| 2 | Develop the solution using proper logic and programming concepts | Dictionaries, sets, lists and functions are used |
| 3 | Implement all required features and pass the given test cases | Recommendation, fallback to popular product, and input validation are all implemented |
| 4 | Test and debug the project to ensure correct output | Verified against all four test cases |
| 5 | Prepare the documentation/report and upload the code and report to GitHub | This README and `recommend.py` are the repository contents |
| 6 | Complete and submit the project within the given deadline | Submit before the deadline |

---

## Design Choices

- **Single file:** the whole project is one `.py` file, as required.
- **Small functions:** each function does one job, which makes the code easy to read, test and change.
- **Only basic concepts:** dictionaries, sets, lists, loops and functions. No classes, lambdas or external libraries.
- **Case-insensitive names:** `amit` and `AMIT` work the same as `Amit`.
- **Lists in storage, sets in comparison:** purchases are kept as lists and turned into sets only when comparing, as the requirements ask.
- **Safe division:** `jaccard_similarity` returns `0.0` when both sets are empty instead of crashing.

---

## Possible Improvements

- Let the user keep entering names until they choose to exit.
- Load purchase data from a file (CSV or JSON) instead of hard-coding it.
- Recommend products from the top few similar customers rather than only the best one.
- Add automated tests for each test case.

---

## Author

**Name:** _Your Name_
**Roll No:** _Your Roll Number_
**Course:** B.Tech Computer Science and Engineering, First Semester
