import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("GastroGPT_Evaluation_Data.csv")

# Set user column as index
df.set_index("User", inplace=True)

# Select score columns
score_columns = ["Relevance Score", "Usefulness Score", "Presentation Score"]

# Define a nice orange color palette (same tone, different shades)
orange_colors = ['#FFB347', '#FFA500', '#FF8C00']  # light orange, classic orange, dark orange

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
df[score_columns].plot(kind="bar", ax=ax, color=orange_colors)

ax.set_title("GastroGPT Evaluation Scores by User", fontsize=14)
ax.set_ylabel("Score (1-5)")
ax.set_xlabel("User")
plt.xticks(rotation=0)
plt.ylim(3.5, 5.1)
plt.legend(title="Evaluation Metric")
plt.tight_layout()

# Save to root directory
plt.savefig("evaluation_results.png")
