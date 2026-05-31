import math

def calculate_rtt_timeout(sample_rtt_list, initial_estimated, initial_dev, alpha=0.125, beta=0.25):
    results = []
    est = initial_estimated
    dev = initial_dev
    
    # مرحله 0 (مقادیر اولیه قبل از نمونه)
    results.append((0, '-', round(est, 2), round(dev, 2), round(est + 4*dev, 2)))
    
    for i, samp in enumerate(sample_rtt_list, start=1):
        # تخمین جدید EstimatedRTT
        est_new = alpha * samp + (1 - alpha) * est
        # تخمین جدید DevRTT (طبق فرمول استاندارد: |sample - est_new|)
        dev_new = beta * abs(samp - est_new) + (1 - beta) * dev
        timeout = est_new + 4 * dev_new
        
        results.append((i, samp, round(est_new, 2), round(dev_new, 2), round(timeout, 2)))
        
        # به روز رسانی برای مرحله بعد
        est = est_new
        dev = dev_new
    
    return results

# ========== مثال با اعداد سوال شما (ترتیب داده شده در متن) ==========
sample_list = [120,140,160]   # ترتیب سوال
initial_est = 100
initial_dev = 10

output = calculate_rtt_timeout(sample_list, initial_est, initial_dev)

print("n\tSampleRTT\tEstimatedRTT\tDevRTT\tTimeoutInterval")
for row in output:
    print(f"{row[0]}\t{row[1]}\t\t{row[2]}\t\t{row[3]}\t{row[4]}")