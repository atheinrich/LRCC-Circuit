# Probe-Circuit-Simulation
Numerical simulation of a parallel LRC circuit with an additional capacitor for capacitive coupling. Variable parameters include capacitances, inductance, inductive resistance, input voltage, input impedance, and input frequency.

A differential equation may be constructed as follows to represent the change in electric charge over time of a series LRC circuit. \
$L\ddot{q}+R\dot{q}+C^{-1}q=\Lambda_\textrm{in}(\omega,t)$ \
Here, $L$ is inductance, $q$ is electric charge, $R$ is resistance, $C$ is capacitance, $\Lambda$ is input voltage, and $\omega$ is angular frequency. An important quantity that may be extracted from this relation is impedance ($Z$). \
$Z(\omega,t)/equiv \frac{\Lambda(\omega,t)}{\dot{q}}$ \
