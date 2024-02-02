import streamlit as st
import pandas as pd

# Cargar datos desde el archivo CSV
archivo_csv = 'pypallets.csv'  # Reemplaza con la ruta correcta de tu archivo CSV
df = pd.read_csv(archivo_csv)

# Obtener la lista de materiales únicos
materiales = df['Material'].unique()

# Cargar o crear el DataFrame de solicitudes
df_solicitudes_path = 'df_solicitudes.csv'
try:
    df_solicitudes = pd.read_csv(df_solicitudes_path)
except FileNotFoundError:
    df_solicitudes = pd.DataFrame(columns=['Material', 'OC', 'Proveedor', 'Cantidad Solicitada', 'Fecha'])

# Crear la interfaz de usuario
st.title('Solicitud de Pallets')

# Seleccionar el material usando Selectbox
material_seleccionado = st.selectbox('Pallet a solicitar:', materiales)

# Filtrar las OC disponibles con saldo para el material seleccionado
oc_disponibles = df[df['Material'] == material_seleccionado]
oc_con_saldo = oc_disponibles[oc_disponibles['Saldo'] > 0]

# Mostrar las OC disponibles con saldo
st.subheader('Ordenes de Compra Disponibles con Saldo:')
st.dataframe(oc_con_saldo)

# Seleccionar la OC
oc_seleccionada = st.selectbox('Seleccione la Orden de Compra:', oc_con_saldo['OC'].unique())

# Mostrar el saldo y proveedor de la OC seleccionada
oc_seleccionada_info = oc_con_saldo[oc_con_saldo['OC'] == oc_seleccionada]
saldo_oc_seleccionada = oc_seleccionada_info['Saldo'].values[0]
proveedor_oc_seleccionada = oc_seleccionada_info['Proveedor'].values[0]
st.info(f'Saldo de la Orden de Compra {oc_seleccionada}: {saldo_oc_seleccionada}')
st.info(f'Proveedor de la Orden de Compra {oc_seleccionada}: {proveedor_oc_seleccionada}')

# Seleccionar las fechas en el calendario
fecha_inicio = st.date_input('Fecha de solicitud:')

# Ingresar la cantidad solicitada
cantidad_solicitada = st.number_input('Cantidad Solicitada:', min_value=0, max_value=saldo_oc_seleccionada)

# Botón para realizar la solicitud# Botón para realizar la solicitud
if st.button('Realizar Solicitud'):
    # Generar una fila con los datos ingresados
    nueva_solicitud = pd.DataFrame({
        'Material': [material_seleccionado],
        'OC': [oc_seleccionada],
        'Proveedor': [proveedor_oc_seleccionada],
        'Cantidad Solicitada': [cantidad_solicitada],
        'Fecha': [fecha_inicio],
    })

    # Verificar si df_solicitudes está definido, si no, cargar el DataFrame
    if 'df_solicitudes' not in locals():
        try:
            df_solicitudes = pd.read_csv(df_solicitudes_path)
        except FileNotFoundError:
            df_solicitudes = pd.DataFrame(columns=['Material', 'OC', 'Proveedor', 'Cantidad Solicitada', 'Fecha'])

    # Concatenar el DataFrame de solicitudes con la nueva solicitud
    df_solicitudes = pd.concat([df_solicitudes, nueva_solicitud], ignore_index=True)

    # Guardar el DataFrame de solicitudes en el archivo CSV
    df_solicitudes.to_csv(df_solicitudes_path, index=False)

    st.subheader('Resumen solicitudes:')
    st.dataframe(df_solicitudes)