import re

def parse_machine(block):
    """
    Parses a block of text corresponding to one machine and extracts the movements and prize location.
    """
    # Define regex patterns to extract numbers
    button_a_pattern = r"Button A:\s*X\+(\d+),\s*Y\+(\d+)"
    button_b_pattern = r"Button B:\s*X\+(\d+),\s*Y\+(\d+)"
    prize_pattern = r"Prize:\s*X=(\d+),\s*Y=(\d+)"

    # Initialize variables
    X_a = Y_a = X_b = Y_b = X_p = Y_p = None

    for line in block:
        line = line.strip()
        if not line:
            continue
        match_a = re.match(button_a_pattern, line)
        if match_a:
            X_a = int(match_a.group(1))
            Y_a = int(match_a.group(2))
            continue
        match_b = re.match(button_b_pattern, line)
        if match_b:
            X_b = int(match_b.group(1))
            Y_b = int(match_b.group(2))
            continue
        match_p = re.match(prize_pattern, line)
        if match_p:
            X_p = int(match_p.group(1))
            Y_p = int(match_p.group(2))
            continue

    if None in [X_a, Y_a, X_b, Y_b, X_p, Y_p]:
        raise ValueError("Incomplete machine configuration.")

    return (X_a, Y_a, X_b, Y_b, X_p, Y_p)

def minimal_token_cost(X_a, Y_a, X_b, Y_b, X_p, Y_p):
    # calculate determinants 
    D = Y_b * X_a - Y_a * X_b

    # if determinantes not zero, we have unique solution
    if D != 0:
        # calculate the numerators to apply Cramer's Rule
        a_num = X_p * Y_b - X_b * Y_p
        b_num = Y_p * X_a - Y_a * X_p

        # Since we don't want negative result, take the absolute value instead
        if D < 0:
            a_num = -a_num
            b_num = -b_num
            D = -D

        # result is a fraction, cannot reach coordinates
        if a_num % D != 0 or b_num % D != 0:
            return None  # No integer solution

        # Cramer's rule result 
        a = a_num // D
        b = b_num // D

        # Cannot have any negative moves 
        if a < 0 or b < 0:
            return None 
        
        # Calculate number of moves
        return 3 * a + b
    else:
        # Check for consistency
        if (Y_a * X_p != X_a * Y_p):
            return None  # Inconsistent system, no solution

        # Handle special cases where both X_a and X_b are zero
        if X_a == 0 and X_b == 0:
            if X_p != 0:
                return None
            # Any a and b satisfy the X equation; minimize based on Y
            # Similar logic can be applied, but it's an edge case
            return None  # Not handling this edge case here

        # Find non-negative integer solutions to X_a * a + X_b * b = X_p
        # We need to minimize 3a + b
        min_cost = None
        max_b = X_p // X_b if X_b != 0 else 0

        for b in range(0, max_b + 1):
            remaining_x = X_p - X_b * b
            if X_a == 0:
                if remaining_x != 0:
                    continue
                a = 0
            else:
                if remaining_x < 0:
                    continue
                if remaining_x % X_a != 0:
                    continue
                a = remaining_x // X_a
            if a < 0:
                continue
            cost = 3 * a + b
            if (min_cost is None) or (cost < min_cost):
                min_cost = cost
        return min_cost

def read_input_file(filename):
    """
    Reads the input file and returns a list of machines.
    Each machine is represented as a tuple:
    (X_a, Y_a, X_b, Y_b, X_p, Y_p)
    """
    with open(filename, 'r') as file:
        input_text = file.read()
    # Split into blocks separated by blank lines
    blocks = input_text.strip().split('\n\n')

    machines = []
    for block in blocks:
        lines = block.strip().split('\n')
        if not lines:
            continue
        try:
            machine = parse_machine(lines)
            machines.append(machine)
        except ValueError as ve:
            print(f"Skipping a machine due to error: {ve}")
            continue

    return machines

def main():
    # Specify the input file name
    input_filename = 'day13/example.txt'

    # Read machines from the input file
    machines = read_input_file(input_filename)

    total_tokens = 0
    solvable_machines = 0

    for idx, machine in enumerate(machines, start=1):
        X_a, Y_a, X_b, Y_b, X_p, Y_p = machine
        cost = minimal_token_cost(X_a, Y_a, X_b, Y_b, X_p+10000000000000, Y_p+10000000000000)
        if cost is not None:
            solvable_machines += 1
            total_tokens += cost
            print(f"Machine {idx}: Solvable with cost {cost} tokens.")
        else:
            print(f"Machine {idx}: No solution.")

    print("\nSummary:")
    print(f"The most prizes you could possibly win is {solvable_machines}; the minimum tokens you would have to spend to win all ({solvable_machines}) prizes is {total_tokens}.")

if __name__ == "__main__":
    main()
