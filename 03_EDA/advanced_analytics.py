"""
=========================================================
Advanced Analytics
=========================================================
"""

import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import networkx as nx

from wordcloud import WordCloud

OUTPUT_FOLDER = "reports/EDA_Charts/Advanced"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


def save_horizontal_bar_chart(
    data,
    title,
    xlabel,
    filename,
    color="steelblue"
):

    if len(data) == 0:
        return

    data = data.sort_values()

    plt.figure(figsize=(14,8))

    ax = data.plot.barh(
        color=color
    )

    for container in ax.containers:

        ax.bar_label(
            container,
            fontsize=9
        )

    plt.title(
        title,
        fontsize=18,
        weight="bold"
    )

    plt.xlabel(
        xlabel,
        fontsize=13
    )

    plt.grid(
        axis="x",
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(

        os.path.join(
            OUTPUT_FOLDER,
            filename
        ),

        dpi=300,

        facecolor="white",

        bbox_inches="tight"

    )

    plt.close()


def generate_advanced_analytics():

    print("="*60)
    print("Generating Advanced Analytics")
    print("="*60)

    # -----------------------------------------
    # Skill Frequency
    # -----------------------------------------

    frequency = pd.read_csv(
        "data/processed/skill_frequency.csv"
    )

    top_skills = (

        frequency

        .sort_values(
            "frequency",
            ascending=False
        )

        .head(20)

        .set_index("skill")["frequency"]

    )

    save_horizontal_bar_chart(

        top_skills,

        "Top 20 Skill Frequency",

        "Frequency",

        "22_Skill_Frequency.png",

        "royalblue"

    )

    print("✓ Skill Frequency Created")

    # -----------------------------------------
    # Skill Co-occurrence
    #
    # `skill_pairs.csv` is read once here (`pairs_raw`) and reused by
    # the co-occurrence chart, the heatmap, and the network graph
    # below -- each section builds its own filtered copy
    # (`cooccurrence_pairs`, `heatmap_pairs`, `network_pairs`) instead
    # of re-reading the file or reassigning a shared `pairs` variable
    # across sections. Reusing one name for different shapes of data
    # in sequence is exactly the kind of shadowing bug that broke
    # skills_analytics.py earlier -- naming each view distinctly here
    # avoids repeating that mistake.
    # -----------------------------------------

    pairs_raw = pd.read_csv(
        "data/processed/skill_pairs.csv"
    )

    cooccurrence_pairs = (

        pairs_raw

        .sort_values(
            "frequency",
            ascending=False
        )

        .head(20)

        .copy()

    )

    cooccurrence_pairs["Pair"] = (

        cooccurrence_pairs["skill_1"]

        + " ↔ "

        + cooccurrence_pairs["skill_2"]

    )

    pair_chart = (

        cooccurrence_pairs

        .set_index("Pair")["frequency"]

    )

    save_horizontal_bar_chart(

        pair_chart,

        "Top Skill Co-occurrence",

        "Frequency",

        "23_Skill_Cooccurrence.png",

        "darkorange"

    )

    print("✓ Skill Co-occurrence Created")

    # --------------------------------------------------
    # Word Cloud
    # --------------------------------------------------

    skills_df = pd.read_csv(
        "data/processed/normalized_skills_long.csv"
    )

    words = (
        skills_df["normalized_skill"]
        .dropna()
        .astype(str)
    )

    text = " ".join(words)

    wc = WordCloud(
        width=2200,
        height=1200,
        background_color="white",
        max_words=200,
        collocations=False,
        colormap="viridis"
    ).generate(text)

    plt.figure(figsize=(16,9))

    plt.imshow(
        wc,
        interpolation="bilinear"
    )

    plt.axis("off")

    plt.title(
        "Normalized Skills Word Cloud",
        fontsize=20,
        weight="bold"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_FOLDER,
            "24_Word_Cloud.png"
        ),
        dpi=300,
        facecolor="white",
        bbox_inches="tight"
    )

    plt.close()

    print("✓ Word Cloud Created")

    # --------------------------------------------------
    # Professional Skill Co-occurrence Heatmap
    # --------------------------------------------------

    heatmap_skills = [

        "SQL",
        "Python",
        "R",
        "statistics",
        "machine learning",
        "Power BI",
        "Tableau",
        "Microsoft Excel",
        "database",
        "computer programming",
        "Amazon Web Services",
        "AWS"

    ]

    heatmap_pairs = pairs_raw[

        pairs_raw["skill_1"].isin(heatmap_skills) &
        pairs_raw["skill_2"].isin(heatmap_skills)

    ]

    matrix = pd.DataFrame(
        0,
        index=heatmap_skills,
        columns=heatmap_skills
    )

    for _, row in heatmap_pairs.iterrows():

        s1 = row["skill_1"]
        s2 = row["skill_2"]
        f = row["frequency"]

        matrix.loc[s1, s2] = f
        matrix.loc[s2, s1] = f

    # Remove diagonal. `pd.DataFrame(0, index=..., columns=...)` can
    # back its data with a read-only array in current numpy/pandas,
    # which makes `np.fill_diagonal(matrix.values, 0)` raise
    # "ValueError: underlying array is read-only". Zeroing the
    # diagonal through pandas' own .loc indexing avoids touching the
    # raw numpy buffer at all, sidestepping that entirely.
    for skill in heatmap_skills:

        matrix.loc[skill, skill] = 0

    plt.figure(figsize=(12,10))

    sns.heatmap(

        matrix,

        annot=True,

        fmt=".0f",

        cmap="YlGnBu",

        linewidths=0.5,

        square=True,

        cbar_kws={
            "label":"Co-occurrence Frequency"
        }

    )

    plt.title(

        "Business Analytics Skill Co-occurrence Heatmap",

        fontsize=20,

        weight="bold"

    )

    plt.xticks(

        rotation=45,

        ha="right"

    )

    plt.yticks(

        rotation=0

    )

    plt.tight_layout()

    plt.savefig(

        os.path.join(

            OUTPUT_FOLDER,

            "25_Correlation_Heatmap.png"

        ),

        dpi=300,

        facecolor="white",

        bbox_inches="tight"

    )

    plt.close()

    print("✓ Correlation Heatmap Created")

    # --------------------------------------------------
    # Skill Network Graph (Publication Quality)
    # --------------------------------------------------

    network_skills = [

        "SQL",
        "Python",
        "R",
        "statistics",
        "machine learning",
        "Microsoft Excel",
        "Power BI",
        "Tableau",
        "business intelligence",
        "data mining",
        "computer programming",
        "database",
        "Amazon Web Services",
        "AWS",
        "Microsoft Azure",
        "Azure",
        "Snowflake",
        "Databricks",
        "deep learning",
        "data analysis"

    ]

    network_pairs = pairs_raw[

        pairs_raw["skill_1"].isin(network_skills) &
        pairs_raw["skill_2"].isin(network_skills)

    ]

    network_pairs = (

        network_pairs

        .sort_values(
            "frequency",
            ascending=False
        )

        .head(30)

    )

    G = nx.Graph()

    for _, row in network_pairs.iterrows():

        G.add_edge(
            row["skill_1"],
            row["skill_2"],
            weight=row["frequency"]
        )

    # ---------------------------------------
    # Professional Layout
    # ---------------------------------------

    pos = nx.spring_layout(
        G,
        k=2.3,
        iterations=400,
        seed=42
    )

    # ---------------------------------------
    # Degree
    # ---------------------------------------

    degree = dict(G.degree())

    # Larger hub nodes
    node_sizes = [
        1400 + degree[node] * 450
        for node in G.nodes()
    ]

    # Hub colouring
    hub_threshold = max(degree.values()) - 1

    node_colors = []

    for node in G.nodes():

        if degree[node] >= hub_threshold:

            node_colors.append("darkorange")

        else:

            node_colors.append("royalblue")

    # ---------------------------------------
    # Edge widths
    # ---------------------------------------

    weights = [
        G[u][v]["weight"]
        for u, v in G.edges()
    ]

    max_weight = max(weights)

    edge_widths = [
        1.5 + (w / max_weight) * 7
        for w in weights
    ]

    # ---------------------------------------
    # Draw Figure
    # ---------------------------------------

    plt.figure(figsize=(18,14))

    # `connectionstyle` only affects edges drawn as FancyArrowPatches
    # (i.e. when `arrows=True`); with the default `arrows=False`,
    # edges are drawn as a plain LineCollection and the argument is
    # silently ignored, which is what produced the
    # "connectionstyle keyword argument is not applicable" warning.
    # Since curved edges weren't otherwise being used here, the
    # argument is dropped rather than switching on arrows.
    nx.draw_networkx_edges(

        G,

        pos,

        edge_color="#9E9E9E",

        alpha=0.28,

        width=edge_widths

    )

    nx.draw_networkx_nodes(

        G,

        pos,

        node_color=node_colors,

        alpha=0.95,

        node_size=node_sizes,

        edgecolors="black",

        linewidths=1.5

    )

    nx.draw_networkx_labels(

        G,

        pos,

        font_size=12,

        font_weight="bold",

        bbox=dict(

            facecolor="white",

            edgecolor="none",

            alpha=0.80,

            pad=0.25

        )

    )

    plt.title(

        "Business Analytics Skill Co-occurrence Network",

        fontsize=22,

        weight="bold"

    )

    plt.axis("off")

    plt.tight_layout()

    plt.figtext(
        0.5,
        0.01,
        "Node size represents the number of skill connections (degree). Edge thickness represents co-occurrence frequency.",
        ha="center",
        fontsize=10
    )

    plt.savefig(

        os.path.join(

            OUTPUT_FOLDER,

            "26_Skill_Network_Graph.png"

        ),

        dpi=300,

        facecolor="white",

        bbox_inches="tight"

    )

    plt.close()

    print("✓ Skill Network Graph Created")

    print("=" * 60)
    print("Advanced Analytics Completed Successfully")
    print("Charts saved to:", OUTPUT_FOLDER)
    print("=" * 60)