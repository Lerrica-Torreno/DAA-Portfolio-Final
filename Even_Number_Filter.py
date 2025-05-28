# Even Number Filter - print rows where the first number is even

def EvenFirstDigit(df):
    results = {
        "even": [],
        "odd": [],
        "invalid": []
    }

    for number in df["Number1"]:
        try:
            first_char = str(number).strip()[0]
            first_digit = int(first_char)

            if first_digit % 2 == 0:
                results["even"].append(number)
            else:
                results["odd"].append(number)

        except (ValueError, IndexError):
            results["invalid"].append(number)

    return results
# Time complexity: O(n), where n = number of rows in the 'Number1' column