# Controlling Arrival Time Traffic

Controlling **arrival times** is critical when training or testing a **hybrid scheduling algorithm** because it directly influences how the scheduler balances responsiveness and throughput under dynamic workloads. In real systems, processes rarely arrive in perfect synchrony — some workloads are bursty, others are steady or delayed — and an effective scheduler must adapt its strategy accordingly. By manipulating arrival distributions (e.g., clustered vs. sparse arrivals), we can expose the scheduler to diverse timing patterns, forcing it to learn when to favor preemption (for interactive responsiveness) versus when to commit longer CPU bursts (for efficiency). This control turns static scheduling into a realistic simulation environment where algorithms can evolve and generalize to the unpredictable timing behavior of real-world systems.

So, for us, instead of just using random to decide arrival timess, we can controll if arrivals are sparse (really spread out), or batchy (really bunched up).

**Basically: **

1. **All arrive “together-ish” (batchy)** — sample _arrival times directly_ from a Normal with a shared mean.
2. **Stream in over time (sparse or bursty)** — sample _inter-arrival_ times from a Gamma whose shape is set by your mean & std.

---

## Formulas & Snippets

So here are some formulas that will allow you to:

1. Batch em Up
2. Spread em Out
3. Swap back and forth

### 1) Single “batch” around a moment (Normal on arrival time)

If you want many jobs to hit around the same time `μ` (e.g., at `t=50`) and control how tightly they clump with `σ`:

**Formula**

- Arrival time for job _i_:  
  \[
  a*i \sim \text{Normal}(\mu,\sigma^2),\quad \text{then clamp/round to } \mathbb{Z}*{\ge 0}
  \]
- Smaller `σ` ⇒ _more_ pileups at the same tick.
- Larger `σ` ⇒ more spread.

**Python**

```python
import random
def batched_arrivals(n, mu, sigma):
    times = [max(0, int(round(random.gauss(mu, sigma)))) for _ in range(n)]
    return sorted(times)
```

> Tip: To create multiple class periods / waves, use a _mixture_ of Normals with different centers: choose a center `c` from a list, then sample `Normal(c, σ)`.

---

### 2) Flow over time (Gamma on inter-arrival)

If you want a _process_ that trickles jobs in (and you still want to control the variance with `mean` and `std`), use a **Gamma** for inter-arrival times. This is great because the **coefficient of variation** (σ/μ) is your “burstiness dial”:

- Set desired **mean inter-arrival** `μ` and **std** `σ` (both > 0).
- Convert to Gamma parameters:
  \[
  k=\left(\frac{\mu}{\sigma}\right)^2,\qquad \theta=\frac{\sigma^2}{\mu}
  \]
  where `k` is shape, `θ` is scale.
- Draw inter-arrival times \( \Delta*i \sim \text{Gamma}(k,\theta) \) and cumulative sum:
  \[
  a_i=\left\lfloor \sum*{j=1}^{i} \Delta_j \right\rfloor
  \]

**Burstiness intuition**

- `σ << μ` → `k` large → _regular_ spacing (sparse, steady).
- `σ ≈ μ` → `k ≈ 1` → exponential/Possion-like (random).
- `σ > μ` → `k < 1` → **bursty** (clumps and lulls).

**Python**

```python
import random
def streamed_arrivals(n, mean_inter, std_inter):
    assert mean_inter > 0 and std_inter > 0
    k = (mean_inter / std_inter) ** 2       # shape
    theta = (std_inter ** 2) / mean_inter   # scale
    t = 0.0
    times = []
    for _ in range(n):
        t += random.gammavariate(k, theta)  # Gamma(shape=k, scale=theta)
        times.append(int(t))                # tick index
    return times
```

---

### 3) Hybrid (sometimes batches, sometimes stream)

You can blend both behaviors with a mixing prob `p`:

- With prob `p`, sample from a Normal centered at one of a few “batch centers”.
- With prob `1-p`, use the Gamma inter-arrival stream.

**Python sketch**

```python
def hybrid_arrivals(n, p_batch, centers, sigma, mean_inter, std_inter):
    # precompute a stream generator
    stream = iter(streamed_arrivals(n*2, mean_inter, std_inter))
    times = []
    for _ in range(n):
        if random.random() < p_batch:
            c = random.choice(centers)
            times.append(max(0, int(round(random.gauss(c, sigma)))))
        else:
            times.append(next(stream))
    return sorted(times)
```

---

### Quick presets you should try

- **“Everyone hits at once”**: Normal with `μ=50, σ=0.5`.
- **“Loose lecture start”**: Normal with `μ=50, σ=10`.
- **“Steady stream”**: Gamma with `mean_inter=5, std_inter=1` (regular).
- **“Bursty chaos”**: Gamma with `mean_inter=5, std_inter=8` (very bursty).

This method gives us a clean, mean+std controlled way to dial **clumping vs spread** without changing the rest of the simulator.
