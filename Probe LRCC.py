###########################################################################
###########################################################################
#
# Alex Heinrich
# Circuit Analyzer
# Outputs a CSV file
#
###########################################################################
###########################################################################

###########################################################################
# Default Defined Parameters
# These are variables that may be adjusted in the program.

# Voltage Supply
input_voltage, input_impedance = [1, 0], [50, 0] # Units of volts and ohms.
frequency, frequency_set = 40*(10**6), 40*(10**6) # Units of hertz. Enter the same value for both parameters.
angular_frequency = 2 * 3.14159265359 * frequency # Units of radians per second.
frequency_list = [] # List initialization.

# Components
inductor_resistance = 0.1 # Units of ohms.
inductance, inductance_set = 0.6*(10**(-6)), 0.6*(10**(-6)) # Units of henrys.
tuning_capacitance, tuning_capacitance_set = 25.2*(10**(-12)), 25.2*(10**(-12)) # Units of farads.
coupling_capacitance, coupling_capacitance_set = 1.19*(10**(-12)), 1.19*(10**(-12)) # Units of farads.
inductor_impedance = [0, 0] # Units of ohms. Serves as a placeholder until calculation.
tuning_impedance = [0, 0] # Units of ohms. Serves as a placeholder until calculation.
coupling_impedance = [0, 0] # Units of ohms. Serves as a placeholder until calculation.
inductor_list, tuning_list, coupling_list, total_list = [], [], [], [] # List initialization.

# Other
sampling_rate = 100 # Sets the number of datapoints calculated across the specified range.
fixed_calculation_counter = 0 # Used to correct undesired data duplication.
total_impedance, total_current = [], []
print_view = 0 # Used for troubleshooting. Set to 1 to view optional messages.


###########################################################################
# Basic Operations
# Here, z_n[0] is the real component, and z_n[1] is the imaginary component.

def add(z_1, z_2):
    """ Adds complex numbers. """
    real_sum = z_1[0] + z_2[0]
    imaginary_sum = z_1[1] + z_2[1]
    result = [real_sum, imaginary_sum]
    return result

def subtract(z_1, z_2):
    """ Subtracts complex numbers. """
    real_difference = z_1[0] - z_2[0]
    imaginary_difference = z_1[1] - z_2[1]
    result = [real_difference, imaginary_difference]
    return result
    
def multiply(z_1, z_2):
    """ Multiplies complex numbers. """
    real_product = (z_1[0] * z_2[0]) - (z_1[1] * z_2[1])
    imaginary_product = (z_1[0] * z_2[1]) + (z_1[1] * z_2[0])
    result = [real_product, imaginary_product]
    return result
    
def divide(z_1, z_2):
    """ Divides complex numbers. """
    real_numerator = (z_1[0] * z_2[0]) + (z_1[1] * z_2[1])
    imaginary_numerator = (z_1[1] * z_2[0]) - (z_1[0] * z_2[1])
    denominator = (z_2[0])**2 + (z_2[1])**2
    real_quotient = real_numerator / denominator
    imaginary_quotient = imaginary_numerator / denominator
    result = [real_quotient, imaginary_quotient]
    return result
    
def parallel(z_1, z_2):
    """ Adds two complex numbers as an inverse reciprocal sum. """
    numerator = multiply(z_1, z_2)
    denominator = add(z_1, z_2)
    result = divide(numerator, denominator)
    return result
    

###########################################################################
# Functions

def impedance_calculations():
    """ Updates the impedance at a given frequency for all components. """
    global angular_frequency, inductor_impedance, tuning_impedance, coupling_impedance
    if print_view == 1: print("impedance_calculations():") # Used for troubleshooting.
    angular_frequency = 2 * 3.14159265359 * frequency # Units of radians per second.
    inductor_impedance = [inductor_resistance, angular_frequency * inductance] # Units of ohms.
    tuning_impedance = [0, -1/(angular_frequency * tuning_capacitance)] # Units of ohms.
    coupling_impedance = [0, -1/(angular_frequency * coupling_capacitance)] # Units of ohms.
    reduce_circuit()

def reduce_circuit():
    """ Determines the total impedance and current of the circuit, given some input voltage. """
    global total_impedance, total_current
    if print_view == 1: print("reduce_circuit():") # Used for troubleshooting.
    parallel_impedance = parallel(inductor_impedance, tuning_impedance) # Inductor and tuning capacitor.
    total_impedance = add(parallel_impedance, coupling_impedance) # Inductor, tuning capacitor, and coupling capacitor.
    effective_impedance = add(total_impedance, input_impedance) # Includes input resistance for total current.
    total_current = divide(input_voltage, effective_impedance) # Current as influenced by the input resistance.
    return total_current, parallel_impedance
    
def solve_circuit(total_current, parallel_impedance):
    """ Calculates the voltage and current across each component, given the total current of the circuit. """
    if print_view == 1: print("solve_circuit():\n") # Used for troubleshooting.
    coupling_voltage = multiply(total_current, coupling_impedance) # Coupling capacitor.
    parallel_voltage = multiply(total_current, parallel_impedance) # Tuning capacitor and inductor.
    tuning_current = divide(parallel_voltage, tuning_impedance) # Tuning capacitor.
    inductor_current = divide(parallel_voltage, inductor_impedance) # Inductor.
    total_values = [input_voltage, total_current, total_impedance] # Totals as seen from the voltage source.
    coupling_values = [coupling_voltage, total_current, coupling_impedance, coupling_capacitance]
    tuning_values = [parallel_voltage, tuning_current, tuning_impedance, tuning_capacitance]
    inductor_values = [parallel_voltage, inductor_current, inductor_impedance, inductance]
    frequency_list.append(frequency) # Logs the frequency used in the calculations.
    total_list.append(total_values) # Logs the results of the calculations.
    inductor_list.append(inductor_values) # Logs the results of the calculations.
    tuning_list.append(tuning_values) # Logs the results of the calculations.
    coupling_list.append(coupling_values) # Logs the results of the calculations.

def export_data():
    """ Saves current calculation lists to tab separated values in a text file. """
    if print_view == 1: print("export_data():\n") # Used for troubleshooting.
    with open("=data.txt", 'w', encoding='utf-8') as data_file:
        export_titles = ("Frequency [Hz]\t"
            "Total voltage (real) [V]\t"
            "Total voltage (imaginary) [V]\t"
            "Total current (real) [A]\t"
            "Total current (imaginary) [A]\t"
            "Total impedance (real) [Ω]\t"
            "Total impedance (imaginary) [Ω]\t"
            "Inductance [H]\t"
            "Inductor voltage (real) [V]\t"
            "Inductor voltage (imaginary) [V]\t"
            "Inductor current (real) [A]\t"
            "Inductor current (imaginary) [A]\t"
            "Inductor impedance (real) [Ω]\t"
            "Inductor impedance (imaginary) [Ω]\t"
            "Tuning capacitance [F]\t"
            "Tuning voltage (real) [V]\t"
            "Tuning voltage (imaginary) [V]\t"
            "Tuning current (real) [A]\t"
            "Tuning current (imaginary) [A]\t"
            "Tuning impedance (real) [Ω]\t"
            "Tuning impedance (imaginary) [Ω]\t"
            "Coupling capacitance [F]\t"
            "Coupling voltage (real) [V]\t"
            "Coupling voltage (imaginary) [V]\t"
            "Coupling current (real) [A]\t"
            "Coupling current (imaginary) [A]\t"
            "Coupling impedance (real) [Ω]\t"
            "Coupling impedance (imaginary) [Ω]\t")
        print(export_titles, file=data_file)
        for i in range(len(total_list)):
            export_values = (f"{frequency_list[i]}\t"
                f"{total_list[i][0][0]}\t"
                f"{total_list[i][0][1]}\t"
                f"{total_list[i][1][0]}\t"
                f"{total_list[i][1][1]}\t"
                f"{total_list[i][2][0]}\t"
                f"{total_list[i][2][1]}\t"
                f"{inductor_list[i][0][-1]}\t"
                f"{inductor_list[i][0][0]}\t"
                f"{inductor_list[i][0][1]}\t"
                f"{inductor_list[i][1][0]}\t"
                f"{inductor_list[i][1][1]}\t"
                f"{inductor_list[i][2][0]}\t"
                f"{inductor_list[i][2][1]}\t"
                f"{tuning_list[i][0][-1]}\t"
                f"{tuning_list[i][0][0]}\t"
                f"{tuning_list[i][0][1]}\t"
                f"{tuning_list[i][1][0]}\t"
                f"{tuning_list[i][1][1]}\t"
                f"{tuning_list[i][2][0]}\t"
                f"{tuning_list[i][2][1]}\t"
                f"{coupling_list[i][0][-1]}\t"
                f"{coupling_list[i][0][0]}\t"
                f"{coupling_list[i][0][1]}\t"
                f"{coupling_list[i][1][0]}\t"
                f"{coupling_list[i][1][1]}\t"
                f"{coupling_list[i][2][0]}\t"
                f"{coupling_list[i][2][1]}")
            print(export_values, file=data_file)

def print_values():
    """ Prints values in the program. """
    print("##################################################################################")
    defined_parameters = (f"Sampling rate:\t\t\t{sampling_rate}\n"
        f"Supply voltage [V]:\t\t({input_voltage[0]:.2f})+i({input_voltage[1]:.2f})\n"
        f"Supply impedance [Ω]:\t\t({input_impedance[0]:.2f})+i({input_impedance[1]:.2f})\n"
        f"Frequency [Hz]:\t\t\t{(frequency):.2e}\n"
        f"Angular frequency [s⁻¹]:\t{angular_frequency:.2e}\n"
        f"Inductance [H]:\t\t\t{inductance:.2e}\n"
        f"Tuning capacitance [F]:\t\t{tuning_capacitance:.2e}\n"
        f"Coupling capacitance [F]:\t{coupling_capacitance:.2e}\n")
    calculated_values = (f"Total current [A]:\t\t({total_list[0][1][0]:.2e})+i({total_list[0][1][1]:.2e})\n"
        f"Total impedance [Ω]:\t\t({total_list[0][2][0]:.2e})+i({total_list[0][2][1]:.2e})\n"
        f"Inductor voltage [V]:\t\t({inductor_list[0][0][0]:.2e})+i({inductor_list[0][0][1]:.2e})\n"
        f"Inductor current [A]:\t\t({inductor_list[0][1][0]:.2e})+i({inductor_list[0][1][1]:.2e})\n"
        f"Inductor impedance [Ω]:\t\t({inductor_list[0][2][0]:.2e})+i({inductor_list[0][2][1]:.2e})\n"
        f"Tuning voltage [V]:\t\t({tuning_list[0][0][0]:.2e})+i({tuning_list[0][0][1]:.2e})\n"
        f"Tuning current [A]:\t\t({tuning_list[0][1][0]:.2e})+i({tuning_list[0][1][1]:.2e})\n"
        f"Tuning impedance [Ω]:\t\t({tuning_list[0][2][0]:.2e})+i({tuning_list[0][2][1]:.2e})\n"
        f"Coupling voltage [V]:\t\t({coupling_list[0][0][0]:.2e})+i({coupling_list[0][0][1]:.2e})\n"
        f"Coupling current [A]:\t\t({coupling_list[0][1][0]:.2e})+i({coupling_list[0][1][1]:.2e})\n"
        f"Coupling impedance [Ω]:\t\t({coupling_list[0][2][0]:.2e})+i({coupling_list[0][2][1]:.2e})")
    print(defined_parameters)
    print(calculated_values)
    print("##################################################################################\n\n")

def update_fixed_values():
    """ Updates a parameter based on user entry. It accepts scientific notation (ex. 6.63e-34). """
    global frequency, sampling_rate, inductance, tuning_capacitance, coupling_capacitance, frequency_set, inductance_set, tuning_capacitance_set, coupling_capacitance_set
    action = int(input("Select a value to change:\n1) Frequency\n2) Sampling rate\n3) Inductance\n4) Inductor resistance\n5) Tuning capacitance\n6) Coupling capacitance\n0) Quit to main menu.\n\n"))
    print()
    if action == 1:
        frequency = float(input("Enter frequency [Hz]:\t"))
    elif action == 2:
        sampling_rate = int(float(input("Enter sampling rate:\t")))
    elif action == 3:
        inductance = float(input("Enter inductance [H]:\t"))
    elif action == 4:
        inductor_resistance = float(input("Enter resistance [Ω]:\t"))
    elif action == 5:
        tuning_capacitance = float(input("Enter tuning capacitance [F]:\t"))
    elif action == 6:
        coupling_capacitance = float(input("Enter coupling capacitance [F]:\t"))
    frequency_set, inductance_set, tuning_capacitance_set, coupling_capacitance_set = frequency, inductance, tuning_capacitance, coupling_capacitance
    print("\n")
    impedance_calculations()

def fixed_calculation():
    """ Solves the circuit with one set of parameters. """
    global tuning_impedance, fixed_calculation_counter
    impedance_calculations()
    total_current, parallel_impedance = reduce_circuit()
    solve_circuit(total_current, parallel_impedance)

def cluster_calculation():
    """ Solves the circuit with one parameter as a variable. """
    global tuning_capacitance, coupling_capacitance, frequency
    action = int(input("Select a variable:\n1) Tuning capacitance.\n2) Coupling capacitance.\n3) Frequency.\n0) Quit to main menu.\n\n"))
    print("\n")
    if action != 0:
        print("Enter 0 for each variable to quit to main menu.")
        if action == 1: # Sets the tuning capacitor as a variable.
            minimum = float(input("Enter a minimum value [F]:\t")) # Sets minimum capacitance.
            maximum = float(input("Enter a maximum value [F]:\t")) # Sets maximum capacitance.
            if (minimum + maximum) != 0:
                tuning_capacitance = minimum # Sets the minimum as the first value in the series.
                gradation = ((maximum - minimum)/sampling_rate) # Sets the number of farads between each value.
                print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation}\n")
                for i in range(sampling_rate+1): # Cycles through each value in the chosen interval.
                    fixed_calculation() # Calculates values for the current parameters.
                    tuning_capacitance += gradation # Sets the next parameter.
                return True
            else:
                return False
        if action == 2: # Sets the coupling capacitor as the variable.
            minimum = float(input("Enter a minimum value [F]:\t")) # Sets minimum capacitance.
            maximum = float(input("Enter a maximum value [F]:\t")) # Sets maximum capacitance.
            if (minimum + maximum) != 0:
                coupling_capacitance = minimum # Sets the minimum as the first value in the series.
                gradation = ((maximum - minimum)/sampling_rate) # Sets the number of farads between each value.
                print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation}\n")
                for i in range(sampling_rate+1): # Cycles through each value in the chosen interval.
                    fixed_calculation() # Calculates values for the current parameters.
                    coupling_capacitance += gradation # Sets the next parameter.
                return True
            else:
                return False
        if action == 3: # Sets the input frequency as the variable.
            minimum = float(input("Enter a minimum value [Hz]:\t")) # Sets minimum frequency.
            maximum = float(input("Enter a maximum value [Hz]:\t")) # Sets maximum frequency.
            if (minimum + maximum) != 0:
                frequency = minimum # Sets the minimum as the first value in the series.
                gradation = ((maximum - minimum)/sampling_rate) # Sets the number of hertz between each value.
                print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation}\n")
                for i in range(sampling_rate+1): # Cycles through each value in the chosen interval.
                    fixed_calculation() # Calculates values for the current parameters.
                    frequency += gradation # Sets the next parameter.
                return True
            else:
                return False
    else:
        return False

def dense_calculation():
    """ Solves the circuit with both capacitance values as variables. """
    global tuning_capacitance, coupling_capacitance
    print("Enter 0 for each variable to quit to main menu.")
    tuning_minimum = float(input("Enter a minimum tuning capacitance [F]:\t")) # Sets minimum capacitance.
    tuning_maximum = float(input("Enter a maximum tuning capacitance [F]:\t")) # Sets maximum capacitance.
    coupling_minimum = float(input("Enter a minimum coupling capacitance [F]:\t")) # Sets minimum capacitance.
    coupling_maximum = float(input("Enter a maximum coupling capacitance [F]:\t")) # Sets maximum capacitance.
    print("\n")
    if (tuning_minimum + tuning_maximum + coupling_minimum + coupling_maximum) != 0:
        tuning_capacitance = tuning_minimum # Sets the minimum as the first value in the series.
        coupling_capacitance = coupling_minimum # Sets the minimum as the first value in the series.
        tuning_gradation = (tuning_maximum - tuning_minimum)/sampling_rate # Sets the number of farads between each value.
        coupling_gradation = (coupling_maximum - coupling_minimum)/sampling_rate # Sets the number of farads between each value.
        print(f"Sampling rate:\t\t\t{sampling_rate}\nTuning gradation [F]:\t\t{tuning_gradation}\nCoupling gradation [F]:\t\t{coupling_gradation}\n")
        for i in range(sampling_rate+1): # Cycles through tuning parameters.
            for i in range(sampling_rate+1): # Cycles through coupling parameters.
                fixed_calculation() # Calculates values for the current parameters.
                coupling_capacitance += coupling_gradation # Sets the next parameter.
            coupling_capacitance = coupling_minimum # Sets the minimum as the first value in the series.
            tuning_capacitance += tuning_gradation # Sets the next parameter.

def complex_algebra():
    """ Computes binary operations on complex numbers. """
    print("Enter 0 for each variable to quit to main menu.")
    x_1 = float(input("Enter Re(z_1):\t")) # Sets first real component.
    y_1 = float(input("Enter Im(z_1):\t")) # Sets first imaginary component.
    x_2 = float(input("Enter Re(z_2):\t")) # Sets second real component.
    y_2 = float(input("Enter Im(z_2):\t")) # Sets second imaginary component.
    print("\n")
    if (x_1 + y_1 + x_2 + y_2) != 0:
        z_1, z_2 = [x_1, y_1], [x_2, y_2] # Pairs each component as a list.
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
    """ Reverts to the default values, rather than the last values calculated. Used in main(). """
    global frequency, inductance, tuning_capacitance, coupling_capacitance
    if print_view == 1: print("reset_variables():\n") # Used for troubleshooting.
    frequency, inductance, tuning_capacitance, coupling_capacitance = frequency_set, inductance_set, tuning_capacitance_set, coupling_capacitance_set
    
def reset_lists():
    """ Clears the data from the last calculation to prepare for the next. Used in main(). """
    global total_list, frequency_list, inductor_list, tuning_list, coupling_list
    if print_view == 1: print("reset_lists():\n") # Used for troubleshooting.
    total_list.clear()
    frequency_list.clear()
    inductor_list.clear()
    tuning_list.clear()
    coupling_list.clear()
    total_impedance.clear()
    total_current.clear()
    fixed_calculation_counter = 0

def main():
    fixed_calculation() # Solves the circuit for the default or updated parameters.
    try: action_1 = int(input("Enter an action:\n1) View fixed values.\n2) Change a value.\n3) Run calculations.\n0) Quit.\n\n"))
    except: action_1 = 0
    print("\n")
    if action_1 == 0:
        print("##################################################################################")
        print("Farewell!")
        print("##################################################################################\n\n")
        pass
    else:
        if action_1 == 1:
            print_values() # Prints parameters and calculations within the program.
        elif action_1 == 2:
            update_fixed_values() # Allows the user to change a parameter.
        elif action_1 == 3:
            action_2 = int(input("Select calculation:\n1) Fixed calculation (no variables).\n2) Cluster calculation (one variable).\n3) Dense calculation (two variables).\n4) Complex algebra (four variables).\n0) Quit to main menu.\n\n"))
            print("\n")
            if action_2 != 0:
                if action_2 == 1:
                    reset_lists()
                    fixed_calculation() # Solves the circuit for one set of parameters.
                    print("Data exported successfully.\n\n")
                elif action_2 == 2:
                    reset_lists()
                    operation = cluster_calculation() # Solves the circuit for one variable.
                    if operation:
                        print("Data exported successfully.\n\n")
                elif action_2 == 3:
                    dense_calculation() # Solves the circuit for two variables.
                    print("Data exported successfully.\n\n")
                elif action_2 == 4:
                    complex_algebra() # Operates on complex numbers.
                export_data() # Exports the resulting data to a text file.
        reset_variables() # Prepares the program for the next calculation.
        reset_lists() # Prepares the program for the next calculation.
        main()

###########################################################################
# Global Script

print("\n##################################################################################")
print("Welcome!")
print("##################################################################################\n\n")
main()


###########################################################################
###########################################################################
