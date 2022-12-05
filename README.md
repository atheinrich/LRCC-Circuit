# Probe-Circuit-Simulation
Numerical simulation of a parallel LRC circuit with an additional capacitor for capacitive coupling. Variable parameters include capacitances, inductance, inductive resistance, input voltage, input impedance, and input frequency.

The primary purpose of these programs are for the construction of probe circuits for magnetic resonance experiments, such as spin exchange optical pumping. These circuits collect and transmit alternating current signals at a desired frequency. This frequency depends on the values of the inductors, resistors, and capacitors used. Furthermore, its implementation in an extended signal flow requires adequate impedance matching to promote signal quality. Each program allows these factors to be adjusted numerically and monitored as a function of up to two simultaneous variables. The probe circuit itself is given by the Probe LRCC script, while the Series and Parallel LRC scripts are prototypical derivatives of the probe circuit that have interesting properties themselves.

Steps to maximize power across the inductive coil:
1. Determine the inductance, resistance, input voltage, input impedance, and desired frequency of the experimental setup.
2. Vary the tuning capacitance to a point at which the total resistance equals the input resistance. It may take some trial-and-error to find the right interval.
3. Update the tuning capacitance to the value that corresponds to the input resistance from the last step.
4. Vary the coupling (matching) capacitance to a point at which the total reactance equals the input reactance.
5. Update the coupling capacitance to the respective value, then verify the circuit's behavior by varying the frequency over the range of interest.

An additional interest in this toolset is the comparison of real and complex analysis in terms of impedance calculations and Ohmic equations. For a series LRC circuit, the following differential equation may be constructed to represent the total change in electric charge over time: \
  $L\ddot{q}+R\dot{q}+C^{-1}q=\Lambda_\textrm{in}(\omega,t)$. \
Here, $L$ is inductance, $q$ is electric charge, $R$ is resistance, $C$ is capacitance, $\Lambda$ is input voltage, and $\omega$ is angular frequency. An important quantity that may be extracted from this relation is impedance: \
  $Z(\omega,t)=\frac{\Lambda_{\textrm{in}}(\omega,t)}{\dot{q}}$. \
In many common texts, the following three equations are assumed for inductors, resistors, and capacitors, respectively: \
  $Z_L = i\omega L$ \
  $Z_R = R$ \
  $Z_C =\frac{-i}{\omega C}$. \
These are derived from the given differential equation by setting all other parameters (L, R, or C) to zero and assuming an input voltage in the form of a complex exponential: \
  $\Lambda_{\textrm{in}}(\omega,t)=\Lambda_0 e^{i\omega t}$.
Alternatively, a real-valued choice of input voltage yields quite different results. This is explored as a side project in the script(s) marked with "(Real)."
