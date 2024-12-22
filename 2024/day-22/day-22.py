import math
from collections import Counter
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

def mix_and_prune(secret, value, operation):
    if operation == "multiply":
        result = secret * value
    elif operation == "divide":
        result = secret // value
    else:
        raise ValueError("Invalid operation. Use 'multiply' or 'divide'.")
    mixed = result ^ secret
    pruned = mixed % 16777216
    return pruned

def generate_secret_sequence(initial_secret, steps):
    secret = initial_secret
    sequence = []
    for _ in range(steps):
        sequence.append(secret)
        secret = mix_and_prune(secret, 64, "multiply")
        secret = mix_and_prune(secret, 32, "divide")
        secret = mix_and_prune(secret, 2048, "multiply")
    return sequence

def calculate_entropy(prices):
    if not prices:
        return 0.0
    counts = Counter(prices)
    total = sum(counts.values())
    entropy = -sum((count / total) * math.log2(count / total) for count in counts.values())
    return entropy

def generate_features_and_labels(secrets, steps=2000):
    features = []
    labels = []
    for secret in secrets:
        sequence = generate_secret_sequence(secret, steps)
        labels.append(sequence[-1])
        modulo_prices = [s % 10 for s in sequence]
        entropy = calculate_entropy(modulo_prices)
        features.append([
            secret, 
            len(str(secret)), 
            secret % 2, 
            entropy,
            np.mean(modulo_prices),
            np.var(modulo_prices),
            np.max(modulo_prices),
            np.min(modulo_prices),
            sum(int(d) for d in str(secret))  # Sum of digits in the secret
        ])
    return np.array(features), np.array(labels)

def train_and_evaluate_models(features, labels):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    models = {
        "RandomForest": RandomForestRegressor(n_estimators=500, max_depth=10, random_state=42),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=200, learning_rate=0.05, max_depth=7, random_state=42),
        "SVR": SVR(kernel="rbf", C=1e3, gamma=0.1),
    }

    results = {}

    for model_name, model in models.items():
        print(f"Training {model_name}...")
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        results[model_name] = {
            "Model": model,
            "MAE": mae,
            "R2": r2,
        }

        print(f"{model_name} - R^2 Score: {r2:.4f}, Mean Absolute Error: {mae:.4f}")

    return results, X_train, X_test, y_train, y_test

def predict_2000th_sum(input_file, model):
    with open(input_file, "r") as file:
        secrets = [int(line.strip()) for line in file if line.strip()]
    features, _ = generate_features_and_labels(secrets)
    predictions = model.predict(features)
    return int(np.sum(predictions))

def find_best_sequence_optimized(input_file):
    """
    Optimized function to find the best sequence of four price changes to maximize bananas.

    Args:
        input_file (str): Path to the input file containing initial secret numbers.

    Returns:
        tuple: The best sequence and the maximum number of bananas.
    """
    with open(input_file, "r") as file:
        initial_secrets = [int(line.strip()) for line in file if line.strip()]

    best_sequence = None
    max_bananas = 0

    for secret in initial_secrets:
        secret_sequence = generate_secret_sequence(secret, 2000)
        prices = [s % 10 for s in secret_sequence]
        price_changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]

        for i in range(len(price_changes) - 3):
            sequence = tuple(price_changes[i:i + 4])
            bananas = prices[i + 4]

            if bananas > max_bananas:
                best_sequence = sequence
                max_bananas = bananas

    print(f"Best sequence debug: {best_sequence}, Bananas: {max_bananas}")
    return best_sequence, max_bananas

if __name__ == "__main__":
    input_file = "input.txt"

    # Load and preprocess data
    with open(input_file, "r") as file:
        training_secrets = [int(line.strip()) for line in file if line.strip()]
    features, labels = generate_features_and_labels(training_secrets)

    # Train and evaluate multiple models
    results, X_train, X_test, y_train, y_test = train_and_evaluate_models(features, labels)

    # Select the best model based on R^2 score
    best_model_name = max(results, key=lambda k: results[k]["R2"])
    best_model = results[best_model_name]["Model"]
    print(f"Best Model: {best_model_name} with R^2 Score: {results[best_model_name]['R2']:.4f}")

    # Predict the sum of the 2000th secret numbers
    result_part1 = predict_2000th_sum(input_file, best_model)
    print(f"The predicted sum of the 2000th secret numbers is: {result_part1}")

    # Part 2: Optimized Sequence Search
    best_sequence, max_bananas = find_best_sequence_optimized(input_file)
    print(f"The best sequence of price changes is: {best_sequence}")
    print(f"The most bananas you can get is: {max_bananas}")

