# SPOCK 🖖

**Stability of Planetary Orbital Configurations Klassifier**

[![image](https://badge.fury.io/py/spock.svg)](https://badge.fury.io/py/spock)
[![image](https://travis-ci.com/dtamayo/spock.svg?branch=master)](https://travis-ci.com/dtamayo/spock)
[![image](http://img.shields.io/badge/license-GPL-green.svg?style=flat)](https://github.com/dtamayo/spock/blob/master/LICENSE)
[![image](https://img.shields.io/badge/launch-binder-ff69b4.svg?style=flat)](http://mybinder.org/repo/dtamayo/spock)
[![image](http://img.shields.io/badge/arXiv-2007.06521-green.svg?style=flat)](http://arxiv.org/abs/2007.06521)
[![image](http://img.shields.io/badge/arXiv-2101.04117-green.svg?style=flat)](https://arxiv.org/abs/2101.04117)

![image](https://raw.githubusercontent.com/dtamayo/spock/master/paper_plots/spockpr.jpg)

[Documentation](https://spock-instability.readthedocs.io/en/latest/)

# Quickstart

Let's predict the probability that a given 3-planet system is stable
past 1 billion orbits with the XGBoost-based classifier, and then compute its
median expected instability time with the deep regressor:

```python
import rebound
from spock import FeatureClassifier, DeepRegressor
feature_model = FeatureClassifier()
deep_model = DeepRegressor()

sim = rebound.Simulation()
sim.add(m=1.)
sim.add(m=1.e-5, P=1., e=0.03, l=0.3)
sim.add(m=1.e-5, P=1.2, e=0.03, l=2.8)
sim.add(m=1.e-5, P=1.5, e=0.03, l=-0.5)
sim.move_to_com()

# XGBoost-based classifier
print(feature_model.predict_stable(sim))
# >>> 0.011505529

# Bayesian neural net-based regressor
median, lower, upper = deep_model.predict_instability_time(sim, samples=10000)
print(int(median))
# >>> 419759

# This time in the time units you used in setting up the REBOUND Simulation above
# Since we set the innermost planet orbit to unity, this corresponds to 419759 innermost planet orbits
```

# Examples

[Colab tutorial](https://colab.research.google.com/drive/1R3NrPmtI5DZFq_VZtv8gowINBrXM85Zv?usp=sharing)
for the deep regressor.

The example notebooks contain many additional examples:
[jupyter\_examples/](https://github.com/dtamayo/spock/tree/master/jupyter_examples).

# Installation

SPOCK is compatible with both Linux and Mac. SPOCK relies on XGBoost, which has installation issues with OpenMP on
Mac OSX. If you have problems (<https://github.com/dmlc/xgboost/issues/4477>), the easiest way is
probably to install [homebrew](brew.sh), and:

```
brew install libomp
```

The most straightforward way to avoid any version conflicts is to download the Anaconda Python distribution and make a separate conda environment.

Here we create we create a new conda environment called `spock` and install all the required dependencies
```
conda create -q --name spock -c pytorch -c conda-forge python=3.7 numpy scipy pandas scikit-learn matplotlib torchvision pytorch xgboost rebound einops jupyter pytorch-lightning ipython h5py
conda activate spock
pip install spock
```

Each time you want to use spock you will first have to activate this `spock` conda environment (google conda environments).
