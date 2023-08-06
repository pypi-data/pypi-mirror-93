# PDS(Personalized Data-Studio) Data Mining Toolbox
# import pandas as pd

def test():
    print('Welcome to PDS data mining toolbox!')

# bsfcmap+dutycycle
def bsfcmap_dutycycle(df, speed_name, torque_name, bsfc_name, stepx, stepy, bubblesize, title, level):
    from scipy.interpolate import griddata
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    df = df
    x = np.array(df[speed_name])
    y = np.array(df[torque_name])
    z = np.array(df[bsfc_name])
    level = level
    title = title

    xi = np.linspace(min(x), max(x), 1000)
    yi = np.linspace(min(y), max(y), 1000)
    X, Y = np.meshgrid(xi, yi)
    Z = griddata((x, y), z, (X, Y), method='cubic')

    # duty cycle inputs:
    x1 = int((min(x) - 200) / 100) * 100
    x2 = int((max(x) + 200) / 100) * 100
    y1 = int((min(y) - 200) / 100) * 100
    y2 = int((max(y) + 200) / 100) * 100

    xedges = [*range(x1, x2, stepx)]
    yedges = [*range(y1, y2, stepy)]

    hist_temp, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))
    hist = hist_temp.T
    xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1])
    xpos = xpos.ravel()
    ypos = ypos.ravel()

    # Visualization(duty cycle+fuel map) method: nearest / linear / cubic
    # (fuel map)
    plt.figure(figsize=(12, 8))
    C = plt.contour(X, Y, Z, level, colors='black', alpha=0.5)
    plt.contourf(X, Y, Z, level, alpha=.75, cmap='plasma')
    plt.colorbar()
    plt.clabel(C, inline=True, fontsize=10, colors='black')
    plt.xlabel(speed_name)
    plt.ylabel(torque_name)
    plt.title(title)

    # (duty cycle)
    plt.grid(which='both', color='grey', linestyle='--', alpha=0.6)
    plt.scatter(xpos, ypos, s=hist * bubblesize, alpha=0.3, color='white', linewidth=1.5, edgecolor='black')
    plt.show()

# duty cycle
def dutycycle(df, speed_name, torque_name, stepx, stepy, bubblesize, title):
    from scipy.interpolate import griddata
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    df = df
    x = df[speed_name]
    y = df[torque_name]

    x1 = int((min(x) - 200) / 100) * 100
    x2 = int((max(x) + 200) / 100) * 100
    y1 = int((min(y) - 200) / 100) * 100
    y2 = int((max(y) + 200) / 100) * 100

    xedges = [*range(x1, x2, stepx)]
    yedges = [*range(y1, y2, stepy)]

    hist_temp, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))
    hist = hist_temp.T
    xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1])
    xpos = xpos.ravel()
    ypos = ypos.ravel()

    fig, ax = plt.subplots(figsize=(14, 8))

    ax.set_xticks(xedges, minor=False)
    ax.set_yticks(yedges, minor=False)

    ax.grid(which='both', color='grey', linestyle='--', alpha=0.6)

    ax.scatter(xpos, ypos, s=hist * bubblesize, alpha=0.5)
    ax.set_xlabel(speed_name)
    ax.set_ylabel(torque_name)
    ax.set_title(title)
    plt.show()

# bsfcmap
def bsfcmap(df, speed_name, torque_name, bsfc_name, title, level):
    from scipy.interpolate import griddata
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np

    df = df
    x = np.array(df[speed_name])
    y = np.array(df[torque_name])
    z = np.array(df[bsfc_name])
    level = level
    title = title

    xi = np.linspace(min(x), max(x), 1000)
    yi = np.linspace(min(y), max(y), 1000)
    X, Y = np.meshgrid(xi, yi)
    Z = griddata((x, y), z, (X, Y), method='cubic')

    # method: nearest / linear / cubic
    plt.figure(figsize=(12, 8))
    C = plt.contour(X, Y, Z, level, colors='black', alpha=0.5)
    plt.contourf(X, Y, Z, level, alpha=.75, cmap='plasma')
    plt.colorbar()
    plt.clabel(C, inline=True, fontsize=10, colors='black')
    plt.xlabel(speed_name)
    plt.ylabel(torque_name)
    plt.title(title)
    plt.show()






# test
import pandas as pd
df=pd.read_csv('C:/Users/lx379/Desktop/ssappoc/pdstoolbox/0128_test.csv')
# df=pd.read_csv('C:/Users/lx379/Desktop/ssappoc/bsfctest.csv')
# bsfcmap(df,'EngSpd','EngTrq','BSFC','BSFC Map Demo.[pdstoolbox]',[180,190,200,210,220,230,240,250])
bsfcmap_dutycycle(df, 'speed', 'torque', 'bsfc', 150, 150, 2400, 'BSFC Map+Duty Cycle Demo.[pdstoolbox]',
                  [160, 170, 180, 190, 200, 210, 220])