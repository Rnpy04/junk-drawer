import math

def binomial_probability(M, p, k):
    """احتمال اینکه دقیقاً k کاربر از M کاربر همزمان فعال باشند"""
    comb = math.comb(M, k)          # تعداد انتخاب k کاربر از M
    prob = comb * (p ** k) * ((1 - p) ** (M - k))
    return prob

def cumulative_probability(M, p, N, greater_than=True):
    """
    محاسبه احتمال تجمعی
    اگر greater_than = True:  احتمال اینکه تعداد کاربران فعال > N باشد
    اگر greater_than = False: احتمال اینکه تعداد کاربران فعال ≤ N باشد
    """
    total = 0.0
    if greater_than:
        start = N + 1
        end = M
    else:
        start = 0
        end = N
    for i in range(start, end + 1):
        total += binomial_probability(M, p, i)
    return total

M = 40      # تعداد کل کاربران
p = 0.1      # احتمال فعال بودن هر کاربر در هر لحظه
N = 10      # آستانه (مثلاً ۵۰ کاربر)


prob_max_10 = cumulative_probability(M, p, N, greater_than=False)
print(f"P(X ≤ N) = {prob_max_10:.8f}")         # خروجی: حدود 0.999... (بسیار نزدیک به ۱)
print(f"P(X > N) = {1-prob_max_10:.8f}") 
