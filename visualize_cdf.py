from preprocess_data import compute_dwell_time_cdf
import matplotlib.pyplot as plt

def visualize_cdf_example(bucketed_dwell_times, location_name):
    # Compute CDF using the imported function
    dwell_times, cdf = compute_dwell_time_cdf(bucketed_dwell_times)

    # Visualize the result
    plt.figure(figsize=(8, 5))
    plt.step(dwell_times, cdf, where='post', label='CDF', color='blue', linewidth=2)
    plt.scatter(dwell_times, cdf, color='red', label='Points', zorder=5)
    plt.xlabel("Dwell Time (hours)")
    plt.ylabel("CDF Value")
    plt.title(f"Dwell Time CDF for {location_name}")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

example_bucketed_dwell_times = {
    '<5': 20,
    '5-10': 30,
    '11-20': 50,
    '21-60': 100,
    '61-120': 200,
    '121-240': 150,
    '>240': 50
}

visualize_cdf_example(example_bucketed_dwell_times, "Example Location")
