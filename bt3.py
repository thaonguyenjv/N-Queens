from simpleai.search import CspProblem, backtrack
import time
class NQueensProblem(CspProblem):
    """
    Bai toan N-Queens su dung CSP
    Moi bien dai dien cho mot hang, gia tri la cot cua quan hau
    """
    def __init__(self, n=5):
        self.n = n
        # Bien: Q0, Q1, Q2, Q3, Q4 (dai dien cho hang 0,1,2,3,4)
        variables = [f'Q{i}' for i in range(n)]
        
        # Mien gia tri: moi quan hau co the o cot 0,1,2,3,4
        domains = {var: list(range(n)) for var in variables}
        
        # Rang buoc: khong hai quan hau nao tan cong nhau
        constraints = []
        
        # Tao rang buoc cho moi cap quan hau
        for i in range(n):
            for j in range(i + 1, n):
                var1 = f'Q{i}'
                var2 = f'Q{j}'
                constraints.append((
                    (var1, var2), 
                    self.not_attacking_constraint
                ))
        
        super().__init__(variables, domains, constraints)
        self.search_steps = 0
    def not_attacking_constraint(self, variables, values):
        """
        Kiem tra hai quan hau khong tan cong nhau
        variables: tuple cua 2 bien (Q_i, Q_j)
        values: tuple cua 2 gia tri (cot cua Q_i, cot cua Q_j)
        """
        self.search_steps += 1
        
        var1, var2 = variables
        col1, col2 = values
        
        # Lay hang tu ten bien (Q0 -> hang 0, Q1 -> hang 1, ...)
        row1 = int(var1[1])
        row2 = int(var2[1])
        
        # Khong cung cot
        if col1 == col2:
            return False
            
        # Khong cung duong cheo
        if abs(row1 - row2) == abs(col1 - col2):
            return False
            
        return True
    def print_solution(self, solution):
        """In ra ban co voi nghiem tim duoc"""
        if not solution:
            print("Khong tim thay nghiem!")
            return
            
        print(f"\nNghiem tim duoc:")
        print("=" * (self.n * 4 + 1))
        
        board = [['.' for _ in range(self.n)] for _ in range(self.n)]
        
        # Dat quan hau len ban co
        for var, col in solution.items():
            row = int(var[1])  # Q0 -> hang 0, Q1 -> hang 1, ...
            board[row][col] = 'Q'
        
        # In ban co
        for i, row in enumerate(board):
            print(f"{i} | {' | '.join(row)} |")
            print("  " + "+" + "---+" * self.n)
        
        print("   ", end="")
        for j in range(self.n):
            print(f" {j}  ", end="")
        print()

def solve_with_ac3_comparison():
    print("=" * 60)
    print("BAI TOAN N-QUEENS 5x5 - SO SANH AC3")
    
    results = {}
    
    # Test with AC3 = True
    print("\n1. Backtrack với AC3 ")
    
    problem_ac3 = NQueensProblem(5)
    start_time = time.time()
    
    try:
        solution_ac3 = backtrack(problem_ac3, ac3=True)
        end_time = time.time()
        
        results['ac3_true'] = {
            'solution': solution_ac3,
            'time': end_time - start_time,
            'steps': problem_ac3.search_steps,
            'success': solution_ac3 is not None
        }
        
        print(f"Thoi gian thuc hien: {results['ac3_true']['time']:.6f} giay")
        print(f"So buoc kiem tra rang buoc: {results['ac3_true']['steps']}")
        print(f"Tim thay nghiem: {'Co' if solution_ac3 else 'Khong'}")
        
        if solution_ac3:
            problem_ac3.print_solution(solution_ac3)
            
    except Exception as e:
        print(f"Loi khi chay voi AC3: {e}")
        results['ac3_true'] = {'success': False, 'error': str(e)}
    
    # Test with AC3 = False  
    print("\n2. Backtrack với không có AC3")
    
    problem_no_ac3 = NQueensProblem(5)
    start_time = time.time()
    
    try:
        solution_no_ac3 = backtrack(problem_no_ac3, ac3=False)
        end_time = time.time()
        
        results['ac3_false'] = {
            'solution': solution_no_ac3,
            'time': end_time - start_time,
            'steps': problem_no_ac3.search_steps,
            'success': solution_no_ac3 is not None
        }
        
        print(f"Thoi gian thuc hien: {results['ac3_false']['time']:.6f} giay")
        print(f"So buoc kiem tra rang buoc: {results['ac3_false']['steps']}")
        print(f"Tim thay nghiem: {'Co' if solution_no_ac3 else 'Khong'}")
        
        if solution_no_ac3:
            problem_no_ac3.print_solution(solution_no_ac3)
            
    except Exception as e:
        print(f"Loi khi chay voi khong co AC3: {e}")
        results['ac3_false'] = {'success': False, 'error': str(e)}
    
    # So sanh ket qua
    print("\n3. SO SANH KET QUA")
    
    if results.get('ac3_true', {}).get('success') and results.get('ac3_false', {}).get('success'):
        ac3_time = results['ac3_true']['time']
        no_ac3_time = results['ac3_false']['time']
        ac3_steps = results['ac3_true']['steps']
        no_ac3_steps = results['ac3_false']['steps']
        
        print(f"Thoi gian:")
        print(f"  • AC3 = True:  {ac3_time:.6f} giay")
        print(f"  • AC3 = False: {no_ac3_time:.6f} giay")
        if no_ac3_time > 0:
            print(f"  • Ti le: {ac3_time/no_ac3_time:.2f}x")
        
        print(f"\nSo buoc kiem tra rang buoc:")
        print(f"  • AC3 = True:  {ac3_steps:,} buoc")
        print(f"  • AC3 = False: {no_ac3_steps:,} buoc")
        if no_ac3_steps > 0:
            print(f"Ti le: {ac3_steps/no_ac3_steps:.2f}x")
    
    return results

def demonstrate_solutions():
    """
    Hien thi mot vai nghiem khac nhau cua bai toan N-Queens 5x5
    """
    print("\n4. MOT SO NGHIEM CUA N-QUEENS 5x5")
    print("-" * 50)
    
    # Nghiem thu cong de minh hoa
    manual_solutions = [
        {'Q0': 0, 'Q1': 2, 'Q2': 4, 'Q3': 1, 'Q4': 3},  # Nghiem 1
        {'Q0': 0, 'Q1': 3, 'Q2': 1, 'Q3': 4, 'Q4': 2},  # Nghiem 2
        {'Q0': 1, 'Q1': 3, 'Q2': 0, 'Q3': 2, 'Q4': 4},  # Nghiem 3
    ]
    
    problem = NQueensProblem(5)
    for i, solution in enumerate(manual_solutions, 1):
        print(f"\nNghiem {i}:")
        problem.print_solution(solution)

if __name__ == "__main__":
    # Chay so sanh chinh
    results = solve_with_ac3_comparison()
    # Hien thi them mot so nghiem
    demonstrate_solutions()