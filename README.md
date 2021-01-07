# Stackstats

A simple command line application that retrieves data from StackOverflow and calculates some statistics
on them.

# Installation

## Using pip

```
$ cd stackstats-1.0
$ pip install .
```

## Running setup file
```
$ cd stackstats-1.0
$ python setup.py install
```

# Usage

## Running command
```
$ stats --since SINCE_DATE --until UNTIL_DATE [--output-format FORMAT]
```
The application expects two date arguments in order to choose the date/time range to retrieve the 
answer data for, as well as one optional to specify the output format. The default output format is *JSON*.
>*Expected date/time format*: **YYYYMMDD HH:mm:SS**

>*Available output format options*: **json, csv and html**

## Output

The application calculates the following statistics:
* *Total accepted answers*
* *Accepted answers' average score*
* *Average answer count per question*
* *Comment count for the top 10 answers*

# Running tests
```
$ cd stackstats-1.0
$ python setup.py test
```

# Example

```
$ stats --since '20200602 10:00:00' --until '20200602 10:05:00'
{"total_accepted_answers": 15, 
"accepted_answers_average_score": 1.07, 
"average_answers_per_question": 1.03, 
"top_ten_answers_comment_count": {"62146559": 7, "62146540": 2, "62146542": 0, "62146565": 3, "62146574": 0, "62146501": 0, "62146505": 3, "62146529": 0, "6214
6543": 1, "62146546": 2}}

```