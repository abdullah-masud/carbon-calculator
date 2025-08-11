# Personal Carbon Footprint Calculator

A simple, interactive **Streamlit** web app to estimate and visualize your annual CO₂ emissions from **electricity**, **natural gas**, **car travel**, and **air travel**.

The app uses credible emission factor datasets to compute **category-wise** and **total** CO₂ emissions, compares your results to **Australia's** and **global** per-capita averages, and provides recommendations for reducing your footprint.

## ✨ Features
- 📊 **Emissions breakdown** by category (kg CO₂ and tonnes CO₂e).
- 🌍 **Comparisons** to Australia and global per-capita averages.
- 💡 **Recommendations** to reduce emissions in each category.
- 📈 **Altair bar chart** for visual analysis.
- 💾 **Export results** to CSV.


## 📦 Installation

Run these commands in order to set up and run the project locally:

```bash
# 1. Clone this repository
git clone https://github.com/abdullah-masud/carbon-calculator.git
cd carbon-calculator

# 2. Create and activate a virtual environment
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\activate

# 3. Install required dependencies
pip install streamlit pandas altair

# 4. (Optional) Save dependencies to requirements.txt
pip freeze > requirements.txt

# 5. Run the Streamlit app
streamlit run carbon_calculator.py
