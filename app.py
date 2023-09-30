import streamlit as st
from graphs import GravityGraphs

def main():
    st.title("Gravity Graphs App")

    # Ввод данных пользователем
    R0 = st.number_input("Radius of the object (R0) in km", min_value=int(1e3), max_value=int(1e5), value=int(49244), step=int(1e3))
    M0 = st.number_input("Mass of the object (M0) in kg", min_value=1e20, max_value=1e30, value=1.02e26, step=1e25)
    RAD_VEL = st.number_input("Radial velocity of the object in 1/s", min_value=1e3, max_value=1e5, value=9648.0, step=100.0)
    
    label_ofset_V_x = st.slider('label_offset_V_x', min_value=0, max_value=20)
    label_ofset_V_y = st.slider('label_offset_V_y', min_value=0, max_value=20)
    label_ofset_F_x = st.slider('label_offset_F_x', min_value=0, max_value=20)
    label_ofset_F_y = st.slider('label_offset_F_y', min_value=0, max_value=20)
    
    gravity_graphs = GravityGraphs(R0, M0, RAD_VEL)

    if st.button("Generate Gravity Graphs"):
        gravity_graphs.plot_gravity_graphs([(label_ofset_V_x, label_ofset_V_y), (label_ofset_F_x, label_ofset_F_y)])
        gravity_graphs.plot_D2V()
        
    if st.button("Generate Tables"):
        table = gravity_graphs.get_tables()
        
        # Отображаем таблицы подряд
        st.write("Table")
        st.write(table)
        
        csv_data = table.to_csv(index=False)
        st.download_button("Download CSV", csv_data, "gravity_table.csv", "text/csv")


if __name__ == "__main__":
    main()

