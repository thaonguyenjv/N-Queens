import time
from simpleai.search import (
    CspProblem,
    backtrack,
    MOST_CONSTRAINED_VARIABLE,
    LEAST_CONSTRAINING_VALUE,
    HIGHEST_DEGREE_VARIABLE,
)

# ================== Tạo bài toán N-Queens ==================
def create_n_queens_problem(n=5):
    """
    Tạo bài toán N-Queens dưới dạng CSP (Constraint Satisfaction Problem).
    - Mỗi biến: Q0, Q1, ..., Q(n-1) (ứng với hàng).
    - Miền giá trị: [0..n-1] (ứng với cột đặt quân hậu).
    - Ràng buộc: không được cùng cột và không được cùng đường chéo.
    """
    variables = [f'Q{i}' for i in range(n)]
    domains = {var: list(range(n)) for var in variables}

    constraints = []

    def not_attacking(variables, values):
        """
        Hàm kiểm tra ràng buộc:
        - Không cùng cột
        - Không cùng đường chéo
        """
        row1 = int(variables[0][1:])
        row2 = int(variables[1][1:])
        col1, col2 = values

        return col1 != col2 and abs(row1 - row2) != abs(col1 - col2)

    # Thêm ràng buộc cho mọi cặp quân hậu
    for i in range(n):
        for j in range(i + 1, n):
            constraints.append(((f'Q{i}', f'Q{j}'), not_attacking))

    return CspProblem(variables, domains, constraints)


# ================== Giải & đo thời gian ==================
def solve_and_measure(problem, variable_heuristic=None, value_heuristic=None, inference=False):
    """
    Giải CSP bằng backtracking với các heuristic khác nhau.
    Trả về nghiệm và thời gian chạy.
    """
    start_time = time.time()
    solution = backtrack(
        problem,
        variable_heuristic=variable_heuristic,
        value_heuristic=value_heuristic,
        inference=inference,
    )
    end_time = time.time()

    return {
        'solution': solution,
        'time': end_time - start_time,
    }

# ================== Hiển thị nghiệm ==================
def print_solution_array(solution, n):
    """
    Hiển thị nghiệm dưới dạng mảng:
    - Chỉ số: hàng (row)
    - Giá trị: cột (col) đặt quân hậu
    """
    if not solution:
        print("❌ Không có nghiệm.")
        return

    result = [0] * n
    for var, col in solution.items():
        row = int(var[1:])
        result[row] = col
    print(f"📌Nghiệm tìm được: {result}")
    return result

# ================== Hiển thị bàn cờ ==================
def print_board(solution, n):
    """
    Hiển thị bàn cờ trực quan từ nghiệm.
    """
    if not solution:
        print("❌ Không tìm thấy nghiệm.")
        return

    board = [['.' for _ in range(n)] for _ in range(n)]
    for var, col in solution.items():
        row = int(var[1:])
        board[row][col] = 'Q'

    for row in board:
        print(' '.join(row))


# ================== Main ==================
if __name__ == "__main__":
    N = 5  # bạn có thể đổi N tại đây
    print(f"=== Giải bài toán N-Queens với N={N} ===\n")

    strategies = [
        ("Cơ bản (Không heuristic)", {}, {}),
        ("Most Constrained Variable (MCV)", {"variable_heuristic": MOST_CONSTRAINED_VARIABLE}, {}),
        ("Least Constraining Value (LCV)", {}, {"value_heuristic": LEAST_CONSTRAINING_VALUE}),
        ("MCV + LCV", {"variable_heuristic": MOST_CONSTRAINED_VARIABLE}, {"value_heuristic": LEAST_CONSTRAINING_VALUE}),
        ("Degree Heuristic", {"variable_heuristic": HIGHEST_DEGREE_VARIABLE}, {}),
        ("Forward Checking", {}, {"inference": True}),
    ]

    results = []

    # Chạy lần lượt các chiến lược
    for name, var_params, val_params in strategies:
        print(f"\n▶ Chiến lược: {name}")
        problem = create_n_queens_problem(N)
        result = solve_and_measure(problem, **var_params, **val_params)
        print(f"⏱️ Thời gian: {result['time']:.4f}s")
        # Hiển thị nghiệm dưới dạng mảng
        arr=print_solution_array(result['solution'], N)
        print_board(result['solution'], N)
        # Lưu kết quả
        results.append((name, result['time']))

    # ================== Bảng so sánh ==================
    print("\n=== Bảng so sánh hiệu quả ===")
    print(f"{'Chiến lược':<30} | {'Thời gian (s)':<10}")
    print("-" * 45)
    for name, t in results:
        print(f"{name:<30} | {t:<10.4f}")
