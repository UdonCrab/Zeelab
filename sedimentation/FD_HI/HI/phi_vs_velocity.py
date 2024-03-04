import matplotlib.pyplot as plt

# Read data from computational_velocity.txt
phi_values = []
average_velocities = []
with open("computational_velocity_HI.txt", "r") as infile:
    next(infile)  # Skip header
    for line in infile:
        phi, velocity = line.strip().split("\t")
        phi_values.append(float(phi))
        average_velocities.append(float(velocity))

# Plot phi vs. average velocity
plt.figure(figsize=(10, 6))
plt.plot(phi_values, average_velocities, marker='o', linestyle='-')
plt.title("Phi vs. Average Velocity")
plt.xlabel("Phi")
plt.ylabel("Average Velocity")
plt.grid(True)
plt.show()
