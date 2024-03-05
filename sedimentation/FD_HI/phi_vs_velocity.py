import matplotlib.pyplot as plt
import numpy as np

# Initialize lists to store data from both files
phi_values_FD = []
velocity_z_values_FD = []
phi_values_HI = []
velocity_z_values_HI = []

# Read data from computational_velocity_FD.txt
with open("computational_velocity_FD.txt", "r") as infile_FD:
    next(infile_FD)  # Skip header
    for line in infile_FD:
        phi, velocity_x, velocity_y, velocity_z = line.strip().split("\t")
        phi_values_FD.append(float(phi))
        velocity_z_values_FD.append(float(velocity_z))

# Read data from computational_velocity_HI.txt
with open("computational_velocity_HI.txt", "r") as infile_HI:
    next(infile_HI)  # Skip header
    for line in infile_HI:
        phi, velocity_x, velocity_y, velocity_z = line.strip().split("\t")
        phi_values_HI.append(float(phi))
        velocity_z_values_HI.append(float(velocity_z))

# Define analytical function
def analytical_result(phi, m=5.40):
    return ((1 - phi) ** m) / (1 + (6.55 - m) * phi)

# Generate phi values for the analytical line
phi_analytical = np.linspace(0, 0.5, 100)
U_U0_analytical = analytical_result(phi_analytical)

# Plot phi vs. Velocity_Z for both FD and HI data
plt.figure(figsize=(10, 6))
plt.plot(phi_values_FD, velocity_z_values_FD, marker='o', linestyle='--', label='FD')
plt.plot(phi_values_HI, velocity_z_values_HI, marker='o', linestyle='--', label='HI')
plt.plot(phi_analytical, U_U0_analytical, color='red', label='Analytical')
plt.xlabel(r'$\phi$')
plt.ylabel("U/U$_0$")
plt.grid(True)
plt.legend()
plt.show()
