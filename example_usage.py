from client import AntColonyOptimizer

def main():
    dist = [
        [0, 2, 9, 10],
        [2, 0, 6, 4],
        [9, 6, 0, 8],
        [10, 4, 8, 0]
    ]
    aco = AntColonyOptimizer(num_ants=8)
    res = aco.solve_tsp(dist, iterations=25)
    print("Ant Colony Optimization Verification:")
    print(f"Optimal Distance: {res['best_distance']}")
    print(f"Optimal Tour: {res['best_tour']}")

if __name__ == "__main__":
    main()
