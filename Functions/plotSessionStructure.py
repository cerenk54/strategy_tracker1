#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 11:48:26 2022

@author: Lowri Powell & Mark Humphries
"""
import matplotlib.pyplot as plt
import numpy as np


def plotSessionStructure(TestData):
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
    block_labels = ["Right Arm", "Lit Arm", "Left Arm", "Unlit Arm"]

    # Draw the rule band in axes coordinates so it doesn't distort the data scale.
    for idx, start in enumerate(block_edges[:-1]):
        end = block_edges[idx + 1]
        xmin = start / no_trials
        xmax = end / no_trials
        ax.axhspan(
            1.02,
            1.12,
            xmin=xmin,
            xmax=xmax,
            alpha=0.25,
            edgecolor='k',
            facecolor='lightgray',
            transform=ax.get_xaxis_transform(),
            clip_on=False,
        )
        ax.axvline(start, ymin=1.02, ymax=1.12, color='k', linewidth=0.8, clip_on=False)

        if idx < len(block_labels):
            midpoint = (start + end) / 2
            ax.text(
                midpoint,
                1.07,
                block_labels[idx],
                ha='center',
                va='center',
                transform=ax.get_xaxis_transform(),
                clip_on=False,
            )

    ax.text(
        no_trials / 2,
        1.16,
        "Rule for Reward",
        ha='center',
        va='bottom',
        transform=ax.get_xaxis_transform(),
        clip_on=False,
    )
