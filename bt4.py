import random, math, time
from typing import List, Tuple, Dict, Any
from simpleai.search import CspProblem, backtrack
from simpleai.search.csp import MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE

class NQueensBase:
    def __init__(self, n: int = 5):
        self.n = n
    def conflicts(self, state: List[int]) -> int:
        """Đếm số cặp quân hậu tấn công nhau"""
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if (state[i] == state[j] or 
                    abs(state[i] - state[j]) == abs(i - j)): #cùng hàng hoặc cùng dường chéo
                    conflicts += 1
        return conflicts
    def print_board(self, state: List[int]):
        """In bàn cờ N-Queens"""
        print(f"\nBàn cờ {self.n}-Queens:")
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                line += "Q " if state[col] == row else ". "
            print(line)
        print()

class NQueensCSP(NQueensBase):
    def __init__(self, n: int = 5):
        super().__init__(n)
        self.variables = [f'Q{i}' for i in range(n)]
        self.domains = {var: list(range(n)) for var in self.variables}
        self.assignments_count = 0
        self.backtracks_count = 0
    def queens_constraint(self, variables_tuple, values_tuple):
        """Constraint: Hai quân hậu không được tấn công nhau"""
        var1, var2 = variables_tuple
        row1, row2 = values_tuple
        
        # Lấy cột từ tên biến (Q0 -> cột 0, Q1 -> cột 1, ...)
        col1 = int(var1[1:])
        col2 = int(var2[1:])
        # Kiểm tra không cùng hàng và không cùng đường chéo
        return (row1 != row2 and 
                abs(row1 - row2) != abs(col1 - col2))
    def create_csp_problem(self):
        """Tạo CSP problem với tất cả constraints"""
        constraints = []
        # Tạo constraint cho mọi cặp quân hậu
        for i in range(self.n):
            for j in range(i + 1, self.n):
                constraints.append(((f'Q{i}', f'Q{j}'), self.queens_constraint))
        
        return CspProblem(self.variables, self.domains, constraints)
    
    def value_ordering_function(self, csp, variable, assignment):
        """
        Value Ordering Function: Sắp xếp giá trị theo hàm value
        Ưu tiên giá trị có ít conflicts nhất với các biến chưa được gán
        """
        values_with_scores = []
        
        for value in csp.domains[variable]:
            # Tính điểm cho giá trị này
            score = self.calculate_value_score(csp, variable, value, assignment)
            values_with_scores.append((value, score))
        
        # Sắp xếp theo điểm giảm dần (điểm cao = ít conflicts)
        values_with_scores.sort(key=lambda x: x[1], reverse=True)
        return [value for value, _ in values_with_scores]
    
    def calculate_value_score(self, csp, variable, value, assignment):
        """
        Tính điểm cho một giá trị:
        - Điểm cao: ít conflicts với các biến chưa gán
        - Có thêm yếu tố ưu tiên vị trí trung tâm
        """
        score = 0
        current_col = int(variable[1:])
        
        # Yếu tố 1: Đếm số giá trị khả dụng trong domain của các biến chưa gán
        unassigned_vars = [var for var in csp.variables if var not in assignment]
        
        for other_var in unassigned_vars:
            if other_var == variable:
                continue
                
            other_col = int(other_var[1:])
            available_values = 0
            
            # Đếm số giá trị trong domain của other_var không conflict với value hiện tại
            for other_value in csp.domains[other_var]:
                if self.queens_constraint((variable, other_var), (value, other_value)):
                    available_values += 1
            
            score += available_values
        
        # Yếu tố 2: Ưu tiên vị trí gần trung tâm (bonus nhỏ)
        center = self.n // 2
        center_bonus = 1.0 / (1.0 + abs(value - center))
        score += center_bonus * 0.1
        
        return score

class NQueensOptimization(NQueensBase):
    """Base class cho các thuật toán tối ưu với Value Ordering"""
    def __init__(self, n: int = 5):
        self.n = n
    
    def value_function(self, state: List[int]) -> float:
        """
        Value Function: Đánh giá chất lượng của một trạng thái
        Giá trị cao = trạng thái tốt (ít conflicts)
        """
        max_pairs = self.n * (self.n - 1) // 2  # Số cặp tối đa
        current_conflicts = self.conflicts(state)
        return max_pairs - current_conflicts

class HillClimbingWithValueOrdering(NQueensOptimization):
    """Hill Climbing với Value Ordering"""
    
    def solve(self, max_iterations: int = 1000) -> Tuple[List[int], int, int]:
        current = self.generate_initial_state_with_value_ordering()
        current_value = self.value_function(current)
        
        for iteration in range(max_iterations):
            if self.conflicts(current) == 0:
                return current, self.conflicts(current), iteration
            
            # Tìm neighbor tốt nhất sử dụng value ordering
            best_neighbor = self.get_best_neighbor_with_ordering(current)
            best_value = self.value_function(best_neighbor)
            
            if best_value <= current_value:
                break  # Local maximum
            
            current = best_neighbor
            current_value = best_value
        
        return current, self.conflicts(current), iteration
    
    def generate_initial_state_with_value_ordering(self) -> List[int]:
        """Tạo trạng thái ban đầu sử dụng value ordering"""
        state = [0] * self.n
        
        for col in range(self.n):
            # Tính điểm cho mỗi vị trí có thể
            position_scores = []
            for row in range(self.n):
                temp_state = state.copy()
                temp_state[col] = row
                score = self.value_function(temp_state)
                position_scores.append((row, score))
            
            # Sắp xếp theo điểm và chọn trong top 3
            position_scores.sort(key=lambda x: x[1], reverse=True)
            top_positions = position_scores[:3]
            
            # Chọn ngẫu nhiên trong top positions
            chosen_row = random.choice(top_positions)[0]
            state[col] = chosen_row
        
        return state
    
    def get_best_neighbor_with_ordering(self, state: List[int]) -> List[int]:
        """Tìm neighbor tốt nhất với value ordering"""
        neighbors_with_values = []
        
        for col in range(self.n):
            for row in range(self.n):
                if row != state[col]:
                    neighbor = state.copy()
                    neighbor[col] = row
                    value = self.value_function(neighbor)
                    neighbors_with_values.append((neighbor, value))
        
        if not neighbors_with_values:
            return state
        
        # Sắp xếp theo value và trả về neighbor tốt nhất
        neighbors_with_values.sort(key=lambda x: x[1], reverse=True)
        return neighbors_with_values[0][0]

class SimulatedAnnealingWithValueOrdering(NQueensOptimization):
    """Simulated Annealing với Value Ordering"""
    
    def solve(self, initial_temp: float = 100, cooling_rate: float = 0.95, 
              min_temp: float = 0.01) -> Tuple[List[int], int, int]:
        current = self.generate_initial_state_with_value_ordering()
        current_value = self.value_function(current)
        
        temperature = initial_temp
        iteration = 0
        
        while temperature > min_temp:
            if self.conflicts(current) == 0:
                return current, self.conflicts(current), iteration
            
            # Tạo neighbor sử dụng value-based selection
            neighbor = self.get_neighbor_with_value_ordering(current, temperature)
            neighbor_value = self.value_function(neighbor)
            
            # Acceptance probability
            delta = neighbor_value - current_value
            if delta > 0 or random.random() < math.exp(delta / temperature):
                current = neighbor
                current_value = neighbor_value
            
            temperature *= cooling_rate
            iteration += 1
        
        return current, self.conflicts(current), iteration
    
    def generate_initial_state_with_value_ordering(self) -> List[int]:
        """Tương tự Hill Climbing"""
        return HillClimbingWithValueOrdering(self.n).generate_initial_state_with_value_ordering()
    
    def get_neighbor_with_value_ordering(self, state: List[int], temperature: float) -> List[int]:
        """Tạo neighbor với bias theo value function"""
        neighbor = state.copy()
        col = random.randint(0, self.n - 1)
        
        # Tính xác suất cho mỗi hàng
        row_probabilities = []
        for row in range(self.n):
            temp_state = state.copy()
            temp_state[col] = row
            value = self.value_function(temp_state)
            # Probability tỷ lệ thuận với value và temperature
            prob = math.exp(value / max(temperature, 0.1))
            row_probabilities.append((row, prob))
        
        # Chuẩn hóa xác suất
        total_prob = sum(prob for _, prob in row_probabilities)
        if total_prob > 0:
            normalized_probs = [(row, prob / total_prob) for row, prob in row_probabilities]
            
            # Chọn hàng dựa trên xác suất
            rand_val = random.random()
            cumulative = 0
            for row, prob in normalized_probs:
                cumulative += prob
                if rand_val <= cumulative:
                    neighbor[col] = row
                    break
        else:
            neighbor[col] = random.randint(0, self.n - 1)
        
        return neighbor

class GeneticAlgorithmWithValueOrdering(NQueensOptimization):
    """Genetic Algorithm với Value Ordering"""
    def __init__(self, n: int = 5, population_size: int = 50):
        super().__init__(n)
        self.population_size = population_size
    
    def solve(self, generations: int = 500) -> Tuple[List[int], int, int]:
        # Tạo population ban đầu sử dụng value ordering
        population = self.create_initial_population_with_ordering()
        
        max_fitness = self.n * (self.n - 1) // 2
        
        for generation in range(generations):
            fitnesses = [self.value_function(individual) for individual in population]
            
            # Kiểm tra nghiệm
            best_fitness = max(fitnesses)
            if best_fitness == max_fitness:
                best_individual = population[fitnesses.index(best_fitness)]
                return best_individual, self.conflicts(best_individual), generation
            
            # Tạo thế hệ mới
            new_population = []
            for _ in range(self.population_size // 2):
                parent1 = self.selection_with_value_ordering(population, fitnesses)
                parent2 = self.selection_with_value_ordering(population, fitnesses)
                
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate_with_value_ordering(child1)
                child2 = self.mutate_with_value_ordering(child2)
                
                new_population.extend([child1, child2])
            
            population = new_population[:self.population_size]
        
        fitnesses = [self.value_function(individual) for individual in population]
        best_individual = population[fitnesses.index(max(fitnesses))]
        return best_individual, self.conflicts(best_individual), generations
    
    def create_initial_population_with_ordering(self) -> List[List[int]]:
        """Tạo population ban đầu với value ordering"""
        population = []
        hc_helper = HillClimbingWithValueOrdering(self.n)
        
        for _ in range(self.population_size):
            individual = hc_helper.generate_initial_state_with_value_ordering()
            population.append(individual)
        
        return population
    
    def selection_with_value_ordering(self, population: List[List[int]], fitnesses: List[float]) -> List[int]:
        """Tournament selection với bias theo value"""
        tournament_size = 3
        tournament_indices = random.sample(range(len(population)), 
                                         min(tournament_size, len(population)))
        tournament = [(population[i], fitnesses[i]) for i in tournament_indices]
        return max(tournament, key=lambda x: x[1])[0]
    
    def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        """Crossover with value-based selection"""
        point = random.randint(1, self.n - 1)
        
        # Value-based crossover: chọn phần tốt hơn
        child1_option1 = parent1[:point] + parent2[point:]
        child1_option2 = parent2[:point] + parent1[point:]
        
        child1 = child1_option1 if self.value_function(child1_option1) > self.value_function(child1_option2) else child1_option2
        child2 = child1_option2 if child1 == child1_option1 else child1_option1
        
        return child1, child2
    
    def mutate_with_value_ordering(self, individual: List[int], mutation_rate: float = 0.1) -> List[int]:
        """Mutation với value-based bias"""
        mutated = individual.copy()
        
        for i in range(self.n):
            if random.random() < mutation_rate:
                # Thử các giá trị và chọn tốt nhất
                best_value = -1
                best_row = mutated[i]
                
                for row in range(self.n):
                    temp_individual = mutated.copy()
                    temp_individual[i] = row
                    value = self.value_function(temp_individual)
                    
                    if value > best_value:
                        best_value = value
                        best_row = row
                mutated[i] = best_row
        
        return mutated

def convert_csp_solution(solution: Dict[str, int], n: int) -> List[int]:
    """Chuyển đổi solution từ CSP sang list"""
    if solution is None:
        return None
    return [solution[f'Q{i}'] for i in range(n)]

def main():
    n = 5
    results = []
    
    # 1. CSP với SimpleAI - So sánh có và không có AC3
    print("1. BACKTRACKING VỚI CSP")
    nqueens_csp = NQueensCSP(n)
    csp_problem = nqueens_csp.create_csp_problem()        
       
    # Backtracking KHÔNG có AC3 (inference=False)
    print("Backtracking không có AC3:")
    start_time = time.time()
    solution_no_ac3 = backtrack(csp_problem, inference=False)
    time_no_ac3 = time.time() - start_time
    solution_list_no_ac3 = convert_csp_solution(solution_no_ac3, n)
        
    print(f"Thời gian: {time_no_ac3:.4f}s")
    print(f"Nghiệm: {solution_list_no_ac3}")
    success_no_ac3 = solution_list_no_ac3 is not None
    if success_no_ac3:
        print(f"Conflicts: {nqueens_csp.conflicts(solution_list_no_ac3)}")
        nqueens_csp.print_board(solution_list_no_ac3)        
        
    # Backtracking CÓ AC3 (inference=True)
    print("Backtracking có AC3:")
    start_time = time.time()
    solution_ac3 = backtrack(csp_problem, inference=True)
    time_ac3 = time.time() - start_time
    solution_list_ac3 = convert_csp_solution(solution_ac3, n)
        
    print(f"Thời gian: {time_ac3:.4f}s")
    print(f"Nghiệm: {solution_list_ac3}")
    success_ac3 = solution_list_ac3 is not None
    if success_ac3:
        print(f"Conflicts: {nqueens_csp.conflicts(solution_list_ac3)}")        
        
    # Backtracking với Value Ordering Function
    print("Backtracking với Value Ordering:")
    start_time = time.time()
    solution_value_ordering = backtrack(
        csp_problem,
        variable_heuristic=MOST_CONSTRAINED_VARIABLE,
        value_heuristic=lambda csp, var, assignment: nqueens_csp.value_ordering_function(csp, var, assignment),
        inference=True
    )
    time_value_ordering = time.time() - start_time
    solution_list_value_ordering = convert_csp_solution(solution_value_ordering, n)
        
    print(f"Thời gian: {time_value_ordering:.4f}s")
    print(f"Nghiệm: {solution_list_value_ordering}")
    success_value_ordering = solution_list_value_ordering is not None
        
    results.extend([
        ("Backtracking (No AC3)", time_no_ac3, success_no_ac3),
        ("Backtracking (With AC3)", time_ac3, success_ac3),
        ("Backtracking + Value Ordering", time_value_ordering, success_value_ordering)
    ])
    
    # 2. Hill Climbing với Value Ordering
    print(f"\n2. HILL CLIMBING")
    hc = HillClimbingWithValueOrdering(n)
    
    best_hc_solution = None
    best_hc_conflicts = float('inf')
    hc_times = []
    successful_runs = 0
    
    for trial in range(10):
        start_time = time.time()
        hc_solution, hc_conflicts, hc_iterations = hc.solve()
        hc_time = time.time() - start_time
        
        hc_times.append(hc_time)
        if hc_conflicts < best_hc_conflicts:
            best_hc_solution = hc_solution
            best_hc_conflicts = hc_conflicts
        
        if hc_conflicts == 0:
            successful_runs += 1
    
    avg_hc_time = sum(hc_times) / len(hc_times)
    print(f"  Thời gian TB (10 lần chạy): {avg_hc_time:.4f}s")
    print(f"  Tỷ lệ thành công: {successful_runs}/10")
    print(f"  Nghiệm tốt nhất: {best_hc_solution}")
    print(f"  Conflicts tốt nhất: {best_hc_conflicts}")
    if best_hc_conflicts == 0:
        hc.print_board(best_hc_solution)
    
    results.append(("Hill Climbing", avg_hc_time, best_hc_conflicts == 0))
    
    # 3. Simulated Annealing với Value Ordering
    print(f"\n3. SIMULATED ANNEALING")
    sa = SimulatedAnnealingWithValueOrdering(n)
    
    best_sa_solution = None
    best_sa_conflicts = float('inf')
    sa_times = []
    sa_successful_runs = 0
    
    for trial in range(5):
        start_time = time.time()
        sa_solution, sa_conflicts, sa_iterations = sa.solve()
        sa_time = time.time() - start_time
        
        sa_times.append(sa_time)
        if sa_conflicts < best_sa_conflicts:
            best_sa_solution = sa_solution
            best_sa_conflicts = sa_conflicts
        
        if sa_conflicts == 0:
            sa_successful_runs += 1
    
    avg_sa_time = sum(sa_times) / len(sa_times)
    print(f"  Thời gian TB (5 lần chạy): {avg_sa_time:.4f}s")
    print(f"  Tỷ lệ thành công: {sa_successful_runs}/5")
    print(f"  Nghiệm tốt nhất: {best_sa_solution}")
    print(f"  Conflicts tốt nhất: {best_sa_conflicts}")
    if best_sa_conflicts == 0:
        sa.print_board(best_sa_solution)
    
    results.append(("SA", avg_sa_time, best_sa_conflicts == 0))
    
    # 4. Genetic Algorithm với Value Ordering
    print(f"\n4. GENETIC ALGORITHM")
    ga = GeneticAlgorithmWithValueOrdering(n, population_size=40)
    
    start_time = time.time()
    ga_solution, ga_conflicts, ga_generations = ga.solve(generations=300)
    ga_time = time.time() - start_time
    
    print(f"  Thời gian: {ga_time:.4f}s")
    print(f"  Số thế hệ: {ga_generations}")
    print(f"  Nghiệm: {ga_solution}")
    print(f"  Conflicts: {ga_conflicts}")
    if ga_conflicts == 0:
        ga.print_board(ga_solution)
    
    results.append(("GA", ga_time, ga_conflicts == 0))
    
    # 5. So sánh kết quả tổng thể
    print(f"\n=== SO SÁNH HIỆU QUẢ CÁC THUẬT TOÁN ===")
    print(f"{'Thuật toán':<30} {'Thời gian (s)':<12} {'Thành công'}")
    print("-" * 55)
    for name, time_taken, success in results:
        print(f"{name:<30} {time_taken:<12.4f} {'✓' if success else '✗'}")
    
    # So sánh Backtracking
    csp_results = [(name, time_taken, success) for name, time_taken, success in results if "Backtracking" in name]
    if len(csp_results) >= 2:
        no_ac3 = next((r for r in csp_results if "No AC3" in r[0]), None)
        with_ac3 = next((r for r in csp_results if "With AC3" in r[0]), None)
        
    if no_ac3 and with_ac3:
        print(f"So sánh AC3:")
        print(f"   Không AC3: {no_ac3[1]:.4f}s")
        print(f"   Có AC3: {with_ac3[1]:.4f}s")
            
    # Thống kê tổng quát
    successful_methods = [(name, time_taken) for name, time_taken, success in results if success]
    if successful_methods:
        fastest = min(successful_methods, key=lambda x: x[1])
        print(f"Nhanh nhất: {fastest[0]} ({fastest[1]:.4f}s)")
    else:
        print(f"\nKhông có phương pháp nào thành công!")
if __name__ == "__main__":
    main()