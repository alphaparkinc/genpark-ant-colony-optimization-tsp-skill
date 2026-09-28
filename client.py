"""Ant Colony Optimization (ACO) for Traveling Salesperson Problem
100% Python Standard Library (random).
"""

import random

class AntColonyOptimizer:
    """Pheromone-guided combinatorial path search engine."""
    def __init__(self, num_ants=10, alpha=1.0, beta=2.0, rho=0.1, q_val=100.0):
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q_val = q_val

    def solve_tsp(self, distance_matrix, iterations=30):
        n = len(distance_matrix)
        pheromones = [[1.0 for _ in range(n)] for _ in range(n)]
        best_tour = None
        best_dist = float('inf')

        for _ in range(iterations):
            all_tours = []
            for ant in range(self.num_ants):
                start = random.randint(0, n - 1)
                tour = [start]
                unvisited = set(range(n)) - {start}

                while unvisited:
                    curr = tour[-1]
                    probs = []
                    denom = 0.0
                    for nxt in unvisited:
                        d = max(1e-5, distance_matrix[curr][nxt])
                        p_val = (pheromones[curr][nxt] ** self.alpha) * ((1.0 / d) ** self.beta)
                        probs.append((nxt, p_val))
                        denom += p_val
                    r = random.uniform(0, denom)
                    cum = 0.0
                    chosen = list(unvisited)[0]
                    for nxt, p_val in probs:
                        cum += p_val
                        if cum >= r:
                            chosen = nxt
                            break
                    tour.append(chosen)
                    unvisited.remove(chosen)

                dist = sum(distance_matrix[tour[i]][tour[(i + 1) % n]] for i in range(n))
                all_tours.append((tour, dist))
                if dist < best_dist:
                    best_dist = dist
                    best_tour = tour

            for i in range(n):
                for j in range(n):
                    pheromones[i][j] *= (1.0 - self.rho)

            for tour, dist in all_tours:
                deposit = self.q_val / max(1e-5, dist)
                for i in range(n):
                    u, v = tour[i], tour[(i + 1) % n]
                    pheromones[u][v] += deposit
                    pheromones[v][u] += deposit

        return {
            "best_tour": best_tour,
            "best_distance": round(best_dist, 4)
        }
