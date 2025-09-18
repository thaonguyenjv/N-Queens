from simpleai.search import CspProblem, backtrack
import time

# --------- Đếm số bước kiểm tra ----------
steps = 0

# --------- Ràng buộc N-Queens ----------
def queens_constraint(variables, values):
    """
    Ràng buộc: hai quân hậu không được cùng hàng, cùng cột, hoặc cùng đường chéo
    """
    global steps
    steps += 1
    var1, var2 = variables
    val1, val2 = values
    # Không cùng hàng và không cùng đường chéo
    return abs(val1 - val2) not in (0, abs(var1 - var2))


# --------- Hàm chạy thử nghiệm ----------
def run_test(N, use_ac3=False):
    global steps
    steps = 0

    # Biến: mỗi cột trên bàn cờ
    variables = list(range(N))
    # Miền giá trị: mỗi cột có thể đặt hậu ở hàng 0..N-1
    domains = {v: list(range(N)) for v in variables}

    # Tạo ràng buộc cho mọi cặp cột
    constraints = []
    for i in range(N):
        for j in range(i + 1, N):
            constraints.append(((i, j), queens_constraint))

    problem = CspProblem(variables, domains, constraints)

    print(f"\n=== N = {N} | AC3 = {use_ac3} ===")

    start = time.time()
    result = backtrack(problem,
                       inference='AC3' if use_ac3 else None)  # dùng AC3 hoặc không
    end = time.time()

    # In kết quả
    print("Solution:", result)
    print("Thời gian chạy:", round(end - start, 5), "giây")
    print("Số bước kiểm tra ràng buộc:", steps)


# --------- Thực thi ----------
if __name__ == '__main__':
    N = 5
    run_test(N, use_ac3=False)   # không dùng AC3
    run_test(N, use_ac3=True)    # dùng AC3
