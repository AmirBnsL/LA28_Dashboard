"""
Head-to-Head Country Comparison Component
Tug-of-war style visualization comparing two countries.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

# Add parent directory to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.helpers import country_summary


def create_tug_of_war_chart(summary_a: dict, summary_b: dict, country_a: str, country_b: str):
    """Create a tug-of-war style comparison chart."""
    
    # Prepare data - extract numeric values
    metrics = []
    values_a = []
    values_b = []
    
    for key in summary_a.keys():
        val_a = summary_a[key]
        val_b = summary_b[key]
        
        # Convert to numeric
        if isinstance(val_a, str):
            val_a = int(val_a) if val_a.isdigit() else 0
        if isinstance(val_b, str):
            val_b = int(val_b) if val_b.isdigit() else 0
            
        metrics.append(key)
        values_a.append(val_a)
        values_b.append(val_b)
    
    # Calculate percentages for tug-of-war effect
    percentages_a = []
    percentages_b = []
    
    for va, vb in zip(values_a, values_b):
        total = va + vb
        if total > 0:
            pct_a = (va / total) * 100
            pct_b = (vb / total) * 100
        else:
            pct_a = 50
            pct_b = 50
        percentages_a.append(-pct_a)  # Negative for left side
        percentages_b.append(pct_b)   # Positive for right side
    
    # Create figure
    fig = go.Figure()
    
    # Country A bars (left side - blue)
    fig.add_trace(go.Bar(
        y=metrics,
        x=percentages_a,
        orientation='h',
        name=country_a,
        marker=dict(
            color='#3498db',
            line=dict(color='#2980b9', width=1)
        ),
        text=[f"{v}" for v in values_a],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Arial Black'),
        hovertemplate=f"<b>{country_a}</b><br>%{{y}}: %{{text}}<extra></extra>"
    ))
    
    # Country B bars (right side - red)
    fig.add_trace(go.Bar(
        y=metrics,
        x=percentages_b,
        orientation='h',
        name=country_b,
        marker=dict(
            color='#e74c3c',
            line=dict(color='#c0392b', width=1)
        ),
        text=[f"{v}" for v in values_b],
        textposition='inside',
        textfont=dict(color='white', size=14, family='Arial Black'),
        hovertemplate=f"<b>{country_b}</b><br>%{{y}}: %{{text}}<extra></extra>"
    ))
    
    # Update layout
    fig.update_layout(
        barmode='relative',
        bargap=0.3,
        height=400,
        xaxis=dict(
            title="",
            range=[-110, 110],
            showticklabels=False,
            showgrid=False,
            zeroline=True,
            zerolinecolor='#2c3e50',
            zerolinewidth=3,
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=14, family='Arial Black'),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=120, r=50, t=80, b=20),
        showlegend=False,
    )

    # Add country labels on sides
    fig.add_annotation(
        x=-55, y=1.15,
        xref="x", yref="paper",
        text=f"🔵 {country_a}",
        showarrow=False,
        font=dict(size=18, color='#3498db', family='Arial Black'),
    )
    
    fig.add_annotation(
        x=55, y=1.15,
        xref="x", yref="paper",
        text=f"{country_b} 🔴",
        showarrow=False,
        font=dict(size=18, color='#e74c3c', family='Arial Black'),
    )
    
    return fig


def render_head_to_head(df_medals: pd.DataFrame):
    """Render the Head-to-Head Country Comparison section."""
    st.header("⚔️ Head-to-Head Tug of War")
    st.markdown("Watch countries battle it out! The bar shows who dominates each stat.")

    countries = sorted(df_medals["country"].unique())
    col_sel1, col_sel2 = st.columns(2)

    with col_sel1:
        country_a = st.selectbox("🔵 Country A", countries, key="country_a")

    countries_b_options = [c for c in countries if c != country_a]
    with col_sel2:
        country_b = st.selectbox("🔴 Country B", countries_b_options, index=0, key="country_b")

    if country_a and country_b:
        summary_a = country_summary(df_medals, country_a)
        summary_b = country_summary(df_medals, country_b)

        # Create and display tug-of-war chart
        fig = create_tug_of_war_chart(summary_a, summary_b, country_a, country_b)
        st.plotly_chart(fig, width='stretch')
        
        # Winner announcement
        total_a = sum(int(v) if str(v).isdigit() else 0 for v in summary_a.values())
        total_b = sum(int(v) if str(v).isdigit() else 0 for v in summary_b.values())
        
        if total_a > total_b:
            st.success(f"🏆 **{country_a}** leads overall with {total_a} total points vs {total_b}!")
        elif total_b > total_a:
            st.success(f"🏆 **{country_b}** leads overall with {total_b} total points vs {total_a}!")
        else:
            st.info(f"🤝 It's a tie! Both countries have {total_a} total points.")
