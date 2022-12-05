# Probe-Circuit-Simulation
Numerical simulation of a parallel LRC circuit with an additional capacitor for capacitive coupling. Variable parameters include capacitances, inductance, inductive resistance, input voltage, input impedance, and input frequency.

A differential equation may be constructed as follows to represent the change in electric charge over time of a series LRC circuit. \
\begin{centering}
$L\ddot{q}+R\dot{q}+C^{-1}q=\Lambda_\textrm{in}(\omega,t)$ \
\end{centering}
Here, $L$ is inductance, $q$ is electric charge, $R$ is resistance, $C$ is capacitance, $\Lambda$ is input voltage, and $\omega$ is angular frequency. An important quantity that may be extracted from this relation is impedance: \
$Z(\omega,t)=\frac{\Lambda_{\textrm{in}}(\omega,t)}{\dot{q}}$. \
In many common texts, the following three equations are assumed for inductors, resistors, and capacitors, respectively:
$Z_L = i\omega L$ \
$Z_R = R$ \
$Z_C =\frac{-i}{\omega C}$. \
