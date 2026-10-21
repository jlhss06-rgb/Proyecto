# Proyecto
Proyecto_Sprint7

### Resumen y Descripción del Proyecto
Este proyecto consiste en el desarrollo de una herramienta interactiva para explorar el mercado de venta de vehículos usados en EE.UU., utilizando los datos previamente limpios y depurados.
Permite a los usuarios y analistas comprender de manera intuitiva y visual la distribución de las principales características de los vehículos, facilitando la identificación de patrones comerciales y tendencias de depreciación.

### 1. Carga y Depuración de Datos en Memoria
Cada vez que la aplicación se inicia o se recarga, ejecuta las siguientes tareas en segundo plano:
* **Lectura del Dataset:** Carga el archivo `vehicles_us.csv` en un DataFrame de Pandas (`car_data`).
* **Limpieza Síncrona:** Aplica de forma automática las mismas transformaciones del cuaderno de análisis:
  * Rellena valores nulos en `is_4wd` con `0` y `paint_color` con `'unknown'`.
  * Imputa valores faltantes en `model_year`, `cylinders` y `odometer` utilizando la mediana correspondiente según el modelo del vehículo (`groupby('model')`).
  * Convierte las columnas numéricas clave a tipos enteros (`int`).

### 2. Flujo de Interacción del Usuario con los Datos
El verdadero poder de la app radica en su interactividad basada en el **estado de los widgets**:

#### A. El Panel de Filtros Lateral (Sidebar)
* **`st.sidebar.multiselect()`**: Extrae dinámicamente todos los modelos únicos del dataset y genera un menú de selección múltiple. 
* **Filtrado en tiempo real:** Cuando el usuario selecciona o remueve modelos de la lista, Streamlit vuelve a ejecutar el código de arriba a abajo. Se crea una variable `filtered_data` que contiene **únicamente** los registros que coinciden con los modelos seleccionados por el usuario.

#### B. Visualización Tabular Bajo Demanda
* **`st.checkbox()`**: Funciona como un interruptor booleano (`True`/`False`). Si la casilla *"Mostrar datos limpios en una tabla interactiva"* está marcada, se ejecuta `st.dataframe(car_data.head(500))`, renderizando una tabla dinámica que permite ordenar y explorar las primeras 500 filas del dataset limpio.

#### C. Gráficos Interactivos mediante Botones (`st.button`)
* Al hacer clic en **"Construir Histograma"** o **"Construir Gráfico de Dispersión"**, se evalúa la condición del botón como verdadera por un instante. 
* La aplicación genera un gráfico de **Plotly Express** utilizando únicamente el subconjunto `filtered_data` (los datos ya filtrados por los modelos del sidebar).
* El histograma además lee el valor de un selector (`st.selectbox`) para decidir dinámicamente con qué columna categórica (`condition`, `transmission` o `fuel`) se colorearán las barras.

#### D. Reactividad Instantánea mediante Casillas de Verificación (`st.checkbox`)
* A diferencia de los botones (que requieren un clic para cada renderizado), las casillas de verificación al final de la app permiten mantener los gráficos visibles permanentemente mientras la casilla esté activa. 
* Si cambias la selección de modelos en la barra lateral con estas casillas marcadas, **los gráficos se actualizarán instantáneamente** en pantalla para reflejar la nueva selección de datos sin necesidad de volver a presionar un botón.

### Resumen del ciclo de vida de Streamlit:
1. El usuario interactúa con un control (mueve un slider, cambia un filtro, marca un checkbox).
2. Streamlit detecta el cambio y **vuelve a ejecutar todo el script de Python de arriba a abajo**.
3. En la nueva ejecución, las variables de los filtros adoptan los nuevos valores elegidos por el usuario.
4. Los gráficos de Plotly se redibujan instantáneamente con el conjunto de datos recién filtrado, creando una experiencia fluida e interactiva.
