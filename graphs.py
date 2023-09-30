import numpy as np
import matplotlib.pyplot as plt
from gravitational_functions import GravitationalFunctions
import streamlit as st
import pandas as pd


class GravityGraphs:
    def __init__(self, R0, M0, RAD_VEL):
        self.R0 = R0
        self.M0 = M0
        self.RAD_VEL = RAD_VEL
        self.grav_functions = GravitationalFunctions(self.R0, self.M0, self.RAD_VEL)
        self.MEASURES = {'THOUSAND_KILOMETER': 1e8, 'KILOMETER': 1e5, 'METER': 100, 'SGS': 1, 'MILIGAL': 1e3, 'EOTVOS': 1e9}

    def get_scale(self, maximum):
        format = 2 - round(np.log10(maximum))
        return 10 ** format

    def add_graph_V(self, x_axis, y_axis, annotatablex=[], annotatabley=[], offset=(0, 0), measurex='SGS', measurey='SGS',
                    normalizex=False, normalizey=False, linelabel='', ylabel='', color='steelblue', is_second=False):
        # Getting right scales
        scalex = self.MEASURES[measurex]
        scaley = self.MEASURES[measurey]

        # Intermediate calculations
        m_x = max(x_axis)
        m_y = max(y_axis)

        # Normalization of graphic values
        if normalizex:
            scalex /= self.get_scale(m_x)
        if normalizey:
            scaley /= self.get_scale(m_y)

        # Check if should create twinx or format x
        if is_second:
            axis = plt.gca().twinx()
        else:
            axis = plt.gca()
            plt.xlabel('$\\rho, тыс.км$')
            axis.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:.0f}".format(x / scalex)))
        
        # Setting axis labels
        if round(np.log10(scaley)) != 0:
            plt.ylabel(ylabel + '$10^{' + f'{str(round(np.log10(scaley)))}' + '}$')
        else:
            plt.ylabel(ylabel)


        # Format of axis
        plt.ylim(min(y_axis) - 0.1 * np.abs(min(y_axis)), m_y * 1.05)
        plt.xlim(0, m_x * 1.05)
        axis.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, loc: "{:.0f}".format(y / scaley)))

        # Drawing a graph
        line, = axis.plot(x_axis, y_axis, label=linelabel, color=color)

        # Drawing annotated points
        for i in range(len(annotatablex)):
            axis.scatter(annotatablex[i], annotatabley[i], color=color)
            axis.annotate(f'{annotatabley[i] / scaley:.2f}', (annotatablex[i], annotatabley[i]), xytext=offset,
                          textcoords='offset points')
        # Returning line object for further use in legend
        return line

    def plot_gravity_graphs(self, label_offsets):
        fig = plt.figure(figsize=(6, 6))
        plt.title('Графики гравитационного потенциала и силы притяжения')

        x_axis = np.linspace(0, 10 * self.grav_functions.RADIUS, 1000)
        indexes = np.array([0, 0.4 * self.grav_functions.RADIUS, 0.8 * self.grav_functions.RADIUS, self.grav_functions.RADIUS,
                            1.5 * self.grav_functions.RADIUS, 2 * self.grav_functions.RADIUS, 3 * self.grav_functions.RADIUS,
                            4 * self.grav_functions.RADIUS, 5 * self.grav_functions.RADIUS, 6 * self.grav_functions.RADIUS,
                            10 * self.grav_functions.RADIUS])
        lines = []

        # Drawing graphs with parameters
        lines.append(self.add_graph_V(x_axis=x_axis, y_axis=self.grav_functions.V(x_axis), annotatablex=indexes,
                                      annotatabley=self.grav_functions.V(indexes), offset=label_offsets[0],
                                      measurex='THOUSAND_KILOMETER', measurey='SGS', normalizex=False,
                                      normalizey=True, linelabel='График потенциала',
                                      ylabel='$V(\\rho), \\frac{см^2}{с^2}$', color='steelblue', is_second=False))
        lines.append(self.add_graph_V(x_axis=x_axis, y_axis=self.grav_functions.DV(x_axis), annotatablex=indexes,
                                      annotatabley=self.grav_functions.DV(indexes), offset=label_offsets[1],
                                      measurex='THOUSAND_KILOMETER', measurey='SGS', normalizex=False,
                                      normalizey=True, linelabel='График cилы', ylabel='F, Гал',
                                      color='orange', is_second=True))
        

        # Drawing labels
        labels = [line.get_label() for line in lines]
        plt.legend(lines, labels, loc='upper right')

        st.pyplot(fig)
    
    def plot_D2V(self):
        fig = plt.figure(figsize=(6, 6))
        plt.title('График второй производной потенциала')
        
        indexes = np.array([0, 0.4 * self.grav_functions.RADIUS, 0.8 * self.grav_functions.RADIUS, self.grav_functions.RADIUS,
                            1.5 * self.grav_functions.RADIUS, 2 * self.grav_functions.RADIUS, 3 * self.grav_functions.RADIUS,
                            4 * self.grav_functions.RADIUS, 5 * self.grav_functions.RADIUS, 6 * self.grav_functions.RADIUS,
                            10 * self.grav_functions.RADIUS])
        
        x_axis = np.linspace(0, self.grav_functions.RADIUS - 1e-1, 1000)
        
        line = self.add_graph_V(x_axis=x_axis, y_axis=self.grav_functions.D2V(x_axis), annotatablex=indexes,
                                      annotatabley=self.grav_functions.D2V(indexes), offset=(5, 5),
                                      measurex='THOUSAND_KILOMETER', normalizex=False,
                                      normalizey=False, linelabel='График второй производной потенциала',
                                      ylabel='$\\frac{d^2V}{d\\rho^2}, Э $', color='steelblue', is_second=False)
        
        x_axis1 = np.linspace(self.grav_functions.RADIUS, 10 * self.grav_functions.RADIUS, 1000)
        
        line1 = self.add_graph_V(x_axis=x_axis1, y_axis=self.grav_functions.D2V(x_axis1), annotatablex=indexes,
                                      annotatabley=self.grav_functions.D2V(indexes), offset=(5, 5),
                                      measurex='THOUSAND_KILOMETER', normalizex=False,
                                      normalizey=False,
                                      ylabel='$\\frac{d^2V}{d\\rho^2}, Э $', color='steelblue', is_second=False)
        
        plt.ylim(min(self.grav_functions.D2V(x_axis)) * 1.1, max(self.grav_functions.D2V(x_axis1)) * 1.1)
        plt.legend()
        
        st.pyplot(fig)


    def get_tables(self):
        indexes = np.array([0, 0.4 * self.grav_functions.RADIUS, 0.8 * self.grav_functions.RADIUS, self.grav_functions.RADIUS,
                            1.5 * self.grav_functions.RADIUS, 2 * self.grav_functions.RADIUS, 3 * self.grav_functions.RADIUS,
                            4 * self.grav_functions.RADIUS, 5 * self.grav_functions.RADIUS, 6 * self.grav_functions.RADIUS,
                            10 * self.grav_functions.RADIUS])

        # Рассчитываем значения для всех функций
        V_values = self.grav_functions.V(indexes)
        DV_values = self.grav_functions.DV(indexes)
        D2V_values = self.grav_functions.D2V(indexes)

        # Создаем таблицы данных для каждой функции
        V_table = pd.DataFrame({'Index': indexes, 'V': V_values})
        DV_table = pd.DataFrame({'Index': indexes, 'DV': DV_values})
        D2V_table = pd.DataFrame({'Index': indexes, 'D2V': D2V_values})
        
        result_table = pd.merge(V_table, DV_table, on='Index')
        result_table = pd.merge(result_table, D2V_table, on='Index')
        result_table['Fraction of Radius'] = round(result_table['Index'] / self.grav_functions.RADIUS, 1)
        result_table = result_table[['Fraction of Radius', 'Index', 'V', 'DV', 'D2V']]

        return result_table
        
        