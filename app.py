import streamlit as st
from graphs import GravityGraphs

def main():
    st.title("Gravity Graphs App")
    
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select page", ["Task 1", "Task 2(Model)"])

    if page == 'Task 1':
        # Ввод данных пользователем
        R0 = st.number_input("Radius of the object (R0) in km", min_value=0., max_value=1e5, value=49244.)
        M0 = st.number_input("Mass of the object (M0) in kg", min_value=0., max_value=1e30, value=1.02e26)
        RAD_VEL = st.number_input("Radial velocity of the object in 1/s", min_value=0., max_value=1e5, value=9648.0)
        
        label_ofset_V_x = st.slider('label_offset_V_x', min_value=-20, max_value=20)
        label_ofset_V_y = st.slider('label_offset_V_y', min_value=-20, max_value=20)
        label_ofset_F_x = st.slider('label_offset_F_x', min_value=-20, max_value=20)
        label_ofset_F_y = st.slider('label_offset_F_y', min_value=-20, max_value=20)
        
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

    elif page == "Task 2(Model)":
        R0 = st.number_input("Radius of the object (R0) in m", min_value=0., max_value=1e6)
        H0 = st.number_input("Depth of the object (H0) in m", min_value=0., max_value=1e6)
        density = st.number_input("Density of the object ($\\sigma$) in $\\frac{g}{sm^3}$", min_value=0., max_value=10.)
        density_external = st.number_input("Density of the outer space ($\\sigma_e$) in $\\frac{g}{sm^3}$", min_value=1., max_value=4.)
        
        gravity_graphs = GravityGraphs(1, 1, 1)
        
        if st.button("Generate Model Graphs"):
            gravity_graphs.draw_model(R0, density, density_external, H0)
        

if __name__ == "__main__":
    main()

