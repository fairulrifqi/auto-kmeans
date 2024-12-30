# library
import streamlit as st
import numpy as np
import pandas as pd
import openpyxl as op

import matplotlib.pyplot as plt
#sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.metrics import davies_bouldin_score

## Header
st.title(":bar_chart: Auto KMeans Clustering Website")
st.divider()

## Upload
dataframe = st.file_uploader(
    "Pilih file excel", accept_multiple_files= False, type=['xlsx','csv'],
)

## Dataframe
if dataframe is not None:
    st.title("Data Preview")
    st.divider()
    if dataframe.type == 'text/csv':
        df = pd.read_csv(dataframe)
        st.dataframe(df, use_container_width=True)
    else:
        df = pd.read_excel(dataframe)
        st.dataframe(df, use_container_width=True)

    st.write("Pilih column yang akan kamu cluster: ")
    df_dimcol = list(df.select_dtypes(exclude=['int64','float64']))
    df_mcol = list(df.select_dtypes(exclude=['object']))
    df_metriccol = []

    # dimensi
    if len(df_dimcol) != 0:
        df_dimensicol = st.selectbox("Kolom dimensi", df_dimcol)
        st.write('Dimensi clustering:')
        st.dataframe(df[df_dimensicol], use_container_width=True)

    # meteric
    st.write('Dataframe clustering:')
    for col in df_mcol:
        if st.checkbox(str(col), value=True):
            df_metriccol.append(col)
    df_clustering = df[df_metriccol]
    st.divider()
    st.dataframe(df_clustering, use_container_width=True)
    parameter = st.number_input("Pilih jumlah cluster: ", 0, len(df))
    ## Clustering
    if "clicked" not in st.session_state:
        st.session_state["clicked"] = False

    def onSearch(opt):
        st.session_state["clicked"] = True

    def drawBtn():
        option= ...
        st.button("Mulai Cluster", on_click= onSearch, args= [option])
    drawBtn()


    def cluster():
        st.divider()
        st.write("Data Transformation")
        # Scaling data
        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(df_clustering)
        st.write("Scaling data row 1 :", x_scaled[0])

        # PCA
        Pca = PCA(n_components=2)
        x_pca = Pca.fit_transform(x_scaled)
        st.write("Scaling data row 1 :", x_pca[0])

        # Kmeans
        kmeans = KMeans(n_clusters= parameter, random_state=42)
        kmeans.fit(x_pca)

        # Plot kmeans
        u_labels = np.unique(kmeans.labels_)

        fig, ax = plt.subplots()

        # Scatter plot for each cluster
        for i in u_labels:
            ax.scatter(
                x_pca[kmeans.labels_ == i, 0],
                x_pca[kmeans.labels_ == i, 1],
                label=f"Cluster {i}"
            )

        # Plot centroids
        ax.scatter(
            kmeans.cluster_centers_[:, 0],
            kmeans.cluster_centers_[:, 1],
            s=80,
            color='black',
            label="Centroids"
        )

        # Add legend and labels
        ax.legend()
        ax.set_title("Clusters and Centroids")
        ax.set_xlabel("PCA Component 1")
        ax.set_ylabel("PCA Component 2")

        # Display plot in Streamlit
        st.pyplot(fig)
        df['cluster'] = kmeans.labels_
        if len(df_dimcol) != 0:
            final_array = df_metriccol + [df_dimensicol, 'cluster']
            st.dataframe(df[final_array])
        else:
            final_array = df_metriccol + ['cluster']
            st.dataframe(df[final_array])

    if st.session_state["clicked"]:
        cluster()
