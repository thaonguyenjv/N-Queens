from simpleai.search import CspProblem, backtrack
import time

class NQueensCSP:
    def __init__(self, n=5):
        self.n = n
        self.setup_csp()
    
    def setup_csp(self):
        """Thiết lập bài toán CSP"""
        # Variables: các hàng (0, 1, 2, 3, 4)
        variables = list(range(self.n))
        
        # Domains: mỗi hàng có thể đặt quân hậu ở cột nào (0-4)
        domains = {}
        for var in variables:
            domains[var] = list(range(self.n))
        
        # Constraints: không cùng cột, không cùng đường chéo
        constraints = []
        
        for i in range(self.n):
            for j in range(i + 1, self.n):
                # Constraint giữa hàng i và hàng j
                def constraint_func(variables, values, row1=i, row2=j):
                    col1, col2 = values
                    # Không cùng cột
                    if col1 == col2:
                        return False
                    # Không cùng đường chéo
                    if abs(row1 - row2) == abs(col1 - col2):
                        return False
                    return True
                
                constraints.append(((i, j), constraint_func))
        
        # Tạo CSP problem
        self.problem = CspProblem(variables, domains, constraints)
    
    def solve(self):
        
        start_time = time.time()
        
        # Sử dụng backtrack search của SimpleAI
        solution = backtrack(self.problem)
        
        end_time = time.time()
        
        if solution:
            print(f"Tìm được nghiệm trong {end_time - start_time:.4f}s")
            return solution
        else:
            print(" Không tìm được nghiệm")
            return None
    
    def print_board(self, solution):
        """In bàn cờ"""
        if not solution:
            return
        
        print(f"\n Bàn cờ {self.n}x{self.n}:")
        print("   " + " ".join([f"{i:2}" for i in range(self.n)]))
        print("  +" + "---" * self.n)
        
        for row in range(self.n):
            line = f"{row} |"
            for col in range(self.n):
                if solution[row] == col:
                    line += " Q "
                else:
                    line += " . "
            print(line)
        
        print(f"\n Vị trí các quân hậu: {[(row, solution[row]) for row in sorted(solution.keys())]}")
        print(f" Kiểm tra: {self.verify_solution(solution)}")
    
    def verify_solution(self, solution):
        """Xác minh nghiệm"""
        if not solution:
            return False
        
        positions = [(row, solution[row]) for row in solution.keys()]
        
        for i, (r1, c1) in enumerate(positions):
            for j, (r2, c2) in enumerate(positions):
                if i != j:
                    # Kiểm tra xung đột
                    if r1 == r2 or c1 == c2 or abs(r1-r2) == abs(c1-c2):
                        return " Có xung đột"
        return "Hợp lệ"

# Chạy thử nghiệm
def main():
    # Giải N-Queens 5x5
    solver = NQueensCSP(5)
    solution = solver.solve()
    solver.print_board(solution)
if __name__ == "__main__":
    main()