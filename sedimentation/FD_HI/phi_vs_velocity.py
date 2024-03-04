import matplotlib.pyplot as plt

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

# Plot phi vs. Velocity_Z for both FD and HI data
plt.figure(figsize=(10, 6))
plt.plot(phi_values_FD, velocity_z_values_FD, marker='o', linestyle='-', label='FD')
plt.plot(phi_values_HI, velocity_z_values_HI, marker='o', linestyle='-', label='HI')
plt.title("Phi vs. Velocity_Z")
plt.xlabel("Phi")
plt.ylabel("Velocity_Z")
plt.grid(True)
plt.legend()
plt.show()
