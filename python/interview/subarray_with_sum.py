# https://practice.geeksforgeeks.org/problems/subarray-with-given-sum/0
# import sys
# print(sys.argv)

# a = input()
# a = a.split()
# sum  = 0
# for i in a:
#     sum += int(i)
# print(sum)

def get_index(total, array, length):
    start = end = 0
    curr_sum = array[start]
    while start <= end < length:
        # print(start, end, curr_sum)
        if curr_sum < total:
            end += 1
            if end == length:
                return None, None
            curr_sum += array[end]
            continue
        elif curr_sum > total:
            if start != end:
                curr_sum -= array[start]
                start += 1
                continue
            else:
                start += 1
                end += 1
                if end == length:
                    return None, None
                curr_sum = array[start]
                continue
        else:
            return start+1, end+1
    return None, None

def main():
    test_count = int(input())
    for _ in range(test_count):
        first_line = input()
        size, total = map(int, first_line.split())
        second_line = input()
        array = list(map(int, second_line.split()))
        s, e = get_index(total, array, size)
        if s:
            print(s, e)
        else:
            print(-1)

if __name__ == "__main__":
    main()
