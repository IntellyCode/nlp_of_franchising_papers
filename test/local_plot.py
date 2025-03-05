import numpy as np
import matplotlib.pyplot as plt


def main():
    # Load the saved data
    data = np.load('./output/plot_data.npz')
    X = data['X']
    Y = data['Y']
    Z = data['Z']

    # Create an interactive 3D plot.
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
    ax.set_xlabel('no_below (integer)')
    ax.set_ylabel('no_above (float)')
    ax.set_zlabel('Unique Tokens')
    ax.set_title('Dictionary Unique Tokens vs. Filter Extremes Parameters')
    fig.colorbar(surf, shrink=0.5, aspect=5)

    # This will open an interactive window on your local device.
    plt.show()


if __name__ == '__main__':
    main()
