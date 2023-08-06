# Apache Airflow Provider for Great Expectations

**Experimental library as of February 2021**

An Airflow operator for [Great Expectations](greatexpectations.io), a Python library for testing and validating data.

## Installation

Pre-requisites: An environment running `great_expectations` and `apache-airflow`, of course.

```
pip install airflow-provider-great-expectations
```

In order to run the `BigQueryOperator`, you will also need to install the relevant dependencies: `pybigquery` and `apache-airflow-providers-google`


## Modules

[Great Expectations Operator](./great_expectations_provider/operators/great_expectations.py): A base operator for Great Expectations. Import into your DAG via: 

```
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
```


[Great Expectations BigQuery Operator](./great_expectations_provider/operators/great_expectations_biquery.py): An operator for Great Expectations that provides some pre-set parameters for a BigQuery Datasource and Expectation, Validation, and Data Docs stores in Google Cloud Storage. The operator can also be configured to send email on validation failure. See the docstrings in the class for more configuration options. Import into your DAG via: 

```
from great_expectations_provider.operators.great_expectations_bigquery import GreatExpectationsBigQueryOperator
```

## Examples

See the [**examples**](./great_expectations_provider/examples) directory for an example DAG with some sample tasks that demonstrate operator functionality. The example DAG file contains a comment with instructions on how to run the examples.

**This operator is in very early stages of development! Feel free to submit issues, PRs, or ping the current author (Sam Bail) in the [Great Expectations Slack](http://greatexpectations.io/slack) for feedback. Thanks to [Pete DeJoy](https://github.com/petedejoy) and the [Astronomer.io](https://www.astronomer.io/) team for the support.
