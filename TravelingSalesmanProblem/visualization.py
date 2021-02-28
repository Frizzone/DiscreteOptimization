
import matplotlib.pyplot as plt
__PLOT = True

def plot(solution, points, nodeCount):
    x = []
    y = []
    for index in range(nodeCount):
        x.append(points[solution[index]].x)
        y.append(points[solution[index]].y)
        plt.plot(x, y, 'xb-')
    plt.show()