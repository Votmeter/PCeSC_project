import matplotlib.pyplot as plt
def save_plot(x, y, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.title('Sequenza di Coordinate')
    plt.xlabel('Longitudine')
    plt.ylabel('Latitudine')
    plt.grid(True)
    plt.savefig(f'DB_update/images/{filename}.png')
