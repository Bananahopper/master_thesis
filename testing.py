import pandas as pd
import matplotlib.pyplot as plt

# Sample dataframe
data = {
    "Patient": ["Patient1", "Patient2", "Patient3", "Patient4"],
    "Connectome overlap": [100, 200, 150, 120],
}

df = pd.DataFrame(data)

# Creating the 'Severity' column based on the new conditions
df["Severity"] = df["Connectome overlap"].apply(
    lambda x: "severe" if x > 150 else ("Middle" if 100 < x <= 150 else "not severe")
)

# Counting the frequency of each severity class
severity_counts = df["Severity"].value_counts()
severity_counts = severity_counts / sum(severity_counts)
severity_counts = severity_counts.reindex(["severe", "Middle", "not severe"])

# Plotting with specific colors for each class
colors = {"severe": "red", "Middle": "orange", "not severe": "green"}

# Applying the colors to the bars based on their labels
severity_counts.plot(
    kind="bar", color=[colors[label] for label in severity_counts.index]
)
plt.xlabel("Severity")
plt.ylabel("Frequency")
plt.title("Frequency of Patients by Severity Class")
plt.show()
