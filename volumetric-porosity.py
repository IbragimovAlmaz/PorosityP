import matplotlib.pyplot as plt

# Grouped porosity data
group_100 = [0.257, 0.0, -0.789]
group_95 = [1.184, 0.0, -0.348]
group_90 = [1.053, 0.970, 0.262]
group_85 = [5.513, 3.639, 5.308]
group_80 = [10.066, 8.335, 9.361]
group_75 = [20.118, 20.531, 18.517]
group_70 = [21.851, 27.551, 24.767]
group_65 = [32.175, 30.383, 32.027]
group_60 = [37.712, 37.568, 37.619]
group_55 = [44.257, 46.227, 46.416]

# Figure
plt.figure(figsize=(6, 5))
plt.boxplot([group_100, group_95, group_90, group_85, group_80, group_75, group_70, group_65, group_60, group_55], tick_labels=['PLA100', 'PLA95', 'PLA90', 'PLA85', 'PLA80', 'PLA75', 'PLA70', 'PLA65', 'PLA60', 'PLA55'])

# Titles
plt.title('Volumetric Porosimetry of PLA:PVP composites')
plt.ylabel('Porosity, %')
plt.xticks(rotation=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Arrow annotation
# The first arrow
plt.annotate(
    text='',                      # no text
    xy=(4.6, 12.0),               # endpoint
    xytext=(3.9, 14.8),           # startpoint
    arrowprops=dict(
        arrowstyle='-|>',         # style
        color='dimgrey',          # color
        lw=1                      # line width
    )
)
# The second arrow
plt.annotate(
    text='',
    xy=(5.7, 22.0),               # endpoint
    xytext=(5.0, 24.8),           # startpoint
    arrowprops=dict(
        arrowstyle='-|>',
        color='dimgrey',
        lw=1
    )
)

plt.savefig('volumetric_porosity.tiff', dpi=300, bbox_inches='tight', pad_inches=0.1)
plt.show()

