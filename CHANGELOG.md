# Changelog

All notable changes to pyEconometrics will be documented in this file.

## [0.1.0] - 2024-07-26

### Added
- **Core Regression Framework**
  - OLS (Ordinary Least Squares) regression with formula interface
  - Robust standard errors (HC0, HC1, HC2, HC3)
  - Clustered standard errors
  - Weighted Least Squares (WLS) support

- **Causal Inference Module**
  - Causal Forest implementation inspired by Wager & Athey (2018)
  - Honest estimation for unbiased treatment effect estimation
  - Bootstrap confidence intervals for treatment effects
  - Formula interface: `"outcome ~ treatment | features | controls"`

- **Output Management (outreg2)**
  - Excel export functionality similar to Stata's outreg2
  - Support for multiple regression models in single output
  - Customizable formatting options
  - Professional table layout

- **Unified API Design**
  - Consistent `reg()` function interface
  - Formula parsing: R/Stata-style syntax `"y ~ x1 + x2"`
  - Type hints throughout the codebase
  - Comprehensive documentation

### Technical Details
- Python 3.8+ support
- Dependencies: numpy, scipy, pandas, scikit-learn, openpyxl
- MIT License
- Comprehensive test suite
