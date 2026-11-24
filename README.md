# Machine Learning Analysis of the Effects of Tyre Characteristics and Weather Conditions on Formula 1 Performance

## Project Overview

This repository supports a BSc Honours in Information Technology research dissertation at Eduvos, South Africa.

The research investigates the relationships between tyre characteristics, weather conditions and Formula 1 lap-time performance using statistical analysis and machine learning techniques.

Historical Formula 1 race data from the 2023–2025 seasons were obtained through the OpenF1 API.

## Research Objectives

- Examine the relationship between tyre characteristics and Formula 1 lap-time performance.
- Investigate the relationship between weather conditions and lap-time performance.
- Develop machine learning models using tyre and weather information.
- Evaluate and compare the predictive performance of the selected machine learning models.

## Dataset Overview

The model-ready dataset consists of:

- 74,508 lap observations
- 70 Formula 1 races
- Three racing seasons (2023–2025)
- Five tyre compounds
- 74,489 observations with complete weather information

Data source: [OpenF1 API](https://openf1.org/docs/)

## Research Methodology

The research incorporates:

- Data collection, cleaning and integration
- Descriptive statistical analysis
- Ordinary Least Squares (OLS) regression
- Race fixed effects and race-clustered standard errors
- Joint Wald hypothesis testing
- Sensitivity analysis
- Five-fold race-grouped cross-validation
- Machine learning model evaluation

## Machine Learning Models

The following regression models were evaluated:

- Linear Regression (LR)
- Random Forest (RF)
- Gradient Boosting (GB)

Mean Absolute Error (MAE), measured in seconds, was used as the principal predictive performance metric.

## Key Research Findings

- Tyre characteristics demonstrated statistically significant joint associations with lap duration across all three regression specifications.
- Weather-related statistical significance depended on the sample restrictions applied.
- Linear Regression using tyre and circuit information achieved the lowest mean cross-validation MAE of 5.71 seconds.
- Adding weather variables did not improve predictive accuracy in the evaluated Linear Regression and Gradient Boosting configurations.
- Prediction errors were higher for opening laps and circuits absent from the corresponding training folds.

These findings distinguish statistical association from predictive usefulness and do not establish causal relationships.

## Machine Learning Performance

| Model | Feature Configuration | Mean CV MAE (seconds) |
|---|---|---:|
| Linear Regression | Tyre and circuit | 5.71 |
| Gradient Boosting | Tyre and circuit | 6.40 |
| Random Forest | Tyre and circuit | 7.69 |
| Linear Regression | Tyre, weather and circuit | 6.14 |
| Gradient Boosting | Tyre, weather and circuit | 7.24 |

## Lap Analysis & Prediction Dashboard (LAPD)

The Lap Analysis & Prediction Dashboard (LAPD) is an interactive research prototype developed using Python and Streamlit.

The dashboard supports:

- Historical Formula 1 data exploration
- Tyre compound analysis
- Lap-time comparisons
- Weather condition exploration
- Machine learning model performance comparisons
- Interactive lap-duration prediction

The prediction component uses a trained Linear Regression pipeline with circuit, tyre compound and estimated tyre age as inputs.

Weather variables are available for exploratory analysis but are not inputs to the saved prediction model.

LAPD is an academic research prototype and is not intended for production-level race strategy optimisation.

## Technologies Used

- Python
- Jupyter Notebook
- pandas
- NumPy
- scikit-learn
- statsmodels
- Matplotlib
- Streamlit
- Joblib
- OpenF1 API

## Research Limitations

- Estimated tyre age is a proxy for tyre usage rather than a direct measurement of physical degradation.
- Weather observations approximate conditions near the recorded lap timestamp.
- Wet-weather and WET tyre observations are underrepresented.
- Driver, vehicle, fuel, traffic and race-interruption factors are not comprehensively represented.
- The separate 14-race exploratory evaluation subset was used during model development and does not constitute an untouched final test set.

## Reproducibility

This repository is being prepared to support research transparency and reproducibility through the inclusion of research notebooks, data preparation procedures, model evaluation outputs and the LAPD prototype.

Project structure, dependency requirements and execution instructions will be updated as the repository is populated.

## Academic Purpose

This project was developed as part of a BSc Honours in Information Technology dissertation at Eduvos.

The research is intended for academic and educational purposes.

## Acknowledgements

Acknowledgement is extended to OpenF1 for providing access to historical Formula 1 data.

This project is independent and is not officially affiliated with Formula 1 or the FIA.
