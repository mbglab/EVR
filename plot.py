#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
This is a simple script for chromosome structure visualization using Matplotlib and structure alignment with Kabsch algorithm.

A visualization example: python plot.py a.pdb --show

An example of comparison between the two structures: python plot.py a.pdb:b.pdb --withRMSD --show

usage: plot.py [-h] [-o O] [-lw LINEWIDTH] [-c COLOR] [--withpoints]
               [-ps POINTSIZE] [-ws] [--withRMSD] [--show]
               i

positional arguments:
  i                     The PDB file(s). If you have more than one file,
                        please split them with ':'.

optional arguments:
  -h, --help            Show this help message and exit.
  -o O                  Output picture file name.
  -lw LINEWIDTH, --linewidth LINEWIDTH
                        Line(s) width. If you enter more than one PDB file,
                        you can enter 2 or more width values; use ':' to
                        split them.
  -c COLOR, --color COLOR
                        Drawing color(s). If you enter more than one PDB file,
                        you can enter 2 or more colors; use ':' to 
						split them.
  --withpoints          Whether to draw points.
  -ps POINTSIZE, --pointsize POINTSIZE
                        If you want to draw points, please choose points size.
  -ws, --withsuperposition
                        Whether to superpose these structures.
  --withRMSD            Whether to print RMSD values in console.
  --show                Whether to plot these structures on computer screen.
'''
import argparse
import random

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from IO import ReadPDB

COLORS = ["blue", "brown", "green", "yellow", "red"]

def CalRotateM(S1, S2):
    A = np.dot(S1.coordinate.T, S2.coordinate)
    u, s, v = np.linalg.svd(A)
    d = np.linalg.det(u) * np.linalg.det(v)

    if d < 0:
        u[:, -1] *= -1

    r_m = np.dot(u, v)
    return r_m

def rmsd(S1, S2):
    S1_p = S1.coordinate
    S2_p = S2.coordinate

    d = S1_p.shape[1]
    n = S2_p.shape[0]
    s = 0.0

    for v, w in zip(S1_p, S2_p):
        s += np.sum((v - w)**2.0)

    rmsd = np.sqrt(s / n)
    return rmsd

class Structure:
    is_setline = False
    is_setpoint = False

    def __init__(self, filename = None, ax = None):
        if filename:
            self.AddStructureFromFile(filename)
        else:
            pass

        if ax:
            self.ax = ax
        else:
            pass

    def AddStructureFromFile(self, filename):
        x, y, z, c = ReadPDB(filename)

        self.coordinate = np.array([[x[i], y[i], z[i]] for i in range(len(x))])

        self.c = []

        start = c.keys()[0]
        self.c.append(start)
        now = start
        while True:
            if now not in c:
                break

            ne_t = c[now]
            self.c.append(ne_t)

            if ne_t == start:
                break
            now = ne_t
        self.Center2O()

    def Center2O(self):
        cent_p = self.GetCenter()
        self.Translation(cent_p)

    def GetCenter(self):
        cent_position = self.coordinate.mean(axis = 0)

        return cent_position

    def Translation(self, pos):
        self.coordinate -= pos

    def Rotate(self, m):
        self.coordinate = np.dot(self.coordinate, m)

    def DrawLine(self):
        if not self.is_setline:
            self.SetLineArgs()
        self.ax.plot(self.coordinate[:, 0][self.c], self.coordinate[:, 1][self.c], self.coordinate[:, 2][self.c], color = self.line_color, linewidth = self.line_size)

    def DrawPoints(self):
        if not self.is_setpoint:
            self.SetPointArgs()
        self.ax.scatter(self.coordinate[:, 0], self.coordinate[:, 1], self.coordinate[:, 2], c = self.point_color, s = self.point_size, depthshade = True)

    def SetLineArgs(self, color = None, size = None):
        if color:
            self.line_color = color

        elif self.is_setpoint:
            self.line_color = self.point_color

        else:
            self.line_color = random.choice(COLORS)
            COLORS.remove(self.line_color)

        if size:
            self.line_size = size
        else:
            self.line_size = 1

        self.is_setline = True

    def SetPointArgs(self, color = None, size = None):
        if color:
            self.point_color = color

        elif self.is_setline:
            self.point_color = self.line_color

        else:
            self.point_color = random.choice(COLORS)
            COLORS.remove(self.point_color)

        if size:
            self.point_size = size
        else:
            self.point_size = 10

        self.is_setpoint = True

    def SetDrawArgs(self, color = None, l_size = None, p_size = None):
        self.SetLineArgs(color, l_size)
        self.SetPointArgs(color, p_size)

    def Draw(self, line = True, point = True):
        if line:
            self.DrawLine()
        if point:
            self.DrawPoints()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("i", help="The PDB file(s). If you have more than one file, please split them with ':'.")
    parser.add_argument("-o", help = "Output picture file name.")

    parser.add_argument("-lw", "--linewidth", help = "Line(s) width. If you enter more than one PDB file, you can enter 2 or more width values; use ':' to split them.", default = "1.0")
    parser.add_argument("-c", "--color", help = "Drawing color(s). If you enter more than one PDB file, you can enter 2 or more colors; use ':' to split them.", default = "Red:Blue")

    parser.add_argument("--withpoints", help = "Whether to draw points.", action = "store_true")
    parser.add_argument("-ps", "--pointsize", help = "If you want to draw points, please choose points size.", type = float, default = 10)
    parser.add_argument("-ws", "--withsuperposition", help = "Whether to superpose these structures.", action='store_true')
    parser.add_argument("--withRMSD", help = "Whether to print RMSD values in console.", action='store_true')


    parser.add_argument("--show", help = "Whether to plot these structures on computer Screen.", action = "store_true")

    args = parser.parse_args()

    pdb_file = args.i
    lw = args.linewidth
    color = args.color

    with_point = args.withpoints
    point_size = args.pointsize

    sp = args.withsuperposition
    with_rmsd = args.withRMSD

    output_file = args.o
    is_show = args.show

    figure = plt.figure()
    #ax = figure.gca(projection = "3d")
    ax = Axes3D(figure)

    if ":" in pdb_file:
        pdbs = pdb_file.split(":")
    else:
        pdbs = [pdb_file]
    if ":" in lw:
        line_widths = lw.split(":")
    else:
        line_widths = [lw]
    if ":" in color:
        colors = color.split(":")
    else:
        colors = [color]

    if len(line_widths) < len(pdbs):
        diff = len(pdbs) - len(line_widths)
        for i in range(diff):
            line_widths.append(line_widths[-1])
    if len(colors) < len(pdbs):
        diff = len(pdbs) - len(colors)
        for i in range(diff):
            colors.append(colors[-1])

    structures = []
    for pdb in pdbs:
        structures.append(Structure(pdb, ax))

    n_pdb = len(pdbs)

    for i in range(n_pdb):
        color = colors[i]
        l_size = line_widths[i]
        p_size = point_size

        structures[i].SetDrawArgs(color = color, l_size = l_size, p_size = p_size)

    if sp:
        s1 = structures[0]
        for i in range(1, n_pdb):
            r_m = CalRotateM(structures[i], s1)
            structures[i].Rotate(r_m)

    if with_rmsd:
        print("Structure1\tStructure2\tRMSD value")
        for i in range(n_pdb):
            for j in range(i + 1, n_pdb):
                rmsd_value = rmsd(structures[i], structures[j])
                print("%s\t%s\t%f" % (pdbs[i], pdbs[j], rmsd_value))

    for i in range(n_pdb):
        structures[i].Draw(True, False)
    plt.axis('off')
    if output_file:
        plt.savefig(output_file)

    if is_show:
        plt.show()
