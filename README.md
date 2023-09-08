# Waterloo Housing Price Predictor

## Overview

The purpose of this machine learning tool is to provide students with reliable insight regarding housing prices in Kitchener-Waterloo given factors like their inner layouts (e.g. 2B2B), amenities (e.g. gym), and locations (e.g. distance to grocery stores). The motivation behind the problem is that many Waterloo students are having difficulties renting for the school term. In particular, a recurring issue amongst the students is the landlords overcharging for rent and themselves not having an effective way to verify if the rent is fairly priced.

This project was designed and built by [Y. Cui](https://www.linkedin.com/in/yuanlong-tony-cui/), [T. Bai](https://www.linkedin.com/in/uwjackie/), [M. Lumibao](https://www.linkedin.com/in/michaellumibao/), and [L. Doria](https://www.linkedin.com/in/lukedoria/) collectively as part of the MSCI446 course in Winter 2023. The team members appreciate the guidance and advise provided by [Prof. Golab](https://uwaterloo.ca/management-sciences/profile/lgolab) and the TAs throughout the development of this project.

To gain an overview of how this project works, please take a look at the Jupyter Notebook file at `Deliverables/MSCI446.ipynb`.

## Sub-Modules

The project is split into 3 main modules, each of which has a dedicated directory:

1. Acquisition

This module includes methods of acquiring raw data (house attributes, rent price, etc.) and any other procedures used (using ChatGPT to parse data from Facebook Marketplace or Kijiji).

2. Processing

This module includes all procedures for processing the data, such as labeling, calculating the distance to campus, and distance to grocery stores.

3. Prediction

This module is the main prediction algorithm and should provide results of evaluation metrics.
