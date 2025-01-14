# -*- coding: utf-8 -*-
# Resistor Ratio Matcher
#   Created: Spring 2023 (Modified: Spring 2025)
#   Hunter Hartley
#
# PURPOSE:
#   Determine the best combination of standard E-Series resistors
#   to create a voltage divider with a particular ratio Vout/Vin.
#   
#   Normally, one must choose one of the resistor's values to calculate
#   the other. This approach will generally yield a value not belonging
#   to an E-Series. This program optimizes both values to yield the
#   closest possible match from the finite set of possible values.

import math
import time

# Below: The E6, E12, and E24 standard values
seriesE6  = [1.0, 1.5, 2.2, 3.3, 4.7, 6.8]

seriesE12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7,
             3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

seriesE24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6,
             1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
             3.3, 3.6, 3.9, 4.3, 4.7, 5.1,
             5.6, 6.2, 6.8, 7.5, 8.2, 9.1]


def number_input_interpreter(i):  # parse user input for choice of E-Series
    interpretOne = [1, "1", "[1]", "1.", "one", "One", "ONE"]
    interpretTwo = [2, "2", "[2]", "2.", "two", "Two", "TWO"]
    interpretThree = [3, "3", "[3]", "3.", "three", "Three", "THREE"]
    interpretNumber = [interpretOne, interpretTwo, interpretThree]
    for internalList in interpretNumber:
        for y in internalList:
            if i == y:
                return internalList[0]
    return -1


def prompt_ratio():
    ratio_input = -1
    while ratio_input == -1:  # Get desired decimal ratio
        print("Choose a decimal ratio [ R2 / (R1+R2) ]")  # Function will use Volt Div Formula
        print("[FLOAT] >", end='')
        strUserRatioInput = input()
        try:
            ratio_input = float(strUserRatioInput)
        except ValueError:
            print("Invalid input: Enter a decimal number [Eg: 0.52, 0.8652, etc]" + "\n")
            continue
        if ratio_input >= 1:
            print("Ratio can not be greater than one, check math")
            ratio_input = -1
            continue
        if ratio_input == 0:
            print("Ratio can not be zero, check math")
            ratio_input = -1
            continue
        if ratio_input < 0:
            print("Ratio can not be negative, check math")
            ratio_input = -1
            continue
        return ratio_input


def prompt_error_thres():
    user_error_thres = -1
    while user_error_thres == -1:  # Get permissible percent error
        print("Choose a percent error threshold (%):")
        strUserPercentErrorThreshold = input("[FLOAT] >")
        try:
            user_error_thres = float(strUserPercentErrorThreshold)
        except ValueError:
            print("Invalid input: Enter a decimal percentage between 0-100")
            continue
        if user_error_thres < 0:
            print("Percent error can't be negative, choose another value")
            user_error_thres = -1
            continue
        return user_error_thres


# Globals
e_series_choice = []
goal_ratio      = -1
error_thres     = -1


def init():
    global e_series_choice
    global goal_ratio
    global error_thres
    
    # Get user's choice of E-Series
    while not e_series_choice:
        print("\nChoose E-Series:\n[0]:E6  [1]:E12  [2]:E24")
        e_series_choice_num = number_input_interpreter(input("[INT] >"))
        e_series_choice = (seriesE6, seriesE12, seriesE24)[e_series_choice_num]

        # Check that input is valid
        if not e_series_choice:
            print("Invalid input, try again...")
            continue
            
        # Print the E-Series values chosen
        print( ("E6", "E12", "E24")[e_series_choice_num] + ":" )
        for index, item in enumerate(e_series_choice):
            print(str(item), end="\t\t")
            # Print in 3 columns (mostly because I have a chart on my wall with 3 columns)
            if (index + 1) % 3 == 0:
                print()
        print()
    
    goal_ratio  = prompt_ratio()
    error_thres = prompt_error_thres()


def comp():
    global e_series_choice
    global goal_ratio
    global error_thres
    
    start_time = time.time()  # Timed for gratification
    calc_results = []

    norm_ratio_exp = math.floor(math.log10(goal_ratio))
#   norm_ratio = goal_ratio * 10 ** (-1 * norm_ratio_exp)
    # 0.5 should yield 1, 0.05 -> 10, etc.
    r1_order_adj = 10**( -1 * (norm_ratio_exp + 1) )

    # Iterate through combinations of E-Series values
    for (r1_mult, r2_mult) in ( (10*r1_order_adj, 1), (1*r1_order_adj, 1), (1*r1_order_adj, 10) ):
        for r1_test in e_series_choice:
            for r2_test in e_series_choice:
                # Calculate ratio given current E-Series values
                testRatio = ( r2_test * r2_mult) / \
                            ( r1_mult * r1_test + r2_mult * r2_test )
                percentError = math.fabs((testRatio - goal_ratio) / goal_ratio) * 100
                # Only keep value if percent error meets threshold
                if percentError <= error_thres:
                    calc_results.append([round(r1_test * r1_mult, 1),
                                        round(r2_test * r2_mult, 1),
                                        round(testRatio,         6 + (-1-norm_ratio_exp) ),
                                        round(percentError,      4) ])

    # Sort results
    calc_results.sort( key=lambda x: float(x[3]) )
    end_time = time.time()

    return calc_results, (start_time, end_time)


def print_results(calc_results, calc_times):
    # Format results
    resultMaxLen = [0] * len(calc_results[0])
    for result in calc_results:
        result[3] = str(result[3]) + '%'
        resultMaxLen = [ max(len(str(x)), resultMaxLen[i]) for i, x in enumerate(result)]

    # Print results
    print('[R1, R2, RATIO, %ERR]\t(GOAL: ' + str(goal_ratio) + ')')
    for index, result in enumerate(calc_results):
        result_string = ', '.join([ f"{x:>{resultMaxLen[i]}}" for i, x in enumerate(result) ])
        print('[' + result_string + ']', end='\t\t')
        if (index + 1) % 3 == 0:
            print()
        
    executionTimeMilliseconds = 1000.0 * (calc_times[1] - calc_times[0])
    print('\n' + "Execution time: " + str(round(executionTimeMilliseconds, 4) ) + 'ms')


def prompt_new_tolerance():
    global error_thres
    # Allow user to try different tolerance without restarting
    tryNewTolerance = 'invalid'
    while tryNewTolerance == 'invalid':
        print("Try new tolerance? Y/n:")  # Prompt user to try new multiplier values
        tryNewTolerance = input("[Y/n] >")
        tryNewTolerance.strip()
        # Verify input
        if tryNewTolerance == '':
            return False
        elif tryNewTolerance in ['n', 'N', 'no', 'No', 'NO']:
            return False
        elif tryNewTolerance in ['y', 'Y', 'yes', 'Yes', 'YES']:
            error_thres = prompt_error_thres()
            return True
        else:
            print("Not understood")
            tryNewTolerance = 'invalid'


def main():
    global e_series_choice
    global goal_ratio
    global error_thres
    # Run init once
    init()
    # Check init() results
    for x in (e_series_choice, goal_ratio, error_thres):
        if x == -1:
            print(f"Variable value invalid: {x}")
    # Run comp until user done
    run_comp = True
    while run_comp:
        comp_results, times = comp()
        if not comp_results:
            print("No results found.")
        else:
            print_results(comp_results, times)
        run_comp = prompt_new_tolerance()
   
    print("\nCompleted. Rerunning... (Ctrl+C to quit at any time)")
    print("==================================================")
    # Choose number of new-lines on re-run
    print("\n"*2, end='')


if __name__ == "__main__":
    # Run main in loop until user manually exits
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            exit()
