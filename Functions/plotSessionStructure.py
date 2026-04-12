#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 11:48:26 2022

@author: Lowri Powell & Mark Humphries
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np


def plotSessionStructure(TestData, block_labels=None):
    ax = plt.gca()
    no_trials = len(TestData)
    if no_trials == 0:
        return

    if 'NewSessionTrials' in TestData.columns:
        session_lines = TestData.index[TestData['NewSessionTrials'] == 1].to_numpy()
        if session_lines.size:
            ax.vlines(
                session_lines,
                0,
                1,
                colors='lightgray',
                linestyles='--',
                linewidth=0.75,
                label="New Sessions",
            )

    rule_lines = np.array([0], dtype=float)
    if 'RuleChangeTrials' in TestData.columns:
        detected_rule_lines = TestData.index[TestData['RuleChangeTrials'] == 1].to_numpy()
        if detected_rule_lines.size:
            rule_lines = np.insert(detected_rule_lines.astype(float), 0, 0.0)

    block_edges = np.append(rule_lines, float(no_trials))

    if block_labels is None:
        block_labels = ["Right Arm", "Lit Arm", "Left Arm", "Unlit Arm"]

    # Band position in axes fraction (above the axes)
    band_ymin = 1.02
    band_ymax = 1.12

    for idx, start in enumerate(block_edges[:-1]):
        end = block_edges[idx + 1]
        xmin = start / no_trials
        xmax = end / no_trials

        # Draw shaded block using transAxes (fully in axes fraction)
        rect = mpatches.FancyBboxPatch(
            (xmin, band_ymin),
            xmax - xmin,
            band_ymax - band_ymin,
            boxstyle="square,pad=0",
            transform=ax.transAxes,
            facecolor='lightgray',
            edgecolor='k',
            alpha=0.35,
            linewidth=0.8,
            clip_on=False
        )
        ax.add_patch(rect)

        # Vertical divider line
        line = Line2D(
            [xmin, xmin], [band_ymin, band_ymax],
            transform=ax.transAxes,
            color='k',
            linewidth=0.8,
            clip_on=False
        )
        ax.add_line(line)

        # Block label text
        if idx < len(block_labels):
            midpoint = (xmin + xmax) / 2
            ax.text(
                midpoint,
                (band_ymin + band_ymax) / 2,
                block_labels[idx],
                ha='center',
                va='center',
                transform=ax.transAxes,
                fontsize=9,
                clip_on=False,
            )

    
