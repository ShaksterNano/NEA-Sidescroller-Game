def shift(list, front, value):  # Shifts a list by one in the direction specified, removes the value that is now out of the list and inserts the specified value at the other end where there is a free space
    length = len(list)

    if list:
        if front:
            for count in range(1, length):
                list[count - 1] = list[count]
            list[length - 1] = value
        else:
            for count in range(length - 2, -1, -1):
                list[count + 1] = list[count]
            list[0] = value

    return list
