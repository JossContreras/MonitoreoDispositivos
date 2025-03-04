import dash
from dash import dcc, html
import plotly.graph_objects as go
import networkx as nx
import random

# ==========================
# 🔹 Inicializar la aplicación Dash
# ==========================
app = dash.Dash(__name__)

# ==========================
# 🔹 Definir departamentos y ubicaciones
# ==========================
departamentos = {
    "TI": {"pos_x": 0, "pos_y": 1, "cantidad": 20},
    "Finanzas": {"pos_x": -1, "pos_y": 0.5, "cantidad": 20},
    "Recursos Humanos": {"pos_x": 1, "pos_y": 0.5, "cantidad": 15},
    "Seguridad": {"pos_x": -1, "pos_y": -0.5, "cantidad": 15},
    "Marketing": {"pos_x": 1, "pos_y": -0.5, "cantidad": 15},
    "Administración": {"pos_x": 0, "pos_y": -1, "cantidad": 15}
}

# ==========================
# 🔹 Definir tipos de dispositivos y sus íconos
# ==========================
device_types = ["Router", "Switch", "PC", "Servidor", "Cámara", "Teléfono"]
device_icons = {
    "Router": "🔷",
    "Switch": "🔳",
    "PC": "💻",
    "Servidor": "🖥️",
    "Cámara": "📷",
    "Teléfono": "📱"
}

# ==========================
# 🔹 Generar dispositivos organizados por departamentos
# ==========================
device_id = 1
info_dispositivos = {}
pos = {}
departamento_nodos = {}

for depto, valores in departamentos.items():
    departamento_nodos[depto] = []
    
    for _ in range(valores["cantidad"]):
        info_dispositivos[device_id] = {
            "nombre": f"{random.choice(device_types)} - 192.168.1.{device_id}",
            "departamento": depto
        }
        pos[device_id] = (
            valores["pos_x"] + random.uniform(-0.3, 0.3),
            valores["pos_y"] + random.uniform(-0.3, 0.3)
        )
        departamento_nodos[depto].append(device_id)
        device_id += 1

# ==========================
# 🔹 Crear conexiones entre departamentos (simulando enlaces)
# ==========================
G = nx.DiGraph()
for depto, nodos in departamento_nodos.items():
    for i in range(1, len(nodos)):
        G.add_edge(nodos[i - 1], nodos[i])  # Conexión interna en el mismo departamento

# 🔹 Crear conexiones entre departamentos
departamento_lista = list(departamento_nodos.keys())
for i in range(len(departamento_lista) - 1):
    d1 = departamento_lista[i]
    d2 = departamento_lista[i + 1]
    if departamento_nodos[d1] and departamento_nodos[d2]:
        G.add_edge(random.choice(departamento_nodos[d1]), random.choice(departamento_nodos[d2]))

# ==========================
# 🔹 Crear trazas para los enlaces (líneas)
# ==========================
edge_x, edge_y = [], []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='gray'),
    hoverinfo='none',
    mode='lines'
)

# ==========================
# 🔹 Crear trazas para los nodos (íconos y nombres)
# ==========================
node_x, node_y, node_text = [], [], []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    device_type = info_dispositivos[node]["nombre"].split(" - ")[0]
    node_text.append(f"{device_icons.get(device_type, '❓')} {info_dispositivos[node]['nombre']}")

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=node_text,
    textposition="top center",
    marker=dict(size=15, color='lightblue', line=dict(width=2, color='black')),
    hoverinfo='text'
)

# ==========================
# 🔹 Configurar la visualización
# ==========================
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title="🌐 Mapa de Red por Departamentos",
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=10, l=10, r=10, t=50),
                    height=800,  # 📌 Optimizado para pantalla completa
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                ))

# ==========================
# 🔹 Crear la interfaz de usuario con Dash
# ==========================
app.layout = html.Div([
    html.H1("🏢 Mapa de Red Organizado por Departamentos", style={'textAlign': 'center'}),
    dcc.Graph(id='grafo-red', figure=fig, style={'height': '90vh'})  # 📌 Expande a toda la pantalla
])

# ==========================
# 🔹 Ejecutar la aplicación
# ==========================
if __name__ == '__main__':
    app.run_server(debug=True)
