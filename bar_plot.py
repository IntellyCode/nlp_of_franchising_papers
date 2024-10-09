import matplotlib.pyplot as plt
from typing import List, Tuple
sorted_frequencies = [('franchise', 1050), ('franchisor', 746), ('franchisee', 647), ('brand', 335), ('strategy', 122), ('franchise system', 119), ('innovation', 42), ('branding', 42), ('entrepreneur', 23), ('franchise agreement', 20), ('sustainability', 19), ('territory', 17), ('foreign direct investment', 14), ('franchise network', 14), ('royalty fee', 11), ('world bank', 10), ('trademark', 10), ('corporation', 9), ('leverage', 9), ('leadership', 9), ('business development', 8), ('startup', 8), ('partnership', 8), ('data mining', 8), ('franchise operations', 8), ('signaling', 8), ('franchise development', 7), ('brand awareness', 7), ('intellectual property', 7), ('joint ventures', 6), ('strategic decision making', 6), ('externality', 6), ('initial investment', 6), ('business intelligence', 5), ('business strategy', 5), ('site selection', 4), ('business model', 4), ('franchise management', 4), ('economic growth', 4), ('corporate finance', 4), ('screening', 4), ('moral hazard', 4), ('private sector', 4), ('training program', 4), ('target market', 4), ('economic indicators', 4), ('franchise fee', 4), ('product development', 4), ('brand loyalty', 3), ('organizational culture', 3), ('globalization', 3), ('e - commerce', 3), ('strategic planning', 3), ('strategic alliances', 3), ('franchise ownership', 3), ('marketing support', 3), ('exchange rates', 3), ('options', 3), ('business plan', 2), ('insurance', 2), ('return on equity', 2), ('financial statements', 2), ('master franchise', 2), ('corporate strategy', 2), ('franchise sales', 2), ('financial management', 2), ('risk management', 2), ('venture capital', 2), ('human capital', 2), ('recession', 2), ('central bank', 2), ('patent', 2), ('market economy', 2), ('franchisee recruitment', 2), ('purchasing power', 2), ('profit margin', 2), ('brand equity', 2), ('economic efficiency', 1), ('human resources management', 1), ('financial ratios', 1), ('employee retention', 1), ('trade liberalization', 1), ('comparative advantage', 1), ('business partnerships', 1), ('unemployment rate', 1), ('benchmarking', 1), ('decision support systems', 1), ('ratio analysis', 1), ('financial analysis', 1), ('franchisee support', 1), ('franchise growth', 1), ('market failure', 1), ('diversification', 1), ('international trade', 1), ('organizational change', 1), ('oligopoly', 1), ('game theory', 1), ('franchisee training', 1), ('elasticity', 1), ('net present value', 1)]

sorted_frequencies = sorted_frequencies[0:30]


# Function to create a bar chart from a list of tuples
def create_bar_chart(data: List[Tuple[str, int]], title: str, xlabel: str, ylabel: str, figsize=(12, 8), rotation=45):
    """
    Creates and displays a bar chart from the provided data.

    Parameters:
    - data: List of tuples where each tuple is ('label', value)
    - title: Title of the bar chart
    - xlabel: Label for the X-axis
    - ylabel: Label for the Y-axis
    - figsize: Tuple specifying the figure size (width, height)
    - rotation: Angle to rotate the X-axis labels
    """
    # Check if data is not empty
    if not data:
        print("No data provided to plot.")
        return

    # Extract labels and values from the data
    labels, values = zip(*data)  # Unzips the list of tuples

    # Create a figure and axis
    plt.figure(figsize=figsize)
    ax = plt.gca()

    # Create the bar chart
    bars = ax.bar(labels, values, color='skyblue')

    # Add title and labels
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)

    # Rotate X-axis labels if necessary
    plt.xticks(rotation=rotation, ha='right')

    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.annotate('{}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

    # Adjust layout to prevent clipping of tick-labels
    plt.tight_layout()

    # Display the bar chart
    plt.show()


# Usage
create_bar_chart(
    data=sorted_frequencies,
    title='Business Financial Overview 2004',
    xlabel='Term',
    ylabel='Frequency',
    figsize=(14, 7),
    rotation=30  # Adjust rotation for better readability
)
