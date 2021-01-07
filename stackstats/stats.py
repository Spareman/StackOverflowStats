import argparse
import sys
import requests
import json
from datetime import datetime
from collections import Counter

DATE_FORMAT = "%Y%m%d %H:%M:%S"
BASE_URL = "https://api.stackexchange.com/2.2"


def _to_json(out):
    """Function to translate output to json."""
    return json.dumps(out)


def _to_csv(out):
    """Function to translate output to csv."""
    output_csv = ""
    for pair in out.items():
        key = pair[0]
        value = pair[1]
        if type(value) == dict:
            output_csv += f"{key}"
            for k, v in value.items():
                output_csv += f",{k},{v}\n"
        else:
            output_csv += f"{key},{value}\n"
    output_csv = output_csv[:-1]
    return output_csv


def _to_html(out):
    """Function to translate output to html."""
    output_html = "<table border=\"1\">\n"
    for pair in out.items():
        key = pair[0]
        value = pair[1]
        if type(value) == dict:
            output_html += f"<tr> <th>{key}</th>\n"
            output_html += f" <td><table>\n"
            for k, v in value.items():
                output_html += f"<tr><th>{k}</th> <td>{v}</td></tr>\n"
            output_html += f"</table></td></tr>\n"
        else:
            output_html += f"<tr> <th>{key}</th> <td>{value}</td> </tr>\n"
    output_html += "</table>"

    return output_html


def to_timestamp(date):
    """Function to transform datetime to UNIX timestamp"""
    date = datetime.strptime(date, DATE_FORMAT)
    timestamp = int(datetime.timestamp(date))
    return timestamp


def create_parser():
    """Create the parser object to parse command line arguments."""

    parser = argparse.ArgumentParser(description="A simple command line application that retrieves data from "
                                                 "StackOverflow and calculates some statistics on them.")
    parser.add_argument("--since", metavar="SINCE_DATE", type=str, required=True,
                        help="The starting date/time of the range. Expected format: \"YYYYMMDD HH:mm:SS\"")
    parser.add_argument("--until", metavar="UNTIL_DATE", type=str, required=True,
                        help="The end date/time of the range. Expected format: \"YYYYMMDD HH:mm:SS\"")
    parser.add_argument("--output-format", metavar="FORMAT", choices=["json", "csv", "html"],
                        help="The chosen format of the output. Options: json, csv, html. Default: json")

    return parser


def retrieve_answers(since, until):
    """Retrieve answers from StackExchange API during datetime range specified by since and until arguments."""

    # Request answer data for specified date/time range in descending votes order.
    page = 1
    response = requests.get(
        BASE_URL + f"/answers?page={page}&fromdate={since}&todate={until}"
                   f"&order=desc&sort=votes&site=stackoverflow")

    # List to store all retrieved answers.
    answers = []
    if not response.ok:
        return answers
    else:
        response_json = response.json()
        answers += response_json["items"]

        # Request again next pages, until there are no more to be retrieved.
        while response_json["has_more"] and response.ok:
            page += 1
            response = requests.get(
                BASE_URL + f"/answers?page={page}&fromdate={since}&todate={until}"
                           f"&order=desc&sort=votes&site=stackoverflow")
            if not response.ok:
                return answers
            else:
                response_json = response.json()
                answers += response_json["items"]
    return answers


def retrieve_comment_counts(ids):
    """Retrieve comments from StackExchange API for the specifiers ids and return a comment counter for each id."""

    # List to store the comment counters per answer.
    comments_count = []
    for iid in ids:

        # Request comments for each top answer.
        response = requests.get(BASE_URL + f"/answers/{iid}/comments?order=desc&sort=creation&site=stackoverflow")
        if not response.ok:
            return comments_count
        else:
            response_json = response.json()
            # Store the number of comments in the list
            comments_count.append(len(response_json["items"]))
    return comments_count


# Dictionary to choose transform method for output
_transform_to = {
    "json": _to_json,
    "csv": _to_csv,
    "html": _to_html
}


def main():
    """
    A command line application that retrieved data from StackOverflow and calculates statistics.
    Command line arguments:
        - since: Starting date/time of range. Format: YYYYMMDD HH:mm:SS
        - until: End date/time of range. Format: YYYYMMDD HH:mm:SS
        - output-format(optional): Choose output format. Options: ["json", "csv", "html"]. Default: json

    :rtype: str (Based on the output-format option)
    """

    # Parse user arguments.
    parser = create_parser()
    args = parser.parse_args()

    # Convert date/time input to UNIX timestamp.
    try:
        date_since = to_timestamp(args.since)
        date_until = to_timestamp(args.until)
    except ValueError:
        return parser.print_help()

    # Set output format based on user's option, or json if no option passed.
    output_format = args.output_format
    output_format = "json" if not output_format else output_format

    answers = retrieve_answers(date_since, date_until)

    # Filter accepted answers.
    accepted = list(filter(lambda x: x["is_accepted"], answers))
    scores_accepted = [ans["score"] for ans in accepted]

    # Divide the accepted answers' scores sum with the total accepted answers to calculate the average score.
    try:
        avg_score_accepted = sum(scores_accepted)/len(scores_accepted)
    except ZeroDivisionError:
        avg_score_accepted = 0

    questions = [ans["question_id"] for ans in answers]

    # Count answers for each question.
    questions_answer_counters = Counter(questions)

    # Divide questions' answer counters sum with total questions to calculate the average counter.
    try:
        avg_question_answer_counter = sum(questions_answer_counters.values())/len(questions_answer_counters)
    except ZeroDivisionError:
        avg_question_answer_counter = 0

    # Answers are in descending votes order, so the first are the top.
    top_10_answers = answers[:10]
    ids_top_10_answers = [ans["answer_id"] for ans in top_10_answers]

    comments_count = retrieve_comment_counts(ids_top_10_answers)

    # Create output.
    output = {
        "total_accepted_answers": len(accepted),
        "accepted_answers_average_score": round(avg_score_accepted, ndigits=2),
        "average_answers_per_question": round(avg_question_answer_counter, ndigits=2),
        "top_ten_answers_comment_count": dict(list(zip(ids_top_10_answers, comments_count)))
    }

    # Return the output in the requested format.
    return print(_transform_to[output_format](output))


if __name__ == "__main__":
    main()
