# Test 3

# Import libraries
import math
from collections import Counter
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from multiprocessing import Pool
from deap import base, creator, tools, algorithms
from scipy.optimize import dual_annealing
from skopt import gp_minimize
from skopt.space import Integer
import pandas as pd

# Mixing and pruning for sequence generation
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

# Generate pseudorandom sequence of secrets
def generate_secret_sequence(initial_secret, steps):
    secret = initial_secret
    sequence = []
    for _ in range(steps):
        sequence.append(secret)
        secret = mix_and_prune(secret, 64, "multiply")
        secret = mix_and_prune(secret, 32, "divide")
        secret = mix_and_prune(secret, 2048, "multiply")
    return sequence

# Calculate entropy of prices
def calculate_entropy(prices):
    if not prices:
        return 0.0
    counts = Counter(prices)
    total = sum(counts.values())
    entropy = -sum((count / total) * math.log2(count / total) for count in counts.values())
    return entropy

# Generate features and labels for ML
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

# Train and evaluate ML models
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

# Predict the sum of 2000th secret numbers
def predict_2000th_sum(input_file, model):
    with open(input_file, "r") as file:
        secrets = [int(line.strip()) for line in file if line.strip()]
    features, _ = generate_features_and_labels(secrets)
    predictions = model.predict(features)
    return int(np.sum(predictions))

# Parallelized sequence search
def sequence_search_worker(args):
    secret, steps = args
    secret_sequence = generate_secret_sequence(secret, steps)
    prices = [s % 10 for s in secret_sequence]
    price_changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]

    best_sequence = None
    max_bananas = 0

    for i in range(len(price_changes) - 3):
        sequence = tuple(price_changes[i:i + 4])
        bananas = prices[i + 4]
        if bananas > max_bananas:
            best_sequence = sequence
            max_bananas = bananas

    return best_sequence, max_bananas

def find_best_sequence_parallel(input_file, steps=2000):
    with open(input_file, "r") as file:
        initial_secrets = [int(line.strip()) for line in file if line.strip()]

    with Pool(processes=8) as pool:  # Adjust processes based on your CPU
        results = pool.map(sequence_search_worker, [(secret, steps) for secret in initial_secrets])

    best_sequence, max_bananas = max(results, key=lambda x: x[1])
    print(f"Best sequence (parallel): {best_sequence}, Bananas: {max_bananas}")
    return best_sequence, max_bananas

# Genetic algorithm optimization
def evaluate_sequence(sequence, secrets, steps):
    total_bananas = 0
    for secret in secrets:
        secret_sequence = generate_secret_sequence(secret, steps)
        prices = [s % 10 for s in secret_sequence]
        price_changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
        for i in range(len(price_changes) - 3):
            if tuple(price_changes[i:i + 4]) == tuple(sequence):
                total_bananas += prices[i + 4]
                break
    return total_bananas,

def genetic_algorithm_optimization(secrets, steps=2000):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("attr_change", lambda: np.random.randint(-9, 10))
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_change, n=4)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate_sequence, secrets=secrets, steps=steps)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low=-9, up=9, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=100)
    algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, verbose=True)
    best_individual = tools.selBest(population, k=1)[0]
    return best_individual, evaluate_sequence(best_individual, secrets, steps)

# Simulated annealing optimization
def sequence_objective(sequence, secrets, steps):
    total_bananas = 0
    for secret in secrets:
        secret_sequence = generate_secret_sequence(secret, steps)
        prices = [s % 10 for s in secret_sequence]
        price_changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
        for i in range(len(price_changes) - 3):
            if tuple(price_changes[i:i + 4]) == tuple(sequence):
                total_bananas += prices[i + 4]
                break
    return -total_bananas

def simulated_annealing_optimization(secrets, steps=2000):
    bounds = [(-9, 9)] * 4
    result = dual_annealing(sequence_objective, bounds, args=(secrets, steps))
    return result.x, -result.fun

# Bayesian optimization
def bayesian_objective(sequence):
    return -sequence_objective(sequence, secrets, steps=2000)

def bayesian_optimization(secrets):
    space = [Integer(-9, 9) for _ in range(4)]
    result = gp_minimize(bayesian_objective, space, n_calls=50, random_state=42)
    return result.x, -result.fun

# Plot model performance
def plot_model_performance(results):
    models = list(results.keys())
    r2_scores = [results[model]["R2"] for model in models]

    plt.figure(figsize=(10, 6))
    plt.bar(models, r2_scores, color="skyblue")
    plt.title("Model Performance: R^2 Scores")
    plt.ylabel("R^2 Score")
    plt.xlabel("Model")
    plt.show()

# Summarize and display results
def summarize_results(ml_results, sequence_results):
    ml_metrics = pd.DataFrame(ml_results).T
    sequence_metrics = pd.DataFrame(sequence_results).T

    print("\n=== ML Performance Metrics ===")
    print(ml_metrics)

    print("\n=== Sequence Optimization Metrics ===")
    print(sequence_metrics)

# Main script
if __name__ == "__main__":
    input_file = "input.txt"

    # Load and preprocess data
    with open(input_file, "r") as file:
        training_secrets = [int(line.strip()) for line in file if line.strip()]
    features, labels = generate_features_and_labels(training_secrets)

    # Train and evaluate models
    results, X_train, X_test, y_train, y_test = train_and_evaluate_models(features, labels)

    # Select best model
    best_model_name = max(results, key=lambda k: results[k]["R2"])
    best_model = results[best_model_name]["Model"]
    print(f"Best Model: {best_model_name} with R^2 Score: {results[best_model_name]['R2']:.4f}")

    # Predict sum of 2000th secret numbers
    result_part1 = predict_2000th_sum(input_file, best_model)
    print(f"The predicted sum of the 2000th secret numbers is: {result_part1}")

    # Parallel sequence search
    best_sequence_parallel, max_bananas_parallel = find_best_sequence_parallel(input_file)
    print(f"Best sequence (parallel): {best_sequence_parallel}, Bananas: {max_bananas_parallel}")

    # Genetic algorithm optimization
    best_sequence_ga, max_bananas_ga = genetic_algorithm_optimization(training_secrets)
    print(f"Best sequence (GA): {best_sequence_ga}, Bananas: {max_bananas_ga}")

    # Simulated annealing optimization
    best_sequence_sa, max_bananas_sa = simulated_annealing_optimization(training_secrets)
    print(f"Best sequence (SA): {best_sequence_sa}, Bananas: {max_bananas_sa}")

    # Bayesian optimization
    best_sequence_bo, max_bananas_bo = bayesian_optimization(training_secrets)
    print(f"Best sequence (Bayesian): {best_sequence_bo}, Bananas: {max_bananas_bo}")

    # Summarize results
    sequence_results = {
        "Parallel Search": {"Best Sequence": best_sequence_parallel, "Bananas": max_bananas_parallel},
        "Genetic Algorithm": {"Best Sequence": best_sequence_ga, "Bananas": max_bananas_ga},
        "Simulated Annealing": {"Best Sequence": best_sequence_sa, "Bananas": max_bananas_sa},
        "Bayesian Optimization": {"Best Sequence": best_sequence_bo, "Bananas": max_bananas_bo},
    }
    summarize_results(results, sequence_results)

    # Plot model performance
    plot_model_performance(results)

