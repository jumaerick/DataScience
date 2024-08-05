from explore import dataLoader
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

dataset = dataLoader.loadData()


class Clustering:
    def __init__(self, n_iters = 10):
        self.n_iters = n_iters

    def test(self):
        return self.n_iters