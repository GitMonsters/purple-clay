"""
app/streamlit_main.py
----------------------
Interactive Streamlit UI for the Purple Clay UGI simulator.

Run with:
    streamlit run app/streamlit_main.py
"""

import sys
import os

# Allow running from the repo root or from the app/ directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import plotly.graph_objs as go
import streamlit as st

from simulator.geometry_module import generate_spiral_path, torus_surface
from simulator.bloch_projection import bloch_sphere_wireframe
from simulator.reaction_diffusion_gpu import run_simulation

st.set_page_config(page_title="Purple Clay – UGI Simulator", layout="wide")

# ---------------------------------------------------------------------------
# Sidebar – simulation parameters
# ---------------------------------------------------------------------------
st.sidebar.title("⚙️ Simulation Parameters")

st.sidebar.subheader("Grid & Integration")
N      = st.sidebar.slider("Grid size N", 32, 256, 64, step=32)
steps  = st.sidebar.slider("Steps", 100, 5000, 500, step=100)
dt     = st.sidebar.number_input("Time step dt", value=0.01, step=0.001, format="%.4f")

st.sidebar.subheader("Reaction-Diffusion")
alpha  = st.sidebar.slider("α (diffusion)", 0.001, 0.2, 0.03)
beta_L = st.sidebar.slider("β_L (left reaction)", 0.0, 5.0, 0.6)
beta_R = st.sidebar.slider("β_R (right reaction)", 0.0, 10.0, 4.5)
kappa  = st.sidebar.slider("κ (coupling)", 0.0, 2.0, 0.4)
lam    = st.sidebar.slider("λ (memory restore)", 0.0, 2.0, 0.5)
gamma  = st.sidebar.slider("γ (memory rate)", 0.001, 0.2, 0.02)
eta    = st.sidebar.slider("η (memory cubic)", 0.001, 0.5, 0.05)
epsilon = st.sidebar.slider("ε (forcing amp.)", 0.0, 1.0, 0.2)

st.sidebar.subheader("Options")
quantize       = st.sidebar.checkbox("6-bit quantisation", value=True)
track_entropy  = st.sidebar.checkbox("Track entropy", value=True)
track_lyapunov = st.sidebar.checkbox("Track Lyapunov", value=True)

st.sidebar.markdown("---")
st.sidebar.subheader("🔑 API Key Storage")
api_key = st.sidebar.text_input("API Key (stored in session only)", type="password")
if api_key:
    st.session_state["api_key"] = api_key
    st.sidebar.success("Key stored in session.")

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
st.title("🏺 Purple Clay — Unified Geometric Intelligence Simulator")
st.markdown(
    """
    A computational research platform modelling symbolic information flow through
    **toroidal geometry**, **Bloch sphere projection**, and **nonlinear reaction-diffusion dynamics**.

    > This is a mathematical simulator. It does not make claims about consciousness or AGI.
    """
)

run_btn = st.button("▶ Run Simulation", type="primary")

if run_btn:
    with st.spinner("Running simulation…"):
        results = run_simulation(
            N=N, alpha=alpha, beta_L=beta_L, beta_R=beta_R,
            kappa=kappa, lam=lam, gamma=gamma, eta=eta, epsilon=epsilon,
            dt=dt, steps=steps,
            quantize=quantize,
            track_entropy=track_entropy,
            track_lyapunov=track_lyapunov,
        )
    st.success("Simulation complete!")

    Psi_L      = results["Psi_L"]
    Psi_R      = results["Psi_R"]
    entropy    = results["entropy"]
    lyapunov   = results["lyapunov"]
    bloch_traj = results["bloch_traj"]

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🌀 Toroidal Spiral",
        "⚛️ Bloch Sphere",
        "🌡️ Field Heatmaps",
        "📈 Entropy",
        "📉 Lyapunov",
    ])

    # ------------------------------------------------------------------
    # Tab 1 – Toroidal spiral
    # ------------------------------------------------------------------
    with tab1:
        st.subheader("Golden Spiral on Torus")
        path = generate_spiral_path(t_max=40, t_step=0.05)
        X_s, Y_s, Z_s = torus_surface()

        surf = go.Surface(
            x=X_s, y=Y_s, z=Z_s,
            colorscale="Purples", opacity=0.35,
            showscale=False, name="Torus",
        )
        spiral = go.Scatter3d(
            x=path[:, 0], y=path[:, 1], z=path[:, 2],
            mode="lines",
            line=dict(color="gold", width=3),
            name="Golden spiral",
        )
        fig1 = go.Figure(data=[surf, spiral])
        fig1.update_layout(
            scene=dict(aspectmode="data"),
            margin=dict(l=0, r=0, t=30, b=0),
            height=550,
        )
        st.plotly_chart(fig1, use_container_width=True)

    # ------------------------------------------------------------------
    # Tab 2 – Bloch sphere
    # ------------------------------------------------------------------
    with tab2:
        st.subheader("Bloch Sphere Trajectory")
        xs, ys, zs = bloch_sphere_wireframe(n=40)
        sphere = go.Surface(
            x=xs, y=ys, z=zs,
            colorscale="Blues", opacity=0.15,
            showscale=False, name="Bloch sphere",
        )
        t_idx = np.linspace(0, len(bloch_traj) - 1, len(bloch_traj))
        traj = go.Scatter3d(
            x=bloch_traj[:, 0], y=bloch_traj[:, 1], z=bloch_traj[:, 2],
            mode="lines",
            line=dict(color=t_idx, colorscale="Plasma", width=3),
            name="Bloch trajectory",
        )
        fig2 = go.Figure(data=[sphere, traj])
        fig2.update_layout(
            scene=dict(
                aspectmode="cube",
                xaxis=dict(range=[-1, 1]),
                yaxis=dict(range=[-1, 1]),
                zaxis=dict(range=[-1, 1]),
            ),
            margin=dict(l=0, r=0, t=30, b=0),
            height=550,
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ------------------------------------------------------------------
    # Tab 3 – Field heatmaps
    # ------------------------------------------------------------------
    with tab3:
        st.subheader("Field Heatmaps (final step)")
        col_l, col_r = st.columns(2)
        with col_l:
            fig_l = go.Figure(go.Heatmap(z=Psi_L, colorscale="Purples"))
            fig_l.update_layout(title="Left hemisphere Ψ_L", height=400)
            st.plotly_chart(fig_l, use_container_width=True)
        with col_r:
            fig_r = go.Figure(go.Heatmap(z=Psi_R, colorscale="Oranges"))
            fig_r.update_layout(title="Right hemisphere Ψ_R", height=400)
            st.plotly_chart(fig_r, use_container_width=True)

    # ------------------------------------------------------------------
    # Tab 4 – Entropy
    # ------------------------------------------------------------------
    with tab4:
        st.subheader("Shannon Entropy over Time")
        if entropy:
            fig_e = go.Figure(go.Scatter(
                y=entropy, mode="lines",
                line=dict(color="purple", width=2),
            ))
            fig_e.update_layout(
                xaxis_title="Step", yaxis_title="H (nats)", height=400,
            )
            st.plotly_chart(fig_e, use_container_width=True)
        else:
            st.info("Entropy tracking was disabled.")

    # ------------------------------------------------------------------
    # Tab 5 – Lyapunov
    # ------------------------------------------------------------------
    with tab5:
        st.subheader("Leading Lyapunov Estimate (log separation)")
        if lyapunov:
            fig_ly = go.Figure(go.Scatter(
                y=lyapunov, mode="lines",
                line=dict(color="crimson", width=2),
            ))
            fig_ly.update_layout(
                xaxis_title="Step",
                yaxis_title="log‖δΨ_L‖",
                height=400,
            )
            st.plotly_chart(fig_ly, use_container_width=True)
        else:
            st.info("Lyapunov tracking was disabled.")

    # ------------------------------------------------------------------
    # Logic Broadcasting panel (placeholder)
    # ------------------------------------------------------------------
    st.markdown("---")
    st.subheader("📡 Logic Broadcasting & Token Minting (simulation)")
    with st.expander("Show details"):
        final_bloch = bloch_traj[-1]
        geom_hash = f"bloch:{final_bloch[0]:.4f},{final_bloch[1]:.4f},{final_bloch[2]:.4f}"
        st.code(geom_hash, language="text")
        st.markdown(
            "In a live deployment this hash would be submitted to the "
            "`SovereignNode` smart contract via `declareNode(geometryHash)`."
        )
        if st.button("🪙 Simulate Token Mint"):
            st.info(f"Simulated mint: geometry hash `{geom_hash}` recorded (no on-chain call made).")
