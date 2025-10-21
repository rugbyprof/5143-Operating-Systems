import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---------------------------------------
# Load timeline.csv into Pandas
# ---------------------------------------
df = pd.read_csv("./timelines/timeline0001.csv")


# Flatten CPU/IO columns (lists stored as strings → eval safely)
def parse_list(s):
    try:
        return eval(s) if isinstance(s, str) else s
    except Exception:
        return []


df["cpus"] = df["cpus"].apply(parse_list)
df["ios"] = df["ios"].apply(parse_list)

# ---------------------------------------
# Build per-device schedules
# ---------------------------------------
records = []
for _, row in df.iterrows():
    t = row["time"]
    for cid, proc in enumerate(row["cpus"]):
        if proc and proc != "None":
            records.append({"device": f"CPU{cid}", "time": t, "process": proc})
    for did, proc in enumerate(row["ios"]):
        if proc and proc != "None":
            records.append({"device": f"IO{did}", "time": t, "process": proc})

sched_df = pd.DataFrame(records)

# ---------------------------------------
# Plot Gantt chart
# ---------------------------------------
fig, ax = plt.subplots(figsize=(12, 6))

devices = sched_df["device"].unique()
device_map = {dev: i for i, dev in enumerate(devices)}

colors = {}
ylabels = []
for dev in devices:
    ylabels.append(dev)

for dev, dev_df in sched_df.groupby("device"):
    y = device_map[dev]
    for proc, proc_df in dev_df.groupby("process"):
        # group consecutive time slots
        times = proc_df["time"].sort_values().tolist()
        start = times[0]
        prev = start
        for t in times[1:] + [None]:
            if t is None or t != prev + 1:
                ax.broken_barh(
                    [(start, prev - start + 1)],
                    (y - 0.4, 0.8),
                    facecolors=colors.get(proc, None),
                    edgecolor="black",
                    linewidth=0.5,
                    label=proc if proc not in colors else "",
                )
                if proc not in colors:
                    colors[proc] = ax._get_lines.get_next_color()
                if t is not None:
                    start = t
            prev = t

# Labels and formatting
ax.set_yticks(range(len(devices)))
ax.set_yticklabels(ylabels)
ax.set_xlabel("Time")
ax.set_title("Process Execution Timeline (Gantt Chart)")

# Build legend (one color per process)
patches = [mpatches.Patch(color=col, label=proc) for proc, col in colors.items()]
ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.show()
