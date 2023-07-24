###########################################################################
###########################################################################
#
# Alex Heinrich
# SEOP Circuit Analyzer
#
###########################################################################
###########################################################################

###########################################################################
# Global Values

# Voltage Supply Values
input_voltage, input_impedance = [1, 0], [0, 0]
frequency, frequency_set = 1, 1
angular_frequency = 2 * 3.14159265359 * frequency

# Component Values
R_op, R_op_set, R_op_impedance, R_op_list = 1, 1, [0, 0], []
C_Rb, C_Rb_set, C_Rb_impedance, C_Rb_list = 1*10^(-6), 1*10^(-6), [0, 0], []
R_sr, R_sr_set, R_sr_impedance, R_sr_list = 1, 1, [0, 0], []
R_ex, R_ex_set, R_ex_impedance, R_ex_list = 1, 1, [0, 0], []
C_Xe, C_Xe_set, C_Xe_impedance, C_Xe_list = 1*10^(-6), 1*10^(-6), [0, 0], []
R_w, R_w_set, R_w_impedance, R_w_list = 1, 1, [0, 0], []
total_list, frequency_list = [], []

# Calculation Values
sampling_rate = 1000 # Sets the number of datapoints calculated across the specified range.
gradation_list = [] # Holds the value taken by the variable for each datapoint.
fixed_calculation_counter = 0
total_impedance, total_current = [], []

# Other
print_view = 0 # Used for troubleshooting.


###########################################################################
# Basic Operations

def add(z_1, z_2):
    """ Adds complex numbers, given as two-item lists. """
    real_sum = z_1[0] + z_2[0]
    imaginary_sum = z_1[1] + z_2[1]
    result = [real_sum, imaginary_sum]
    return result

def subtract(z_1, z_2):
    """ Subtracts complex numbers, given as two-item lists. """
    real_difference = z_1[0] - z_2[0]
    imaginary_difference = z_1[1] - z_2[1]
    result = [real_difference, imaginary_difference]
    return result
    
def multiply(z_1, z_2):
    """ Multiplies complex numbers, given as two-item lists. """
    real_product = (z_1[0] * z_2[0]) - (z_1[1] * z_2[1])
    imaginary_product = (z_1[0] * z_2[1]) + (z_1[1] * z_2[0])
    result = [real_product, imaginary_product]
    return result
    
def divide(z_1, z_2):
    """ Divides complex numbers, given as two-item lists. """
    real_numerator = (z_1[0] * z_2[0]) + (z_1[1] * z_2[1])
    imaginary_numerator = (z_1[1] * z_2[0]) - (z_1[0] * z_2[1])
    denominator = (z_2[0])**2 + (z_2[1])**2
    real_quotient = real_numerator / denominator
    imaginary_quotient = imaginary_numerator / denominator
    result = [real_quotient, imaginary_quotient]
    return result
    
def parallel(z_1, z_2):
    numerator = multiply(z_1, z_2)
    denominator = add(z_1, z_2)
    result = divide(numerator, denominator)
    return result
    

###########################################################################
# Functions

def impedance_calculations():
    """ Updates the impedance at a given frequency for all components. """
    global angular_frequency, R_op_impedance, C_Rb_impedance, R_sr_impedance, R_ex_impedance, C_Xe_impedance, R_w_impedance
    if print_view == 1: print("impedance_calculations():")
    angular_frequency = 2 * 3.14159265359 * frequency
    R_op_impedance = [R_op, 0]
    C_Rb_impedance = [0, -1/(angular_frequency * C_Rb)]
    R_sr_impedance = [R_sr, 0]
    R_ex_impedance = [R_ex, 0]
    C_Xe_impedance = [0, -1/(angular_frequency * C_Xe)]
    R_w_impedance = [R_w, 0]
    if print_view == 1: print(f"R_op_impedance:\t{R_op_impedance}\nC_Rb_impedance:\t{C_Rb_impedance}\nR_sr_impedance:\t{R_sr_impedance}\nR_ex_impedance:\t{R_ex_impedance}\nC_Xe_impedance:\t{C_Xe_impedance}\nR_w_impedance:\t{R_w_impedance}\n") # Optional.
    reduce_circuit()

def reduce_circuit():
    """ Determines the total impedance and current of the circuit, given some input voltage. """
    global total_impedance, total_current
    if print_view == 1: print("reduce_circuit():")
    parallel_1 = parallel(R_w_impedance, C_Xe_impedance)
    series_1 = add(parallel_1, R_ex_impedance)
    parallel_2 = parallel(series_1, R_sr_impedance)
    parallel_3 = parallel(parallel_2, C_Rb_impedance)
    series_2 = add(parallel_3, R_op_impedance)
    total_impedance = add(series_2, input_impedance)
    total_current = divide(input_voltage, total_impedance)
    total_impedance = [total_impedance[0]-input_impedance[0], total_impedance[1]]
    return total_impedance, total_current
    
def solve_circuit(total_current, parallel_impedance):
    if print_view == 1: print("solve_circuit():\n")
    R_op_voltage = multiply(total_current, R_op_impedance)
    C_Rb_voltage = subtract(input_voltage, R_op_voltage)
    C_Rb_current = divide(C_Rb_voltage, C_Rb_impedance)
    other_current = subtract(total_current, C_Rb_current)
    R_sr_voltage = subtract(input_voltage, R_op_voltage)
    R_sr_current = divide(R_sr_voltage, R_sr_impedance)
    R_ex_current = subtract(other_current, R_sr_current)
    R_ex_voltage = multiply(R_ex_current, R_ex_impedance)
    C_Xe_voltage = subtract(input_voltage, R_op_voltage)
    C_Xe_voltage = subtract(C_Xe_voltage, R_ex_voltage)
    C_Xe_current = divide(C_Xe_voltage, C_Xe_impedance)
    R_w_current = subtract(R_ex_current, C_Xe_current)
    R_w_voltage = multiply(R_w_current, R_w_impedance)

    frequency_list.append(frequency)
    total_values = [input_voltage, total_current, total_impedance]
    total_list.append(total_values)
    R_op_values = [R_op_voltage, total_current, R_op_impedance]
    R_op_list.append(R_op_values)
    C_Rb_values = [C_Rb_voltage, C_Rb_current, C_Rb_impedance]
    C_Rb_list.append(C_Rb_values)
    R_sr_values = [R_sr_voltage, R_sr_current, R_sr_impedance]
    R_sr_list.append(R_sr_values)
    R_ex_values = [R_ex_voltage, R_ex_current, R_ex_impedance]
    R_ex_list.append(R_ex_values)
    C_Xe_values = [C_Xe_voltage, C_Xe_current, C_Xe_impedance]
    C_Xe_list.append(C_Xe_values)
    R_w_values = [R_w_voltage, R_w_current, R_w_impedance]
    R_w_list.append(R_w_values)

def export_data():
    """ Saves current calculation lists to tab separated values in a text file. """
    if print_view == 1: print("export_data():\n")
    with open("=data.txt", 'w', encoding='utf-8') as data_file:
        print(f"Frequency [Hz]\tTotal voltage (real) [V]\tTotal voltage (imaginary) [V]\tTotal current (real) [A]\tTotal current (imaginary) [A]\tTotal impedance (real) [Ω]\tTotal impedance (imaginary) [Ω]\tR_op voltage (real) [V]\tR_op voltage (imaginary) [V]\tR_op current (real) [A]\tR_op current (imaginary) [A]\tR_op impedance (real) [Ω]\tR_op impedance (imaginary) [Ω]\tC_Rb voltage (real) [V]\tC_Rb voltage (imaginary) [V]\tC_Rb current (real) [A]\tC_Rb current (imaginary) [A]\tC_Rb impedance (real) [Ω]\tC_Rb impedance (imaginary) [Ω]\tR_sr voltage (real) [V]\tR_sr voltage (imaginary) [V]\tR_sr current (real) [A]\tR_sr current (imaginary) [A]\tR_sr impedance (real) [Ω]\tR_sr impedance (imaginary) [Ω]\tR_ex voltage (real) [V]\tR_ex voltage (imaginary) [V]\tR_ex current (real) [A]\tR_ex current (imaginary) [A]\tR_ex impedance (real) [Ω]\tR_ex impedance (imaginary) [Ω]\tC_Xe voltage (real) [V]\tC_Xe voltage (imaginary) [V]\tC_Xe current (real) [A]\tC_Xe current (imaginary) [A]\tC_Xe impedance (real) [Ω]\tC_Xe impedance (imaginary) [Ω]\tR_w voltage (real) [V]\tR_w voltage (imaginary) [V]\tR_w current (real) [A]\tR_w current (imaginary) [A]\tR_w impedance (real) [Ω]\tR_w impedance (imaginary) [Ω]", file=data_file)
        for i in range(len(total_list)):
            print(f"{frequency_list[i]}\t{total_list[i][0][0]}\t{total_list[i][0][1]}\t{total_list[i][1][0]}\t{total_list[i][1][1]}\t{total_list[i][2][0]}\t{total_list[i][2][1]}\t{R_op_list[i][0][0]}\t{R_op_list[i][0][1]}\t{R_op_list[i][1][0]}\t{R_op_list[i][1][1]}\t{R_op_list[i][2][0]}\t{R_op_list[i][2][1]}\t{C_Rb_list[i][0][0]}\t{C_Rb_list[i][0][1]}\t{C_Rb_list[i][1][0]}\t{C_Rb_list[i][1][1]}\t{C_Rb_list[i][2][0]}\t{C_Rb_list[i][2][1]}\t{R_sr_list[i][0][0]}\t{R_sr_list[i][0][1]}\t{R_sr_list[i][1][0]}\t{R_sr_list[i][1][1]}\t{R_sr_list[i][2][0]}\t{R_sr_list[i][2][1]}\t{R_ex_list[i][0][0]}\t{R_ex_list[i][0][1]}\t{R_ex_list[i][1][0]}\t{R_ex_list[i][1][1]}\t{R_ex_list[i][2][0]}\t{R_ex_list[i][2][1]}\t{C_Xe_list[i][0][0]}\t{C_Xe_list[i][0][1]}\t{C_Xe_list[i][1][0]}\t{C_Xe_list[i][1][1]}\t{C_Xe_list[i][2][0]}\t{C_Xe_list[i][2][1]}\t{R_w_list[i][0][0]}\t{R_w_list[i][0][1]}\t{R_w_list[i][1][0]}\t{R_w_list[i][1][1]}\t{R_w_list[i][2][0]}\t{R_w_list[i][2][1]}", file=data_file)

def print_values():
    print("##################################################################################")
    print(f"Sampling rate:\t\t\t{sampling_rate}\n\nSupply voltage [V]:\t\t({input_voltage[0]:.2f})+i({input_voltage[1]:.2f})\nSupply impedance [Ω]:\t\t({input_impedance[0]:.2f})+i({input_impedance[1]:.2f})\nFrequency [MHz]:\t\t{(frequency*10**(-6)):.2f}\nAngular frequency [s⁻¹]:\t{angular_frequency:.2e}\n")
    print(f"Frequency:\t\t\t{frequency_list[0]}\nTotal voltage:\t\t\t{total_list[0][0]}\nTotal current:\t\t\t{total_list[0][1]}\nTotal impedance:\t\t{total_list[0][2]}\nR_op voltage:\t\t\t{R_op_list[0][0]}\nR_op current:\t\t\t{R_op_list[0][1]}\nR_op impedance:\t\t\t{R_op_list[0][2]}\nC_Rb voltage:\t\t\t{C_Rb_list[0][0]}\nC_Rb current:\t\t\t{C_Rb_list[0][1]}\nC_Rb impedance:\t\t\t{C_Rb_list[0][2]}\nR_sr voltage:\t\t\t{R_sr_list[0][0]}\nR_sr current:\t\t\t{R_sr_list[0][1]}\nR_sr impedance:\t\t\t{R_sr_list[0][2]}\nR_ex voltage:\t\t\t{R_ex_list[0][0]}\nR_ex current:\t\t\t{R_ex_list[0][1]}\nR_ex impedance:\t\t\t{R_ex_list[0][2]}\nC_Xe voltage:\t\t\t{C_Xe_list[0][0]}\nC_Xe current:\t\t\t{C_Xe_list[0][1]}\nC_Xe impedance:\t\t\t{C_Xe_list[0][2]}\nR_w voltage:\t\t\t{R_w_list[0][0]}\nR_w current:\t\t\t{R_w_list[0][1]}\nR_w impedance:\t\t\t{R_w_list[0][2]}")
    print("##################################################################################\n\n")

def update_fixed_values():
    global frequency, sampling_rate, R_op, C_Rb, R_sr, R_ex, C_Xe, R_w, frequency_set, R_op_set, C_Rb_set, R_sr_set, R_ex_set, C_Xe_set, R_w_set
    action = int(input("Select a value to change:\n1) Frequency\n2) Sampling rate\n3) R_op\n4) C_Rb\n5) R_sr\n6) R_ex\n7) C_Xe\n8) R_w\n0) Quit to main menu.\n\n"))
    print()
    if action == 1:
        frequency = float(input("Enter frequency [Hz]:\t"))
    elif action == 2:
        sampling_rate = int(input("Enter sampling rate:\t"))
    elif action == 3:
        R_op = float(input("Enter optical resistance (R_op) [Ω]:\t"))
    elif action == 4:
        C_Rb = float(input("Enter rubidium capacitance [F]:\t"))
    elif action == 5:
        R_sr = float(input("Enter spin relaxation resistance [Ω]:\t"))
    elif action == 6:
        R_ex = float(input("Enter spin exchange resistance [Ω]:\t"))
    elif action == 7:
        C_Xe = float(input("Enter xenon capacitance [F]:\t"))
    elif action == 8:
        R_w = float(input("Enter wall resistance [Ω]:\t"))
    frequency_set, R_op_set, C_Rb_set, R_sr_set, R_ex_set, C_Xe_set, R_w_set = frequency, R_op, C_Rb, R_sr, R_ex, C_Xe, R_w
    print("\n")
    impedance_calculations()

def fixed_calculation():
    global tuning_impedance, fixed_calculation_counter
    impedance_calculations()
    total_current, parallel_impedance = reduce_circuit()
    solve_circuit(total_current, parallel_impedance)

def cluster_calculation():
    global frequency, R_op, C_Rb, R_sr, R_ex, C_Xe, R_w
    action = int(input("Select a variable:\n1) Frequency\n2) R_op\n3) C_Rb\n4) R_sr\n5) R_ex\n6) C_Xe\n7) R_w\n0) Quit to main menu.\n\n"))
    print("\n")
    if action != 0:
        print("Enter 0 for each variable to quit to main menu.")
        if action == 1:
            minimum = float(input("Enter a minimum value [Hz]:\t"))
            maximum = float(input("Enter a maximum value [Hz]:\t"))
            if (minimum + maximum) != 0:
                frequency = minimum
                gradation_list.append(frequency)
                gradation = ((maximum - minimum)/sampling_rate) # Allows for a variable number of datapoints.
                print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation}\n")
                for i in range(sampling_rate+1):
                    fixed_calculation() # Calculates values for the current parameters.
                    frequency += gradation # Sets the next parameter.
                    gradation_list.append(frequency) # Maintains a memory of each parameter taken by the variable.
                return True
            else:
                return False
    else:
        return False

def dense_calculation():
    global tuning_capacitance, coupling_capacitance
    print("Enter 0 for each variable to quit to main menu.")
    tuning_minimum = float(input("Enter a minimum tuning capacitance [pF]:\t"))
    tuning_maximum = float(input("Enter a maximum tuning capacitance [pF]:\t"))
    coupling_minimum = float(input("Enter a minimum coupling capacitance [pF]:\t"))
    coupling_maximum = float(input("Enter a maximum coupling capacitance [pF]:\t"))
    print("\n")
    if (tuning_minimum + tuning_maximum + coupling_minimum + coupling_maximum) != 0:
        tuning_capacitance = tuning_minimum*10**(-12)
        coupling_capacitance = coupling_minimum*10**(-12)
        tuning_gradation_list.append(tuning_capacitance)
        coupling_gradation_list.append(coupling_capacitance)
        tuning_gradation = (((tuning_maximum*10**(-12)) - (tuning_minimum*10**(-12)))/sampling_rate) # Allows for a variable number of datapoints.
        coupling_gradation = (((coupling_maximum*10**(-12)) - (coupling_minimum*10**(-12)))/sampling_rate)
        print(f"Sampling rate:\t\t\t{sampling_rate}\nTuning gradation [F]:\t\t{tuning_gradation}\nCoupling gradation [F]:\t\t{coupling_gradation}\n")
        for i in range(sampling_rate+1): # Cycles through tuning parameters.
            for i in range(sampling_rate+1): # Cycles through coupling parameters.
                fixed_calculation() # Calculates values for the current parameters.
                coupling_capacitance += coupling_gradation # Sets the next parameter.
                coupling_gradation_list.append(tuning_capacitance) # Maintains a memory of each parameter taken by the variable.
            coupling_capacitance = coupling_minimum*10**(-12)
            tuning_capacitance += tuning_gradation # Sets the next parameter.
            tuning_gradation_list.append(tuning_capacitance) # Maintains a memory of each parameter taken by the variable.
        #print(f"tuning_capacitance: {tuning_capacitance}\ncoupling_capacitance: {coupling_capacitance}\n")

def complex_algebra():
    print("Enter 0 for each variable to quit to main menu.")
    x_1 = float(input("Enter Re(z_1):\t"))
    y_1 = float(input("Enter Im(z_1):\t"))
    x_2 = float(input("Enter Re(z_2):\t"))
    y_2 = float(input("Enter Im(z_2):\t"))
    print("\n")
    if (x_1 + y_1 + x_2 + y_2) != 0:
        z_1, z_2 = [x_1, y_1], [x_2, y_2]
        operation = int(input("Select an operation:\n1) Addition.\n2) Subtraction.\n3) Multiplication.\n4) Division.\n5) Parallel components.\n0) Quit to main menu.\n\n"))
        print("\n")
        if operation != 0:
            if operation == 1:
                result = add(z_1, z_2)
            if operation == 2:
                result = subtract(z_1, z_2)
            if operation == 3:
                result = multiply(z_1, z_2)
            if operation == 4:
                result = divide(z_1, z_2)
            if operation == 5:
                result = parallel(z_1, z_2)
            print(f"Result:\t({result[0]})+i({result[1]})\n\n")

def reset_variables():
    global frequency, R_op, C_Rb, R_sr, R_ex, C_Xe, R_w
    if print_view == 1: print("reset_variables():\n")
    frequency, R_op, C_Rb, R_sr, R_ex, C_Xe, R_w = frequency_set, R_op_set, C_Rb_set, R_sr_set, R_ex_set, C_Xe_set, R_w_set
    
def reset_lists():
    global R_op_list, C_Rb_list, R_sr_list, R_ex_list, C_Xe_list, R_w_list, total_list, frequency_list
    if print_view == 1: print("reset_lists():\n")
    R_op_list.clear()
    C_Rb_list.clear()
    R_sr_list.clear()
    R_ex_list.clear()
    C_Xe_list.clear()
    R_w_list.clear()
    total_list.clear()
    frequency_list.clear()
    gradation_list.clear()
    total_impedance.clear()
    total_current.clear()
    fixed_calculation_counter = 0

def main():
    fixed_calculation()
    action_1 = int(input("Enter an action:\n1) View fixed values.\n2) Change a value.\n3) Run calculations.\n0) Quit.\n\n"))
    print("\n")
    if action_1 == 0:
        pass
    else:
        if action_1 == 1:
            print_values()
        elif action_1 == 2:
            update_fixed_values()
        elif action_1 == 3:
            action_2 = int(input("Select calculation:\n1) Fixed calculation (no variables).\n2) Cluster calculation (one variable).\n3) Dense calculation (two variables).\n4) Complex algebra (four variables).\n0) Quit to main menu.\n\n"))
            print("\n")
            if action_2 != 0:
                if action_2 == 1:
                    reset_lists()
                    fixed_calculation()
                    print("Data exported successfully.\n\n")
                elif action_2 == 2:
                    reset_lists()
                    operation = cluster_calculation()
                    if operation:
                        print("Data exported successfully.\n\n")
                elif action_2 == 3:
                    dense_calculation()
                    print("Data exported successfully.\n\n")
                elif action_2 == 4:
                    complex_algebra()
                export_data()
        reset_variables()
        reset_lists()
        main()

###########################################################################
# Global Script

print("\n##################################################################################")
print("Welcome!")
print("##################################################################################\n\n")
main()


###########################################################################
###########################################################################
