import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("scores.csv")
df.columns = df.columns.str.strip()
print(df.head())

lower = {c.lower(): c for c in df.columns}
courses = [lower["math"], lower["python"], lower["db"]]

fig, ax = plt.subplots(figsize=(8, 5))
markers = ["o", "s", "^"]
for course, m in zip(courses, markers):
    df.reset_index().plot.scatter(x="index", y=course, ax=ax,
                                  label=course, marker=m,
                                  color=f"C{courses.index(course)}")
ax.set_xlabel("Student")
ax.set_ylabel("Score")
ax.set_title("Student scores")
ax.legend()
plt.tight_layout()
plt.savefig("scattered.png")
plt.close()

axes = df[courses].plot.hist(subplots=True, layout=(1, 3), figsize=(12, 4),
                             bins=10, legend=True, edgecolor="black")
for ax, course in zip(axes.flatten(), courses):
    ax.set_title(course)
    ax.set_xlabel("Score")
plt.tight_layout()
plt.savefig("histo.png")
plt.close()

ax = df[courses].plot.box(figsize=(6, 5))
ax.set_ylabel("Score")
ax.set_title("Scores by course")
plt.tight_layout()
plt.savefig("box.png")
plt.close()

print("Saved: scattered.png, histo.png, box.png")
