# Project Summary: Product Recommendation System

## What I Had to Make

For this project I had to build a small program in Python that recommends products to a customer. The idea is simple. If two customers have bought many of the same things, then one of them will probably like the other's products too. So the program finds the customer who is most similar to the chosen one and recommends what that customer has bought but the chosen one has not. If nobody is similar, it just shows the most popular product.

## How I Thought About It

Before writing any code I first broke the problem into small parts:

1. Store who bought what.
2. Find how similar two customers are.
3. Do that for every other customer and sort the results.
4. Pick the best one and find the products that are new for the chosen customer.
5. Handle the special cases (no similar customer, wrong name, empty input).

Each part became one function, so I could write and test them one by one instead of writing everything at once.

## How I Implemented It

**Storing the data:** I used a dictionary where the key is the customer name and the value is a list of products. I kept lists in the dictionary because the question asked for that, and I only change them into sets when I need to compare.

**Jaccard similarity:** This was the main formula. It is the number of common products divided by the number of all different products of both customers. In Python, sets make this very easy. `set_a & set_b` gives the common items and `set_a | set_b` gives all different items, so I just divided their lengths. I also added a check so that if both sets are empty the function returns 0 and does not divide by zero.

**Comparing with everyone:** In `calculate_scores` I loop through all the customers, skip the chosen one, and calculate the score with each of the others. I save each result as a pair like `("Bina", 0.5)` in a list. Then I sort the list so the highest score comes first.

**Making the recommendation:** After sorting, the first pair in the list is the most similar customer. I then go through that customer's products and keep only those which the chosen customer does not already have. Those are the recommended products.

**Popular product:** If the best score is 0, nobody is similar. In that case `most_popular_product` counts how many customers bought each product using a dictionary, and picks the one with the highest count.

**Checking the input:** In `main` the program first checks if the name is empty and then checks if the customer exists. I also made the search ignore capital and small letters, so typing `amit` works the same as `Amit`.

## Difficulties I Faced

- **Sorting the scores:** At first I did not know how to sort a list of pairs by the score and not by the name. After reading about it, I learned that `sort()` takes a `key`, so I wrote a small function `get_score` that gives back the second item of the pair. Then I used `reverse=True` to get the highest first.

- **Understanding the formula properly:** I confused the union and the intersection in the beginning and got wrong answers. I solved Amit and Bina by hand on paper (2 common out of 4 different = 0.50), and after that I understood it and the code matched my paper answer.

- **Divya and Bina giving 0.17:** I was not sure if the answer was right because it is a long decimal (1 divided by 6). Printing with `:.2f` rounds it to two decimal places, and then it matched the expected output.

- **The Chetan case:** This one confused me because every score is 0, so there is no "most similar" customer. I had to think about when to stop and show the popular product instead. I decided to check the best score after sorting, and if it is 0 the program prints the popular product and returns.

- **Matching names:** If the user typed a name in different letter case, the program said "not found". I fixed this by comparing both names in lowercase, and returning the real name from the dictionary so the other functions still work.

- **No new product to recommend:** I realised that sometimes the most similar customer might have nothing new to give. To avoid printing an empty line, I added a message `No new products to recommend.`

## Testing

I ran the program with all four test cases from the question: Amit, Chetan, Zara with an empty name, and Bina. I compared every output with the expected output, and they all matched. Testing by hand helped me find the small mistakes mentioned above.

## What I Learned

- How to use dictionaries, lists and sets together in one program.
- How the Jaccard similarity works and why sets are useful for it.
- How to sort a list using a key.
- Why it is better to divide a program into small functions. It was much easier to find mistakes this way.
- That checking wrong inputs is as important as the normal case.

## If I Had More Time

I would like to read the customer data from a file, let the user check many customers without restarting the program, and recommend products from more than one similar customer.
