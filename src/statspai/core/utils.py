"""
Utility functions for formula parsing and data processing
"""

from typing import Tuple, List, Optional, Dict, Any
import pandas as pd
import numpy as np
import re
from patsy import dmatrices, dmatrix


def parse_formula(formula: str) -> Dict[str, Any]:
    """
    Parse econometric formula into components
    
    Supports formulas like:
    - "y ~ x1 + x2"  (basic regression)
    - "y ~ x1 + x2 | fe1 + fe2"  (fixed effects)
    - "y ~ (x1 ~ z1 + z2) + x3"  (instrumental variables)
    
    Parameters
    ----------
    formula : str
        Formula string
        
    Returns
    -------
    Dict[str, Any]
        Parsed formula components
    """
    result = {
        'dependent': None,
        'exogenous': [],
        'endogenous': [],
        'instruments': [],
        'fixed_effects': [],
        'has_constant': True
    }
    
    # Split by | for fixed effects
    if '|' in formula:
        main_formula, fe_part = formula.split('|', 1)
        result['fixed_effects'] = [var.strip() for var in fe_part.split('+')]
    else:
        main_formula = formula
    
    # Split dependent and independent variables
    if '~' not in main_formula:
        raise ValueError("Formula must contain '~' to separate dependent and independent variables")
    
    dependent_part, independent_part = main_formula.split('~', 1)
    result['dependent'] = dependent_part.strip()
    
    # Parse instrumental variables (in parentheses)
    iv_pattern = r'\(([^)]+)\)'
    iv_matches = re.findall(iv_pattern, independent_part)
    
    if iv_matches:
        for iv_spec in iv_matches:
            if '~' in iv_spec:
                endog, instruments = iv_spec.split('~', 1)
                result['endogenous'].extend([var.strip() for var in endog.split('+')])
                result['instruments'].extend([var.strip() for var in instruments.split('+')])
            else:
                result['exogenous'].extend([var.strip() for var in iv_spec.split('+')])
        
        # Remove IV specifications from independent part
        independent_part = re.sub(iv_pattern, '', independent_part)
    
    # Parse remaining exogenous variables
    remaining_vars = [var.strip() for var in independent_part.split('+') if var.strip()]
    result['exogenous'].extend(remaining_vars)
    
    # Check for constant term
    if '-1' in result['exogenous'] or '0' in result['exogenous']:
        result['has_constant'] = False
        result['exogenous'] = [var for var in result['exogenous'] if var not in ['-1', '0']]
    
    return result


def create_design_matrices(
    formula: str, 
    data: pd.DataFrame,
    return_type: str = 'dataframe'
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Create design matrices from formula and data
    
    Parameters
    ----------
    formula : str
        Regression formula
    data : pd.DataFrame
        Input data
    return_type : str, default 'dataframe'
        Return type ('dataframe' or 'array')
        
    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame]
        (y, X) matrices
    """
    try:
        y, X = dmatrices(formula, data, return_type=return_type)
        return y, X
    except Exception as e:
        # Fallback to manual parsing if patsy fails
        parsed = parse_formula(formula)
        
        y = data[parsed['dependent']].values
        if return_type == 'dataframe':
            y = pd.DataFrame(y, columns=[parsed['dependent']], index=data.index)
        
        X_cols = parsed['exogenous'].copy()
        if parsed['has_constant']:
            X_cols = ['Intercept'] + X_cols
        
        if parsed['has_constant']:
            X = np.column_stack([np.ones(len(data))] + 
                               [data[col].values for col in parsed['exogenous']])
        else:
            X = np.column_stack([data[col].values for col in parsed['exogenous']])
        
        if return_type == 'dataframe':
            X = pd.DataFrame(X, columns=X_cols, index=data.index)
        
        return y, X


def prepare_data(
    data: pd.DataFrame,
    dependent: str,
    independent: List[str],
    weights: Optional[str] = None,
    subset: Optional[pd.Series] = None
) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]:
    """
    Prepare data for econometric estimation
    
    Parameters
    ----------
    data : pd.DataFrame
        Input data
    dependent : str
        Dependent variable name
    independent : List[str]
        Independent variable names
    weights : str, optional
        Weight variable name
    subset : pd.Series, optional
        Boolean series for subsetting data
        
    Returns
    -------
    Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]
        (y, X, weights) arrays
    """
    # Apply subset if provided
    if subset is not None:
        data = data[subset].copy()
    
    # Drop missing values
    all_vars = [dependent] + independent
    if weights:
        all_vars.append(weights)
    
    data_clean = data[all_vars].dropna()
    
    # Extract arrays
    y = data_clean[dependent].values
    X = data_clean[independent].values
    w = data_clean[weights].values if weights else None
    
    return y, X, w


def add_constant(X: np.ndarray, has_constant: bool = True) -> np.ndarray:
    """
    Add constant term to design matrix
    
    Parameters
    ----------
    X : np.ndarray
        Design matrix
    has_constant : bool, default True
        Whether to add constant
        
    Returns
    -------
    np.ndarray
        Design matrix with constant if requested
    """
    if has_constant:
        return np.column_stack([np.ones(X.shape[0]), X])
    return X


def get_variable_names(
    formula: str,
    data: pd.DataFrame,
    include_constant: bool = True
) -> List[str]:
    """
    Get variable names from formula
    
    Parameters
    ----------
    formula : str
        Regression formula
    data : pd.DataFrame
        Input data
    include_constant : bool, default True
        Whether to include constant in names
        
    Returns
    -------
    List[str]
        Variable names
    """
    parsed = parse_formula(formula)
    
    names = []
    if include_constant and parsed['has_constant']:
        names.append('const')
    
    names.extend(parsed['exogenous'])
    
    return names
