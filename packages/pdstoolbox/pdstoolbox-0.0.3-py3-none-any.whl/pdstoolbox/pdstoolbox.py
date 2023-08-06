# PDS(Personalized Data-Studio) Data Mining Toolbox

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
    plt.scatter(xpos, ypos, s=hist * bubblesize, alpha=0.3, color='white', linewidth=1, edgecolor='black')
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

    ax.scatter(xpos, ypos, s=hist * bubblesize, alpha=0.4,edgecolor='black')
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

# scatter plot+boxplot
def scatterbox(df, parameter_x, parameter_y, title):
    import matplotlib.pyplot as plt

    df = df
    x = df[parameter_x]
    y = df[parameter_y]
    title = title

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.08]
    rect_histy = [left + width + spacing, bottom, 0.08, height]

    # start with a rectangular Figure
    plt.figure(figsize=(8, 8))

    # scatter plot
    ax_scatter = plt.axes(rect_scatter)
    plt.grid(linestyle='--', lw=0.5)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    plt.xlabel(parameter_x)
    plt.ylabel(parameter_y)

    # top hist
    ax_histx = plt.axes(rect_histx)
    plt.grid(linestyle='--', lw=0.5, axis='y')
    ax_histx.tick_params(direction='in', labelbottom=False)
    plt.xlabel(parameter_x)
    #     plt.ylabel('Counts')
    plt.title(title)

    # right hist
    ax_histy = plt.axes(rect_histy)
    plt.grid(linestyle='--', lw=0.5, axis='x')
    ax_histy.tick_params(direction='in', labelleft=False)
    #     plt.xlabel('Counts')
    plt.ylabel(parameter_y)

    # the scatter plot:
    ax_scatter.scatter(x, y, s=600, edgecolor='black', lw=1, alpha=0.8, facecolor='darkorange')

    # now determine nice limits by hand:
    #     ax_histx.hist(x, bins=bins,edgecolor='black',facecolor='darkorange',alpha=0.7)
    #     ax_histy.hist(y, bins=bins, orientation='horizontal',edgecolor='black',facecolor='darkorange',alpha=0.7)

    red_square = dict(markerfacecolor='lightgrey', marker='o', alpha=0.5, lw=1)

    x = ax_histx.boxplot(x, flierprops=red_square, vert=False, widths=0.5, patch_artist=True)
    for patch in x['boxes']:
        patch.set_facecolor('orange')

    y = ax_histy.boxplot(y, flierprops=red_square, widths=0.5, patch_artist=True)
    for patch in y['boxes']:
        patch.set_facecolor('orange')

    #     ax_histx.set_xlim(ax_scatter.get_xlim())
    #     ax_histy.set_ylim(ax_scatter.get_ylim())

    plt.show()

# heatmap: multi-correlation plot
def heatmap(df, title):
    import seaborn as sns
    import numpy as np
    import matplotlib.pyplot as plt

    df = df

    plt.figure(figsize=(12, 8))
    sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns, linewidth=1, linecolor='white',
                cmap='Blues', center=0, annot=True)
    plt.title(title)
    plt.xticks(rotation=30)
    plt.yticks(rotation=30)
    plt.show()




# test|demos
import pandas as pd
# df=pd.read_csv('C:/Users/lx379/Desktop/ssappoc/bsfctest.csv')
# dutycycle(df, 'EngSpd', 'EngTrq', 150, 150, 1400, 'Duty Cycle.[pdstoolbox demo]')
# df=pd.read_csv('C:/Users/lx379/Desktop/ssappoc/test001.csv')
