
import time  
from simpleai.search import (
    CspProblem,  # Lớp cơ sở để định nghĩa một bài toán CSP
    backtrack,  # Thuật toán giải CSP bằng phương pháp quay lui
    MOST_CONSTRAINED_VARIABLE,  # Heuristic: ưu tiên biến có ít giá trị hợp lệ còn lại nhất
    LEAST_CONSTRAINING_VALUE,  # Heuristic: ưu tiên giá trị loại bỏ ít lựa chọn nhất của các biến lân cận
    HIGHEST_DEGREE_VARIABLE,  # Heuristic: ưu tiên biến có nhiều ràng buộc với các biến khác nhất
)

# ================== Phần 1: Định nghĩa bài toán N-Queens ==================
def create_n_queens_problem(n=5):
    '''
    Hàm này tạo ra một đối tượng bài toán N-Queens dưới dạng CSP (Constraint Satisfaction Problem).
    - Biến (Variables): Mỗi quân hậu trên một hàng là một biến. Ví dụ: Q0, Q1, ..., Q(n-1).
    - Miền giá trị (Domains): Vị trí cột mà mỗi quân hậu có thể được đặt. Ví dụ: [0, 1, ..., n-1].
    - Ràng buộc (Constraints): Các điều kiện để các quân hậu không "ăn" nhau.
    '''
    
    # Tạo danh sách các biến, mỗi biến tương ứng với một hàng trên bàn cờ.
    # Ví dụ với n=4, ta có ['Q0', 'Q1', 'Q2', 'Q3'].
    variables = [f'Q{i}' for i in range(n)]
    
    # Tạo miền giá trị cho mỗi biến. Mỗi quân hậu (biến) có thể được đặt ở bất kỳ cột nào từ 0 đến n-1.
    domains = {var: list(range(n)) for var in variables}

    # Khởi tạo danh sách để chứa các ràng buộc.
    constraints = []

    # Định nghĩa hàm kiểm tra ràng buộc cho hai quân hậu.
    def not_attacking(variables, values):
        '''
        Hàm này là một ràng buộc, trả về True nếu hai quân hậu không tấn công nhau.
        - `variables`: một tuple chứa tên của hai biến (ví dụ: ('Q1', 'Q3')).
        - `values`: một tuple chứa giá trị (cột) của hai biến đó (ví dụ: (2, 4)).
        '''
        # Lấy chỉ số hàng từ tên biến (ví dụ: 'Q1' -> 1).
        row1 = int(variables[0][1:])
        row2 = int(variables[1][1:])
        # Lấy giá trị cột.
        col1, col2 = values

        # Hai quân hậu không tấn công nhau nếu chúng không cùng cột VÀ không cùng đường chéo.
        # - Cùng cột: col1 == col2
        # - Cùng đường chéo: abs(row1 - row2) == abs(col1 - col2)
        return col1 != col2 and abs(row1 - row2) != abs(col1 - col2)

    # Tạo ràng buộc cho mọi cặp quân hậu khác nhau trên bàn cờ.
    # Ví dụ: (Q0, Q1), (Q0, Q2), ..., (Q(n-2), Q(n-1)).
    for i in range(n):
        for j in range(i + 1, n):
            constraints.append(((f'Q{i}', f'Q{j}'), not_attacking))

    # Trả về một đối tượng CspProblem đã được định nghĩa đầy đủ.
    return CspProblem(variables, domains, constraints)

# ================== Phần 2: Hàm giải bài toán và đo lường hiệu suất ==================
def solve_and_measure(problem, variable_heuristic=None, value_heuristic=None, inference=False):
    '''
    Hàm này nhận một bài toán CSP và các tùy chọn, sau đó giải nó và đo thời gian.
    - `problem`: Đối tượng CspProblem cần giải.
    - `variable_heuristic`: Chiến lược chọn biến tiếp theo (ví dụ: MOST_CONSTRAINED_VARIABLE).
    - `value_heuristic`: Chiến lược chọn giá trị cho biến (ví dụ: LEAST_CONSTRAINING_VALUE).
    - `inference`: Bật/tắt suy luận (ví dụ: Forward Checking).
    '''
    # Ghi lại thời điểm bắt đầu.
    start_time = time.time()
    
    # Gọi hàm `backtrack` của simpleai để tìm nghiệm.
    solution = backtrack(
        problem,
        variable_heuristic=variable_heuristic,
        value_heuristic=value_heuristic,
        inference=inference,
    )
    
    # Ghi lại thời điểm kết thúc.
    end_time = time.time()

    # Trả về một dictionary chứa nghiệm và tổng thời gian giải.
    return {
        'solution': solution,  # Nghiệm tìm được (hoặc None nếu không có nghiệm)
        'time': end_time - start_time,  # Thời gian thực thi
    }

# ================== Phần 3: Các hàm hiển thị kết quả ==================
def print_solution_array(solution, n):
    '''
    Hiển thị nghiệm tìm được dưới dạng một mảng đơn giản.
    - Chỉ số của mảng là hàng.
    - Giá trị tại mỗi chỉ số là cột đặt quân hậu.
    Ví dụ: [1, 3, 0, 2] nghĩa là:
      - Hàng 0, cột 1
      - Hàng 1, cột 3
      - Hàng 2, cột 0
      - Hàng 3, cột 2
    '''
    if not solution:
        print("Không có nghiệm.")
        return

    # Chuyển đổi từ định dạng dictionary của simpleai sang mảng.
    result = [0] * n
    for var, col in solution.items():
        row = int(var[1:])
        result[row] = col
    print(f"Nghiệm tìm được: {result}")
    return result

def print_board(solution, n):
    if not solution:
        print("Không tìm thấy nghiệm để hiển thị bàn cờ.")
        return

    # Tạo một bàn cờ rỗng.
    board = [['.' for _ in range(n)] for _ in range(n)]
    
    # Đặt các quân hậu vào bàn cờ dựa trên nghiệm.
    for var, col in solution.items():
        row = int(var[1:])
        board[row][col] = 'Q'

    # In bàn cờ ra màn hình.
    for row_data in board:
        print(' '.join(row_data))

# ================== Phần 4: Khối thực thi chính ==================
if __name__ == "__main__":
    N = 5 
    print(f"=== Giải bài toán N-Queens với N={N} ===\n")

    # --- Định nghĩa các chiến lược cần thử nghiệm ---
    # Mỗi chiến lược là một tuple: (Tên, tham số cho variable_heuristic, tham số cho value_heuristic/inference)
    strategies = [
        # 1. Không dùng heuristic nào cả.
        ("Cơ bản (Không heuristic)", {}, {}),
        
        # 2. Chỉ dùng heuristic chọn biến (Most Constrained Variable).
        ("Most Constrained Variable (MCV)", {"variable_heuristic": MOST_CONSTRAINED_VARIABLE}, {}),
        
        # 3. Chỉ dùng heuristic chọn giá trị (Least Constraining Value).
        ("Least Constraining Value (LCV)", {}, {"value_heuristic": LEAST_CONSTRAINING_VALUE}),
        
        # 4. Kết hợp cả hai heuristic trên.
        ("MCV + LCV", {"variable_heuristic": MOST_CONSTRAINED_VARIABLE}, {"value_heuristic": LEAST_CONSTRAINING_VALUE}),
        
        # 5. Dùng heuristic bậc (Degree Heuristic).
        ("Degree Heuristic", {"variable_heuristic": HIGHEST_DEGREE_VARIABLE}, {}),
        
        # 6. Dùng kỹ thuật suy luận Forward Checking.
        ("Forward Checking", {}, {"inference": True}),
    ]

    # Danh sách để lưu kết quả của mỗi lần chạy.
    results = []

    # --- Chạy và so sánh các chiến lược ---
    # Vòng lặp qua từng chiến lược đã định nghĩa.
    for name, var_params, other_params in strategies:
        print(f"\nĐang chạy chiến lược: {name}")
        
        # Tạo lại bài toán cho mỗi lần chạy để đảm bảo tính công bằng.
        problem = create_n_queens_problem(N)
        
        # Giải bài toán với chiến lược hiện tại và đo thời gian.
        # Dấu ** dùng để "giải nén" dictionary thành các tham số keyword.
        result = solve_and_measure(problem, **var_params, **other_params)
        
        print(f"Thời gian: {result['time']:.6f}s")
        
        # Hiển thị nghiệm tìm được.
        print_solution_array(result['solution'], N)
        print_board(result['solution'], N)
        
        # Lưu lại kết quả để so sánh cuối cùng.
        results.append((name, result['time']))

    print("\n\n=== Bảng so sánh hiệu quả các chiến lược ===")
    print(f"{'Chiến lược':<35} | {'Thời gian (giây)':<10}")
    print("-" * 55)
    # Sắp xếp kết quả từ nhanh nhất đến chậm nhất.
    results.sort(key=lambda x: x[1])
    for name, t in results:
        print(f"{name:<35} | {t:<10.6f}")