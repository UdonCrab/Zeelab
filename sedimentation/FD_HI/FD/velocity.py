import numpy as np
import os

def unwrap_trajectory(particle_positions, box_sizes):
    # Compute displacement between frames
    delta_x = np.diff(particle_positions, axis=0)
    
    # Get nearest image displacement
    delta_x -= np.fix(2 * delta_x / box_sizes) * box_sizes
    
    # Take cumulative sum of displacements
    unwrapped_positions = np.cumsum(delta_x, axis=0)
    
    return unwrapped_positions

def compute_mean_displacement(unwrapped_positions):
    # Average trajectories over all particles
    mean_displacement = np.mean(unwrapped_positions, axis=1)
    
    return mean_displacement

def compute_velocity(mean_displacement, time_interval):
    # Fit a straight line to the displacement to compute velocity
    velocity = np.polyfit(np.arange(len(mean_displacement)), mean_displacement, 1)[0]
    
    # Convert displacement to velocity (assuming time_interval is 1)
    velocity /= time_interval
    
    return velocity

if __name__ == "__main__":
    directory = "."  # Directory containing the data files
    time_interval = 1  # Example time interval
    
    results = []  # List to store results
    
    for filename in os.listdir(directory):
        if filename.startswith("sed_N8000_phi") and filename.endswith("_FD.txt"):
            print(f"Processing file: {filename}")  # Print filename before loading data
            
            # Extract phi from filename
            phi = float(filename.split("_")[2].replace("phi", ""))
            
            # Initialize arrays to store particle positions for each frame
            particle_positions = []
            N = None
            box_sizes = None
            
            # Open and read the file
            with open(os.path.join(directory, filename), 'r') as file:
                # Read the file line by line
                frame_positions = []
                row_count = 0
                for line in file:
                    if row_count % 8003 == 0:
                        N = int(line)
                    elif row_count % 8003 == 1:
                        box_sizes = np.array([float(x) for x in line.split()])
                    elif line.strip():
                        frame_positions.append([float(x) for x in line.split()])
                    else:
                        # Process the completed frame
                        particle_positions.append(np.array(frame_positions))
                        frame_positions = []
                    row_count += 1
            
            # Convert particle positions to numpy array
            particle_positions = np.array(particle_positions)
            
            # Initialize arrays to store mean displacements and velocities for each frame
            mean_displacements = []
            velocities = []
            
            # Loop through frames
            for frame_positions in particle_positions:  # Loop through frames
                # Unwrap trajectory for the frame
                unwrapped_positions = unwrap_trajectory(particle_positions, box_sizes)
                
                # Compute mean displacement for the frame
                mean_displacement = compute_mean_displacement(unwrapped_positions)
                
                # Compute velocity for the frame
                velocity = compute_velocity(mean_displacement, time_interval)
                
                # Append mean displacement and velocity to lists
                mean_displacements.append(mean_displacement)
                velocities.append(velocity)
            
            # Compute overall average velocity for all frames
            average_velocity = np.mean(velocities)
            
            # Store phi and average velocity in results
            results.append((phi, average_velocity))
            
            print(f"For phi={phi}: Average velocity = {average_velocity}")
    
    # Sort results based on phi values
    results.sort(key=lambda x: x[0])
    
    # Write results to a text file
    with open("computational_velocity_FD.txt", "w") as outfile:
        outfile.write("Phi\tAverage Velocity\n")
        for result in results:
            outfile.write(f"{result[0]}\t{result[1]}\n")
    
    print("Results saved to computational_velocity_FD.txt")
