"""
Unified results class for all econometric models
"""

from typing import Dict, Any, Optional, List, Union
import pandas as pd
import numpy as np
from scipy import stats


class EconometricResults:
    """
    Unified results class for econometric models
    
    This class provides a consistent interface for accessing results
    from different econometric estimators, similar to R's broom package.
    """
    
    def __init__(
        self,
        params: pd.Series,
        std_errors: pd.Series,
        model_info: Dict[str, Any],
        data_info: Optional[Dict[str, Any]] = None,
        diagnostics: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize results object
        
        Parameters
        ----------
        params : pd.Series
            Parameter estimates with variable names as index
        std_errors : pd.Series
            Standard errors with variable names as index
        model_info : Dict[str, Any]
            Model metadata (model type, estimation method, etc.)
        data_info : Dict[str, Any], optional
            Data metadata (sample size, variable names, etc.)
        diagnostics : Dict[str, Any], optional
            Model diagnostics (R-squared, F-statistics, etc.)
        """
        self.params = params
        self.std_errors = std_errors
        self.model_info = model_info
        self.data_info = data_info or {}
        self.diagnostics = diagnostics or {}
        
        # Compute derived statistics
        self._compute_statistics()
    
    def _compute_statistics(self):
        """Compute t-statistics, p-values, and confidence intervals"""
        self.tvalues = self.params / self.std_errors
        self.pvalues = 2 * (1 - stats.t.cdf(np.abs(self.tvalues), 
                                           self.data_info.get('df_resid', np.inf)))
        
        # 95% confidence intervals by default
        alpha = 0.05
        t_crit = stats.t.ppf(1 - alpha/2, self.data_info.get('df_resid', np.inf))
        self.conf_int_lower = self.params - t_crit * self.std_errors
        self.conf_int_upper = self.params + t_crit * self.std_errors
    
    def summary(self, alpha: float = 0.05) -> str:
        """
        Generate a summary table of results
        
        Parameters
        ----------
        alpha : float, default 0.05
            Significance level for confidence intervals
            
        Returns
        -------
        str
            Formatted summary table
        """
        # Create coefficients table
        coef_table = pd.DataFrame({
            'Coefficient': self.params,
            'Std. Error': self.std_errors,
            't-statistic': self.tvalues,
            'P>|t|': self.pvalues,
            f'[{alpha/2:.3f}': self.conf_int_lower,
            f'{1-alpha/2:.3f}]': self.conf_int_upper
        })
        
        # Format the output
        output = []
        output.append("=" * 80)
        output.append(f"Model: {self.model_info.get('model_type', 'Unknown')}")
        output.append(f"Method: {self.model_info.get('method', 'Unknown')}")
        if 'dependent_var' in self.data_info:
            output.append(f"Dependent Variable: {self.data_info['dependent_var']}")
        output.append("=" * 80)
        
        # Add coefficient table
        output.append(coef_table.to_string(float_format='%.4f'))
        
        # Add model diagnostics
        if self.diagnostics:
            output.append("")
            output.append("Model Diagnostics:")
            output.append("-" * 20)
            for key, value in self.diagnostics.items():
                if isinstance(value, (int, float)):
                    output.append(f"{key:20s}: {value:.4f}")
                else:
                    output.append(f"{key:20s}: {value}")
        
        output.append("=" * 80)
        return "\n".join(output)
    
    def conf_int(self, alpha: float = 0.05) -> pd.DataFrame:
        """
        Return confidence intervals for parameters
        
        Parameters
        ----------
        alpha : float, default 0.05
            Significance level
            
        Returns
        -------
        pd.DataFrame
            Confidence intervals
        """
        t_crit = stats.t.ppf(1 - alpha/2, self.data_info.get('df_resid', np.inf))
        lower = self.params - t_crit * self.std_errors
        upper = self.params + t_crit * self.std_errors
        
        return pd.DataFrame({
            f'{alpha/2:.3f}': lower,
            f'{1-alpha/2:.3f}': upper
        }, index=self.params.index)
    
    def predict(self, data: Optional[pd.DataFrame] = None) -> np.ndarray:
        """
        Generate predictions (to be implemented by specific models)
        
        Parameters
        ----------
        data : pd.DataFrame, optional
            Data for prediction
            
        Returns
        -------
        np.ndarray
            Predicted values
        """
        raise NotImplementedError("Prediction method not implemented for this model")
    
    def residuals(self) -> Optional[np.ndarray]:
        """
        Return model residuals if available
        
        Returns
        -------
        np.ndarray or None
            Residuals
        """
        return self.data_info.get('residuals')
    
    def fitted_values(self) -> Optional[np.ndarray]:
        """
        Return fitted values if available
        
        Returns
        -------
        np.ndarray or None
            Fitted values
        """
        return self.data_info.get('fitted_values')
    
    def __repr__(self) -> str:
        """String representation of results"""
        model_type = self.model_info.get('model_type', 'Unknown')
        n_params = len(self.params)
        n_obs = self.data_info.get('nobs', 'Unknown')
        return f"<EconometricResults: {model_type}, {n_params} parameters, {n_obs} observations>"
