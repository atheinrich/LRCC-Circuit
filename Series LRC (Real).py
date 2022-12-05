###########################################################################
###########################################################################
#
# Alex Heinrich
# Circuit Analyzer
# Outputs a CSV file 
# Differs from Series LRC in the assumption of a real-valued voltage input
# in the differential equation for electric charge over time. This notably
# results in time-dependent impedance functions. The resulting behavior is
# highly asymptotic and not necessarily sustantiated through experiments.
#
###########################################################################
###########################################################################


###########################################################################
# Imports

from math import tan
from math import cos

###########################################################################
# Default Defined Parameters
# These are variables that may be adjusted in the program.

# Voltage Supply
time = 0.001 # Initial condition.
frequency, frequency_set = 40*(10**6), 40*(10**6) # Units of hertz. Enter the same value for both parameters.
angular_frequency = 2 * 3.14159265359 * frequency # Units of radians per second.
input_voltage, input_voltage_set, input_impedance = 1*cos(angular_frequency*time), 1*cos(angular_frequency*time), 50 # Units of volts and ohms.
voltage_list, time_list, frequency_list = [], [], [] # List initialization.

# Components
inductor_resistance = 0.1 # Units of ohms.
inductance, inductance_set = 0.6*(10**(-6)), 0.6*(10**(-6)) # Units of henrys.
coupling_capacitance, coupling_capacitance_set = 1.19*(10**(-12)), 1.19*(10**(-12)) # Units of farads.
inductor_impedance = 0 # Units of ohms. Serves as a placeholder until calculation.
coupling_impedance = 0 # Units of ohms. Serves as a placeholder until calculation.
inductor_list, coupling_list, total_list = [], [], [] # List initialization.

# Other
sampling_rate = 10000 # Sets the number of datapoints calculated across the specified range.
fixed_calculation_counter = 0 # Used to correct undesired data duplication.
total_impedance, total_current = [], []
print_view = 0 # Used for troubleshooting. Set to 1 to view optional messages.

###########################################################################
# Functions

def impedance_calculations():
    """ Updates the impedance at a given frequency for all components. """
    global angular_frequency, input_voltage, inductor_impedance, tuning_impedance, coupling_impedance
    if print_view == 1: print("impedance_calculations():") # Used for troubleshooting.
    angular_frequency = 2 * 3.14159265359 * frequency # Units of radians per second.
    input_voltage = 1 * cos(2 * 3.14159265359 * frequency * time)
    inductor_impedance = inductor_resistance +(angular_frequency*inductance/tan(angular_frequency*time)) # Units of ohms.
    coupling_impedance = -1/(angular_frequency*coupling_capacitance*tan(angular_frequency*time)) # Units of ohms.
    reduce_circuit()

def reduce_circuit():
    """ Determines the total impedance and current of the circuit, given some input voltage. """
    global total_impedance, total_current
    if print_view == 1: print("reduce_circuit():") # Used for troubleshooting.
    total_impedance = inductor_impedance+coupling_impedance
    effective_impedance = total_impedance+input_impedance
    total_current = input_voltage/effective_impedance
    return total_current, total_impedance

def solve_circuit(total_current, total_impedance):
    """ Calculates the voltage and current across each component, given the total current of the circuit. """
    if print_view == 1: print("solve_circuit():\n")
    coupling_voltage = total_current*coupling_impedance
    inductor_voltage = total_current*inductor_impedance
    total_values = [input_voltage, total_current, total_impedance]
    coupling_values = [coupling_voltage, total_current, coupling_impedance, coupling_capacitance]
    inductor_values = [inductor_voltage, total_current, inductor_impedance, inductance]
    time_list.append(time)
    voltage_list.append(input_voltage)
    frequency_list.append(frequency)
    total_list.append(total_values)
    inductor_list.append(inductor_values)
    coupling_list.append(coupling_values)

def export_data():
    """ Saves current calculation lists to tab separated values in a text file. """
    if print_view == 1: print("export_data():\n") # Used for troubleshooting.
    with open("=data.txt", 'w', encoding='utf-8') as data_file:
        export_titles = ("Time [s]\t"
            "Input voltage [V]\t"
            "Frequency [Hz]\t"
            "Total voltage [V]\t"
            "Total current [A]\t"
            "Total impedance [Ω]\t"
            "Inductance [H]\t"
            "Inductor voltage [V]\t"
            "Inductor current [A]\t"
            "Inductor impedance [Ω]\t"
            "Coupling capacitance [F]\t"
            "Coupling voltage [V]\t"
            "Coupling current [A]\t"
            "Coupling impedance [Ω]\t")
        print(export_titles, file=data_file)
        for i in range(len(total_list)):
            export_values = (f"{time_list[i]}\t"
                f"{voltage_list[i]}\t"
                f"{frequency_list[i]}\t"
                f"{total_list[i][0]}\t"
                f"{total_list[i][1]}\t"
                f"{total_list[i][2]}\t"
                f"{inductor_list[i][-1]}\t"
                f"{inductor_list[i][0]}\t"
                f"{inductor_list[i][1]}\t"
                f"{inductor_list[i][2]}\t"
                f"{coupling_list[i][-1]}\t"
                f"{coupling_list[i][0]}\t"
                f"{coupling_list[i][1]}\t"
                f"{coupling_list[i][2]}")
            print(export_values, file=data_file)

def print_values():
    print("##################################################################################")
    print(f"Sampling rate:\t\t\t{sampling_rate}\n\nSupply voltage [V]:\t\t{input_voltage:.2f}\nSupply impedance [Ω]:\t\t{input_impedance:.2f}\nFrequency [Hz]:\t\t\t{(frequency):.2e}\nAngular frequency [s⁻¹]:\t{angular_frequency:.2e}\n")
    print(f"Total current [A]:\t\t{total_list[0][1]:.2e}\nTotal impedance [Ω]:\t\t{total_list[0][2]:.2e}\nInductor voltage [V]:\t\t{inductor_list[0][0]:.2e}\nInductor current [A]:\t\t{inductor_list[0][1]:.2e}\nInductor impedance [Ω]:\t\t{inductor_list[0][2]:.2e}\nCoupling voltage [V]:\t\t{coupling_list[0][0]:.2e}\nCoupling current [A]:\t\t{coupling_list[0][1]:.2e}\nCoupling impedance [Ω]:\t\t{coupling_list[0][2]:.2e}")
    print("##################################################################################\n\n")

def update_fixed_values():
    """ Updates a parameter based on user entry. It accepts scientific notation (ex. 6.63e-34). """
    global frequency, sampling_rate, inductance, coupling_capacitance, frequency_set, inductance_set, coupling_capacitance_set
    action = int(input("Select a value to change:\n1) Frequency\n2) Sampling rate\n3) Inductance\n4) Inductor resistance\n5) Coupling capacitance\n0) Quit to main menu.\n\n"))
    print()
    if action == 1:
        frequency = float(input("Enter frequency [Hz]:\t"))
    elif action == 2:
        sampling_rate = int(input("Enter sampling rate:\t"))
    elif action == 3:
        inductance = float(input("Enter inductance [H]:\t"))
    elif action == 4:
        inductor_resistance = float(input("Enter resistance [Ω]:\t"))
    elif action == 5:
        coupling_capacitance = float(input("Enter coupling capacitance [F]:\t"))
    frequency_set, inductance_set, coupling_capacitance_set = frequency, inductance, coupling_capacitance
    print("\n")
    impedance_calculations()

def fixed_calculation():
    """ Solves the circuit with one set of parameters. """
    global tuning_impedance, fixed_calculation_counter
    impedance_calculations()
    total_current, total_impedance = reduce_circuit()
    solve_circuit(total_current, total_impedance)

def cluster_calculation():
    """ Solves the circuit as one parameter changes. """
    global tuning_capacitance, coupling_capacitance, time, frequency
    action = int(input("Select a variable:\n1) Coupling capacitance.\n2) Frequency.\n3) Time.\n0) Quit to main menu.\n\n"))
    print("\n")
    if action != 0:
        print("Enter 0 for each variable to quit to main menu.")
        if action == 1:
            minimum = float(input("Enter a minimum value [F]:\t"))
            maximum = float(input("Enter a maximum value [F]:\t"))
            if (minimum + maximum) != 0:
                coupling_capacitance = minimum
                gradation = ((maximum - minimum)/sampling_rate) # Allows for a variable number of datapoints.
                print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation}\n")
                for i in range(sampling_rate+1):
                    fixed_calculation() # Calculates values for the current parameters.
                    coupling_capacitance += gradation # Sets the next parameter.
                return True
            else:
                return False
        if action == 2:
            minimum = float(input("Enter a minimum value [Hz]:\t"))
            maximum = float(input("Enter a maximum value [Hz]:\t"))
            if (minimum + maximum) != 0:
                frequency = minimum
                gradation = ((maximum - minimum)/sampling_rate) # Allows for a variable number of datapoints.
                print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation}\n")
                for i in range(sampling_rate+1):
                    fixed_calculation() # Calculates values for the current parameters.
                    frequency += gradation # Sets the next parameter.
                return True
            else:
                return False
        if action == 3:
            minimum = float(input("Enter a minimum value [s]:\t"))
            maximum = float(input("Enter a maximum value [s]:\t"))
            if (minimum + maximum) != 0:
                time = minimum
                gradation = ((maximum - minimum)/sampling_rate) # Allows for a variable number of datapoints.
                print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation [F]:\t\t\t{gradation}\n")
                for i in range(sampling_rate+1):
                    fixed_calculation() # Calculates values for the current parameters.
                    time += gradation # Sets the next parameter.
                return True
            else:
                return False
    else:
        return False

def dense_calculation():
    """ Solves the circuit with both capacitance values as variables. """
    global time, frequency, inductance, inductor_resistance, coupling_capacitance
    name_list = ["0", "time", "frequency", "inductance", "inductor_resistance", "capacitance"]
    unit_list = ["0", "s", "Hz", "H", "Ω", "F"]
    action_1 = int(input("Select the first variable:\n1) Time.\n2) Frequency.\n3) Inductance.\n4) Resistance.\n5) Capacitance.\n0) Quit to main menu.\n\n"))
    print("\n")
    if action_1 != 0:
        action_2 = int(input("Select the second variable:\n1) Time.\n2) Frequency.\n3) Inductance.\n4) Resistance.\n5) Capacitance.\n0) Quit to main menu.\n\n"))
        print("\n")
        if action_2 != 0:
            minimum_1 = float(input(f"Enter a minimum {name_list[action_1]} [{unit_list[action_1]}]:\t"))
            maximum_1 = float(input(f"Enter a maximum {name_list[action_1]} [{unit_list[action_1]}]:\t"))
            minimum_2 = float(input(f"Enter a minimum {name_list[action_2]} [{unit_list[action_2]}]:\t"))
            maximum_2 = float(input(f"Enter a maximum {name_list[action_2]} [{unit_list[action_2]}]:\t"))
            gradation_1 = (maximum_1 - minimum_1)/sampling_rate # Allows for a variable number of datapoints.
            gradation_2 = (maximum_2 - minimum_2)/sampling_rate # Allows for a variable number of datapoints.
            print(f"Sampling rate:\t\t\t{sampling_rate}\nGradation 1:\t\t{gradation_1}\nGradation 2:\t\t{gradation_2}\n")
            if action_1 == 1 and action_2 == 2:
                time = minimum_1
                frequency = minimum_2
                for i in range(sampling_rate+1): # Cycles through tuning parameters.
                    for i in range(sampling_rate+1): # Cycles through coupling parameters.
                        fixed_calculation() # Calculates values for the current parameters.
                        frequency += gradation_2 # Sets the next parameter.
                    frequency = minimum_2
                    time += gradation_1 # Sets the next parameter.
            elif action_1 == 1 and action_2 == 3:
                time = minimum_1
                inductance = minimum_2
                for i in range(sampling_rate+1): # Cycles through tuning parameters.
                    for i in range(sampling_rate+1): # Cycles through coupling parameters.
                        fixed_calculation() # Calculates values for the current parameters.
                        inductance += gradation_2 # Sets the next parameter.
                    inductance = minimum_2
                    time += gradation_1 # Sets the next parameter.
            elif action_1 == 1 and action_2 == 4:
                time = minimum_1
                inductor_resistance = minimum_2
                for i in range(sampling_rate+1): # Cycles through tuning parameters.
                    for i in range(sampling_rate+1): # Cycles through coupling parameters.
                        fixed_calculation() # Calculates values for the current parameters.
                        inductor_resistance += gradation_2 # Sets the next parameter.
                    inductor_resistance = minimum_2
                    time += gradation_1 # Sets the next parameter.
            elif action_1 == 1 and action_2 == 5:
                time = minimum_1
                coupling_capacitance = minimum_2
                for i in range(sampling_rate+1): # Cycles through tuning parameters.
                    for i in range(sampling_rate+1): # Cycles through coupling parameters.
                        fixed_calculation() # Calculates values for the current parameters.
                        coupling_capacitance += gradation_2 # Sets the next parameter.
                    coupling_capacitance = minimum_2
                    time += gradation_1 # Sets the next parameter.
            elif action_1 == 2 and action_2 == 3:
                frequency = minimum_1
                inductance = minimum_2
                for i in range(sampling_rate+1): # Cycles through tuning parameters.
                    for i in range(sampling_rate+1): # Cycles through coupling parameters.
                        fixed_calculation() # Calculates values for the current parameters.
                        inductance += gradation_2 # Sets the next parameter.
                    inductance = minimum_2
                    frequency += gradation_1 # Sets the next parameter.
            elif action_1 == 2 and action_2 == 4:
                frequency = minimum_1
                inductor_resistance = minimum_2
                for i in range(sampling_rate+1): # Cycles through tuning parameters.
                    for i in range(sampling_rate+1): # Cycles through coupling parameters.
                        fixed_calculation() # Calculates values for the current parameters.
                        inductor_resistance += gradation_2 # Sets the next parameter.
                    inductor_resistance = minimum_2
                    frequency += gradation_1 # Sets the next parameter.
            elif action_1 == 2 and action_2 == 5:
                frequency = minimum_1
                coupling_capacitance = minimum_2
                for i in range(sampling_rate+1): # Cycles through tuning parameters.
                    for i in range(sampling_rate+1): # Cycles through coupling parameters.
                        fixed_calculation() # Calculates values for the current parameters.
                        coupling_capacitance += gradation_2 # Sets the next parameter.
                    coupling_capacitance = minimum_2
                    frequency += gradation_1 # Sets the next parameter.
            elif action_1 == 3 and action_2 == 4:
                inductance = minimum_1
                inductor_resistance = minimum_2
                for i in range(sampling_rate+1): # Cycles through tuning parameters.
                    for i in range(sampling_rate+1): # Cycles through coupling parameters.
                        fixed_calculation() # Calculates values for the current parameters.
                        inductor_resistance += gradation_2 # Sets the next parameter.
                    inductor_resistance = minimum_2
                    inductance += gradation_1 # Sets the next parameter.
            elif action_1 == 3 and action_2 == 5:
                inductance = minimum_1
                coupling_capacitance = minimum_2
                for i in range(sampling_rate+1): # Cycles through tuning parameters.
                    for i in range(sampling_rate+1): # Cycles through coupling parameters.
                        fixed_calculation() # Calculates values for the current parameters.
                        coupling_capacitance += gradation_2 # Sets the next parameter.
                    coupling_capacitance = minimum_2
                    inductance += gradation_1 # Sets the next parameter.
            elif action_1 == 4 and action_2 == 5:
                coupling_capacitance = minimum_1
                inductor_resistance = minimum_2
                for i in range(sampling_rate+1): # Cycles through tuning parameters.
                    for i in range(sampling_rate+1): # Cycles through coupling parameters.
                        fixed_calculation() # Calculates values for the current parameters.
                        inductor_resistance += gradation_2 # Sets the next parameter.
                    inductor_resistance = minimum_2
                    coupling_capacitance += gradation_1 # Sets the next parameter.
            else:
                return False
        else:
            return False
    else:
        return False

def reset_variables():
    """ Reverts to the default values, rather than the last values calculated. Used in main(). """
    global frequency, inductance, coupling_capacitance
    if print_view == 1: print("reset_variables():\n")
    frequency, inductance, coupling_capacitance = frequency_set, inductance_set, coupling_capacitance_set

def reset_lists():
    """ Clears the data from the last calculation to prepare for the next. Used in main(). """
    global total_list, frequency_list, inductor_list, coupling_list
    if print_view == 1: print("reset_lists():\n")
    total_list.clear()
    time_list.clear()
    voltage_list.clear()
    frequency_list.clear()
    inductor_list.clear()
    coupling_list.clear()
    total_impedance = 0
    total_current = 0
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
            action_2 = int(input("Select calculation:\n1) Fixed calculation (no variables).\n2) Cluster calculation (one variable).\n3) Dense calculation (two variables).\n0) Quit to main menu.\n\n"))
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
