# pyEconometrics

[![PyPI version](https://badge.fury.io/py/pyEconometrics.svg)](https://badge.fury.io/py/pyEconometrics)
[![Python versions](https://img.shields.io/pypi/pyversions/pyEconometrics.svg)](https://pypi.org/project/pyEconometrics/)
[![License](https://img.shields.io/github/license/brycewang-stanford/pyEconometrics.svg)](https://github.com/brycewang-stanford/pyEconometrics/blob/main/LICENSE)
[![Build Status](https://github.com/brycewang-stanford/pyEconometrics/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/brycewang-stanford/pyEconometrics/actions)
[![codecov](https://codecov.io/gh/brycewang-stanford/pyEconometrics/branch/main/graph/badge.svg)](https://codecov.io/gh/brycewang-stanford/pyEconometrics)

A comprehensive econometrics package for Python, inspired by Stata's simplicity and R's flexibility. pyEconometrics bridges the gap between user-friendly syntax and powerful econometric analysis, making advanced techniques accessible to researchers and practitioners.

## 🚀 Features

### Core Econometric Methods
- **Linear Regression**: OLS, WLS with robust standard errors
- **Instrumental Variables**: 2SLS estimation 
- **Panel Data**: Fixed Effects, Random Effects models
- **Causal Inference**: Causal Forest implementation (inspired by EconML)

### User Experience
- **Formula Interface**: Intuitive R/Stata-style syntax `"y ~ x1 + x2"`
- **Excel Export**: Professional output tables via `outreg2` (Stata-inspired)
- **Flexible API**: Both formula and matrix interfaces supported
- **Rich Output**: Detailed summary statistics and diagnostic tests

### Technical Excellence
- **Robust Implementation**: Based on proven econometric theory
- **Performance Optimized**: Efficient algorithms for large datasets
- **Well Tested**: Comprehensive test suite ensuring reliability
- **Type Hints**: Full type annotation for better development experience

## 📦 Installation

```bash
# Latest stable version
pip install pyEconometrics

# Development version
pip install git+https://github.com/brycewang-stanford/pyEconometrics.git
```

### Requirements
- Python 3.8+
- NumPy, SciPy, Pandas
- scikit-learn (for Causal Forest)
- openpyxl (for Excel export)

## 🏁 Quick Start

### Basic Regression Analysis
```python
import pandas as pd
from pyeconometrics import reg, outreg2

# Load your data
df = pd.read_csv('data.csv')

# Run OLS regression
result1 = reg('wage ~ education + experience', data=df)
print(result1.summary())

# Add control variables
result2 = reg('wage ~ education + experience + age + gender', data=df)

# Export results to Excel
outreg2([result1, result2], 'regression_results.xlsx', 
        title='Wage Regression Analysis')
```

### Instrumental Variables
```python
# 2SLS estimation
iv_result = reg('wage ~ education | mother_education + father_education', 
                data=df, method='2sls')
print(iv_result.summary())
```

### Panel Data Analysis
```python
# Fixed effects model
fe_result = reg('y ~ x1 + x2', data=df, 
                entity_col='firm_id', time_col='year', 
                method='fixed_effects')
```

### Causal Forest for Heterogeneous Treatment Effects
```python
from pyeconometrics import CausalForest

# Initialize Causal Forest
cf = CausalForest(n_estimators=100, random_state=42)

# Fit model: outcome ~ treatment | features | controls
cf.fit('income ~ job_training | age + education + experience | region + year', 
       data=df)

# Estimate individual treatment effects
individual_effects = cf.effect(df)

# Get confidence intervals
effects_ci = cf.effect_interval(df, alpha=0.05)

# Export results
cf_summary = cf.summary()
outreg2([cf_summary], 'causal_forest_results.xlsx')
```

## 📊 Advanced Usage

### Robust Standard Errors
```python
# Heteroskedasticity-robust standard errors
result = reg('y ~ x1 + x2', data=df, robust=True)

# Clustered standard errors
result = reg('y ~ x1 + x2', data=df, cluster='firm_id')
```

### Model Comparison
```python
from pyeconometrics import compare_models

models = [
    reg('y ~ x1', data=df),
    reg('y ~ x1 + x2', data=df),
    reg('y ~ x1 + x2 + x3', data=df)
]

comparison = compare_models(models)
print(comparison.summary())
```

### Custom Output Formatting
```python
outreg2(results, 'output.xlsx',
        title='Regression Results',
        add_stats={'Observations': lambda r: r.nobs,
                  'R-squared': lambda r: r.rsquared},
        decimal_places=4,
        star_levels=[0.01, 0.05, 0.1])
```

## 📚 Documentation

- **[User Guide](docs/user_guide.md)**: Comprehensive tutorials and examples
- **[API Reference](docs/api_reference.md)**: Detailed function documentation  
- **[Theory Guide](docs/theory_guide.md)**: Mathematical foundations
- **[Examples](examples/)**: Jupyter notebooks with real-world applications

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone repository
git clone https://github.com/brycewang-stanford/pyEconometrics.git
cd pyEconometrics

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by Stata's `outreg2` command for output formatting
- Causal Forest implementation based on Wager & Athey (2018)
- Built on the shoulders of NumPy, SciPy, and scikit-learn

## 📞 Contact

- **Author**: Bryce Wang
- **Email**: brycewang2018@gmail.com
- **GitHub**: [brycewang-stanford](https://github.com/brycewang-stanford)

## 📈 Citation

If you use pyEconometrics in your research, please cite:

```bibtex
@software{wang2024pyeconometrics,
  title={pyEconometrics: A Comprehensive Econometrics Package for Python},
  author={Wang, Bryce},
  year={2024},
  url={https://github.com/brycewang-stanford/pyEconometrics},
  version={0.1.0}
}
```
