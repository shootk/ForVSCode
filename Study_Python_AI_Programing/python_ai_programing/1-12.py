from sklearn import datasets
home_prices = datasets.load_boston()
print(home_prices.target)
digits = datasets.load_digits()
print(digits.images[4])