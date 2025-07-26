"""
StatsPAI: The AI-powered Statistics & Econometrics Toolkit for Python

This package provides tools for econometric analysis including:
- OLS regression with robust standard errors
- Causal Forest for heterogeneous treatment effects
- Panel data models (IV/2SLS)
- Time series analysis
- Publication-ready output formatting

Basic usage:
>>> import statspai as sp
>>> 
>>> # Traditional regression
>>> result = pe.regress("y ~ x1 + x2", data=df)
>>> result.summary()
>>> 
>>> # Causal Forest for treatment effects
>>> cf = pe.causal_forest("y ~ treatment | x1 + x2", data=df)
>>> effects = cf.effect(df[['x1', 'x2']])
>>> 
>>> # Export results
>>> pe.outreg2(result, cf, filename="results.xlsx")
"""

from .core.results import EconometricResults
from .regression.ols import regress
from .causal.causal_forest import CausalForest, causal_forest
from .output.outreg2 import OutReg2, outreg2

__version__ = "0.1.0"
__author__ = "StatsPAI Team"
__email__ = "contact@statspai.org"

__all__ = [
    "regress",
    "EconometricResults", 
    "CausalForest",
    "causal_forest",
    "OutReg2",
    "outreg2",
]

__version__ = "0.1.0"
__author__ = "Bryce Wang"
__email__ = "your.email@example.com"

from .regression.ols import regress
from .core.results import EconometricResults

__all__ = [
    "regress",
    "EconometricResults",
]
