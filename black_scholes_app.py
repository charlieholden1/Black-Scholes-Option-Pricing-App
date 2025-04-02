import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Black-Scholes Formula
def black_scholes(S, K, T, sigma, r, option_type="call"):
    if T == 0:
        return max(0, S - K) if option_type == "call" else max(0, K - S)

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# Function to calculate and display option prices
def calculate_option_prices():
    try:
        S = float(spot_price_var.get())
        K = float(strike_price_var.get())
        T = float(time_to_maturity_var.get())
        sigma = float(volatility_var.get())
        r = float(risk_free_rate_var.get())
        
        call_price = black_scholes(S, K, T, sigma, r, "call")
        put_price = black_scholes(S, K, T, sigma, r, "put")
        
        result_text = f"Call Option Price: {call_price:.4f}\nPut Option Price: {put_price:.4f}"
        result_label.config(text=result_text)
    except ValueError:
        result_label.config(text="Please enter valid numerical values")

# Function to update heatmaps
def update_heatmap():
    try:
        strike_price = float(strike_price_var.get())
        time_to_maturity = float(time_to_maturity_var.get())
        risk_free_rate = float(risk_free_rate_var.get())

        min_spot_price = float(min_spot_price_var.get())
        max_spot_price = float(max_spot_price_var.get())
        min_volatility = float(min_volatility_var.get())
        max_volatility = float(max_volatility_var.get())

        spot_prices = np.linspace(min_spot_price, max_spot_price, 10)
        volatilities = np.linspace(min_volatility, max_volatility, 10)

        call_prices = np.zeros((10, 10))
        put_prices = np.zeros((10, 10))

        for i, vol in enumerate(volatilities):
            for j, spot in enumerate(spot_prices):
                call_prices[i, j] = black_scholes(spot, strike_price, time_to_maturity, vol, risk_free_rate, "call")
                put_prices[i, j] = black_scholes(spot, strike_price, time_to_maturity, vol, risk_free_rate, "put")

        # Clear previous heatmaps
        call_ax.clear()
        put_ax.clear()

        # Update Call Heatmap
        sns.heatmap(call_prices, xticklabels=np.round(spot_prices, 2), 
                    yticklabels=np.round(volatilities, 2), cmap="RdYlGn_r", 
                    annot=True, fmt=".2f", ax=call_ax, cbar=False)
        call_ax.set_title("Call Option Price Heatmap")
        call_ax.set_xlabel("Spot Price")
        call_ax.set_ylabel("Volatility")
        
        # Rotate x-axis labels for better readability
        call_ax.set_xticklabels(call_ax.get_xticklabels(), rotation=45)
        call_ax.set_yticklabels(call_ax.get_yticklabels(), rotation=0)

        # Update Put Heatmap
        sns.heatmap(put_prices, xticklabels=np.round(spot_prices, 2), 
                    yticklabels=np.round(volatilities, 2), cmap="RdYlGn_r", 
                    annot=True, fmt=".2f", ax=put_ax, cbar=False)
        put_ax.set_title("Put Option Price Heatmap")
        put_ax.set_xlabel("Spot Price")
        put_ax.set_ylabel("Volatility")
        
        # Rotate x-axis labels for better readability
        put_ax.set_xticklabels(put_ax.get_xticklabels(), rotation=45)
        put_ax.set_yticklabels(put_ax.get_yticklabels(), rotation=0)

        call_canvas.draw()
        put_canvas.draw()
        
    except ValueError:
        result_label.config(text="Please enter valid numerical values for heatmap ranges")

# GUI Setup
root = tk.Tk()
root.title("Black-Scholes Option Pricing")
root.geometry("850x650")  # Increased height to accommodate new elements

# Sidebar for Inputs
sidebar = ttk.Frame(root, padding=10)
sidebar.grid(row=0, column=0, sticky="N", padx=10, pady=10)

# Input Fields for Option Pricing Calculation
ttk.Label(sidebar, text="Current Asset Price:").grid(row=0, column=0, sticky="W")
spot_price_var = tk.StringVar(value="100")
ttk.Entry(sidebar, textvariable=spot_price_var, width=10).grid(row=0, column=1)

ttk.Label(sidebar, text="Strike Price:").grid(row=1, column=0, sticky="W")
strike_price_var = tk.StringVar(value="100")
ttk.Entry(sidebar, textvariable=strike_price_var, width=10).grid(row=1, column=1)

ttk.Label(sidebar, text="Time to Maturity (years):").grid(row=2, column=0, sticky="W")
time_to_maturity_var = tk.StringVar(value="1")
ttk.Entry(sidebar, textvariable=time_to_maturity_var, width=10).grid(row=2, column=1)

ttk.Label(sidebar, text="Volatility (σ):").grid(row=3, column=0, sticky="W")
volatility_var = tk.StringVar(value="0.2")
ttk.Entry(sidebar, textvariable=volatility_var, width=10).grid(row=3, column=1)

ttk.Label(sidebar, text="Risk-Free Rate:").grid(row=4, column=0, sticky="W")
risk_free_rate_var = tk.StringVar(value="0.05")
ttk.Entry(sidebar, textvariable=risk_free_rate_var, width=10).grid(row=4, column=1)

# Input Fields for Heatmap Ranges
ttk.Label(sidebar, text="Min Spot Price:").grid(row=5, column=0, sticky="W")
min_spot_price_var = tk.StringVar(value="80")
ttk.Entry(sidebar, textvariable=min_spot_price_var, width=10).grid(row=5, column=1)

ttk.Label(sidebar, text="Max Spot Price:").grid(row=6, column=0, sticky="W")
max_spot_price_var = tk.StringVar(value="120")
ttk.Entry(sidebar, textvariable=max_spot_price_var, width=10).grid(row=6, column=1)

ttk.Label(sidebar, text="Min Volatility:").grid(row=7, column=0, sticky="W")
min_volatility_var = tk.StringVar(value="0.1")
ttk.Entry(sidebar, textvariable=min_volatility_var, width=10).grid(row=7, column=1)

ttk.Label(sidebar, text="Max Volatility:").grid(row=8, column=0, sticky="W")
max_volatility_var = tk.StringVar(value="0.5")
ttk.Entry(sidebar, textvariable=max_volatility_var, width=10).grid(row=8, column=1)

# Buttons
ttk.Button(sidebar, text="Calculate Option Prices", command=calculate_option_prices).grid(row=9, column=0, columnspan=2, pady=5)
ttk.Button(sidebar, text="Update Heatmap", command=update_heatmap).grid(row=10, column=0, columnspan=2, pady=5)
ttk.Button(sidebar, text="Quit", command=root.quit).grid(row=11, column=0, columnspan=2, pady=5)

# Result Label
result_label = ttk.Label(sidebar, text="", font=('Helvetica', 10))
result_label.grid(row=12, column=0, columnspan=2, pady=10)

# Notebook (Tabs for Graphs)
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=1, padx=10, pady=10, sticky="NSEW")

# Call Heatmap Tab
call_tab = ttk.Frame(notebook)
notebook.add(call_tab, text="Call Option Heatmap")

call_fig, call_ax = plt.subplots(figsize=(5.7, 6.4))
call_canvas = FigureCanvasTkAgg(call_fig, master=call_tab)
call_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Put Heatmap Tab
put_tab = ttk.Frame(notebook)
notebook.add(put_tab, text="Put Option Heatmap")

put_fig, put_ax = plt.subplots(figsize=(5.7, 6.4))
put_canvas = FigureCanvasTkAgg(put_fig, master=put_tab)
put_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Initial heatmap generation
update_heatmap()

root.mainloop()