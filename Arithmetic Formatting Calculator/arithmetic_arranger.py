def arithmetic_arranger(s:str, solve:bool=False)->str:
    for x in s:
        split_string = x.split()
        if len(s)>5: return "Error: Too many problems."
        if split_string[1] not in ["+", "-"]: return "Error: Operator must be '+' or '-'."
        if not all([i.isnumeric() for i in split_string[0]]): return "Error: Numbers must only contain digits."
        if not all([i.isnumeric() for i in split_string[2]]): return "Error: Numbers must only contain digits."
        if len(split_string[0])>4: return "Error: Numbers cannot be more than four digits."
        if len(split_string[2])>4: return "Error: Numbers cannot be more than four digits."

    first_number, second_number, third_number, operator, max_length, bar = [],[],[],[],[],[]
    for i in s:
        t = i.split()
        first_number.append(t[0])
        operator.append(t[1])
        second_number.append(t[2])
        if solve:
            third_number.append(str(eval(i)))

    for n in range(len(s)):
        max_length.append(max(len(first_number[n]), len(second_number[n])))
        first_number[n] = " "*(max_length[n] - len(first_number[n]))+first_number[n]
        second_number[n] = " "*(max_length[n] - len(second_number[n]))+second_number[n]
        bar.append("-"*(max_length[n]+2))
        second_number[n] = operator[n]+" "+second_number[n]
        if len(first_number[n])<len(second_number[n]):
            first_number[n] = " "*(len(second_number[n])-len(first_number[n]))+first_number[n]
        if solve:
            third_number[n] = " "*(len(second_number[n])-len(third_number[n]))+third_number[n]

    first_number = "    ".join(first_number)
    second_number = "    ".join(second_number)
    bar = "    ".join(bar)

    if solve:
        third_number = "    ".join(third_number)
        res_list = [first_number, second_number, bar, third_number]
    else:
        res_list = [first_number, second_number, bar]
    arranged_problems = "\n".join(res_list)

    return arranged_problems

s = ["32 - 698", "1 - 3801", "45 + 43", "123 + 49"]
print(arithmetic_arranger(s, True))

