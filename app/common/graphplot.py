def count_digits(n):
    """ 桁数を求める """
    digits = 0
    val = 1
    if n < 1:
        val *= 0.1
        digits -= 1
        while n < val:
            digits -= 1
            val *= 0.1
    elif n > 1:
        val *= 10
        while n >= val:
            digits += 1
            val *= 10
    return digits

def round_to_nearest(min_val, max_val):
    """ 数値を丸める """
    diff = max_val - min_val
    digi = count_digits(diff) - 1
    # maxは切り上げ
    max_val_re = (10 ** digi) * (max_val // (10 ** digi) + 1)
    # minは切り捨て
    min_val_re = (10 ** digi) * (min_val // (10 ** digi))
    return min_val_re, max_val_re
    
def divide_ticks(start, end, num_divisions):
    """ 指定した数で分割したメモリラベルを取得 """
    if start > end:
        start, end = end, start
    
    total_duration = end - start
    division_duration = total_duration / num_divisions
    
    divided_ticks = [start + i * division_duration for i in range(num_divisions + 1)]
    
    return divided_ticks