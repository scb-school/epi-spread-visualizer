.. EpiSpread documentation master file, created by
   sphinx-quickstart on Wed Apr  5 10:12:28 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to EpiSpread's documentation
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Installation
==================
.. code-block::

       $ pip3 install epispread

Usage - Plot a Heat Map with Slider
===================================
.. code-block::

       from epispread import EpiSpread

      EpiSpread.run_query()

      $Available files:
      $['WHO-COVID-19-global-data', 'vaccination-data', 'vaccination-metadata']
      $Which file do you want to analyze? WHO-COVID-19-global-data

      $['heat map', 'heat map w/ time slider', 'time series']
      $What type of data visualization do you want to create?heat map w/ time slider

      $['New_cases', 'Cumulative_cases', 'New_deaths', 'Cumulative_deaths']
      $Which variable do you want to plot in your heat map w/ time slider?New_cases

      $['Date_reported']
      $Which time series would you like to plot?Date_reported

      $Which date would you like to start plotting from?
      $Please format it YYYY-MM-DD, and it cannot be earlier than 2020-01-03.2020-01-03

.. image:: ../epispread/images/mappic+80.jpg
  :width: 400
  :alt: Alternative text


.. image:: ../epispread/images/mappic+180.jpg
  :width: 400
  :alt: Alternative text


.. image:: ../epispread/images/mappic+280.jpg
  :width: 400
  :alt: Alternative text