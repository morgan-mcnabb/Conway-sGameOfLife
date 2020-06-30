import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse


def AddGosperGun(grid, size):
    grid[1, 25] = 255
    grid[2, 23] = 255
    grid[2, 25] = 255
    grid[3, 13] = 255
    grid[3, 14] = 255
    grid[3, 21] = 255
    grid[3, 22] = 255
    grid[3, 35] = 255
    grid[3, 36] = 255
    grid[4, 12] = 255
    grid[4, 16] = 255
    grid[4, 21] = 255
    grid[4, 22] = 255
    grid[4, 35] = 255
    grid[4, 36] = 255
    grid[5, 1] = 255
    grid[5, 2] = 255
    grid[5, 11] = 255
    grid[5, 17] = 255
    grid[5, 21] = 255
    grid[5, 22] = 255
    grid[6, 1] = 255
    grid[6, 2] = 255
    grid[6, 11] = 255
    grid[6, 15] = 255
    grid[6, 17] = 255
    grid[6, 18] = 255
    grid[6, 23] = 255
    grid[6, 25] = 255
    grid[7, 11] = 255
    grid[7, 17] = 255
    grid[7, 25] = 255
    grid[8, 12] = 255
    grid[8, 16] = 255
    grid[9, 13] = 255
    grid[9, 14] = 255


# for adding predetermined pattern to the grid
def addGlider(i, j, grid):
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider


# randomizes the grid if glider isn't used
def randomizeGrid(size):
    return np.random.choice([0, 255], size * size, p =[0.25, 0.75]).reshape(size, size)


# updated the grid each frame
def update(frameNum, img, grid, N):
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = int((grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                         grid[(i - 1) % N, j] + grid[(i + 1) % N, j] +
                         grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N] +
                         grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / 255)

            if grid[i, j] == 255:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = 0
            else:
                if total == 3:
                    newGrid[i, j] = 255

    # visually updates the data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,


def main():
    # arguments for command line execution
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movFile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)

    args = parser.parse_args()

    # set the grid size
    if args.N and int(args.N) > 8:
        N = int(args.N)
    else:
        N = 100

    # set the animation update interval
    if args.interval:
        interval = int(args.interval)
    else:
        interval = 50

    # check if the glider flag is specified
    if args.glider and not args.gosper:
        grid = np.zeros(N * N).reshape(N, N)
        addGlider(1, 1, grid)
    elif args.gosper and not args.glider:
        grid = np.zeros(N * N).reshape(N, N)
        AddGosperGun(grid, N)
    else:
        grid = randomizeGrid(N)

    # set up the animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames=10,
                                  interval=interval,
                                  save_count=50)

    # set the output file
    if args.movFile:
        ani.save(args.movFile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


if __name__ == '__main__':
    main()
