import os
import numpy as np
from scipy.stats import linregress

def load_data(directory):
    data = {}
    for file_name in os.listdir(directory):
        if file_name.startswith('sed_N8000_phi') and file_name.endswith('.txt'):
            phi = float(file_name.split('_')[2][3:])  # Extract phi value from file name
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r') as file:
                frames = []
                frame_data = {'particle_positions': [], 'box_length': None}
                line_num = 1
                for line in file:
                    line_data = line.strip().split()
                    if line_num % 8003 == 1:  # Total number of particles
                        frame_data['particle_count'] = int(line_data[0])
                    elif line_num % 8003 == 2:  # Box length
                        frame_data['box_length'] = list(map(float, line_data))
                    else:  # Particle position
                        frame_data['particle_positions'].append(list(map(float, line_data)))
                    line_num += 1
                    if line_num % 8003 == 0:  # End of frame
                        frames.append(frame_data)
                        frame_data = {'particle_positions': [], 'box_length': None}
                data[phi] = frames
    return data

def compute_displacement(data):
    for phi, frames in data.items():
        print(f"Processing data for phi = {phi}:")
        for i in range(1, len(frames)):
            current_frame = frames[i]
            next_frame = frames[i + 1]
            print(f"Processing frames {i} and {i + 1}:")
            print(f"Current frame particle positions: {current_frame['particle_positions']}")
            print(f"Next frame particle positions: {next_frame['particle_positions']}")
            try:
                displacement = np.array(next_frame['particle_positions']) - np.array(current_frame['particle_positions'])
                print(f"Displacement shape: {displacement.shape}")
            except ValueError as e:
                print(f"Error computing displacement: {e}")


def adjust_displacement(data):
    for phi, frames in data.items():
        for frame in frames:
            box_length = np.array(frame['box_length'])
            for i in range(len(frame['displacement'])):
                displacement = frame['displacement'][i]
                adjusted_displacement = displacement - box_length * np.fix(2 * displacement / box_length)
                frame['displacement'][i] = adjusted_displacement

def cumulative_sum(data):
    for phi, frames in data.items():
        for frame in frames:
            frame['cumulative_displacement'] = np.cumsum(frame['displacement'], axis=0)

def average_displacement(data):
    for phi, frames in data.items():
        total_displacement = np.sum([frame['cumulative_displacement'] for frame in frames], axis=0)
        average_displacement = total_displacement / len(frames)
        data[phi]['average_displacement'] = average_displacement

def fit_straight_line(data):
    for phi, frames in data.items():
        velocities = {'x': [], 'y': [], 'z': []}
        for frame in frames:
            for direction in range(3):
                slope, intercept, _, _, _ = linregress(np.arange(len(frame['cumulative_displacement'][:, direction])), frame['cumulative_displacement'][:, direction])
                velocities['xyz'[direction]].append(slope)
        data[phi]['velocities'] = velocities

def print_results(data):
    for phi, result in data.items():
        print(f"Phi: {phi}")
        for direction, velocity in result['velocities'].items():
            print(f"Velocity in {direction}-direction: {np.mean(velocity)}")

# Main script
directory_path = "."
data = load_data(directory_path)
compute_displacement(data)
adjust_displacement(data)
cumulative_sum(data)
average_displacement(data)
fit_straight_line(data)
print_results(data)
