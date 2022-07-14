from flask import Flask
from flask import request
from random import randrange
import os

app = Flask(__name__)

def get_numbers(threshold, range_to):

    numbers = []
    test = True
    while threshold != 0:
        get_number = randrange(1, range_to + 1)
        if get_number not in numbers or len(numbers) == 0:
            numbers.append(get_number)
            threshold -= 1
    return set(sorted(numbers))


def try_match(attempt, random_choice, my_input_sorted):

    if random_choice == my_input_sorted:
        is_not_success = False
    else:
        is_not_success = True

    return attempt, is_not_success


def get_parially_results(partially_results, random_choice, my_input_sorted):

    prefix = " times matched."
    result = f"{len(random_choice & my_input_sorted)}{prefix}"

    if result not in partially_results:
        partially_results[result] = 1
    else:
        partially_results[result] = partially_results[result] + 1

    return partially_results
  
def run_app(input_value):

    range_to = 49
    my_input = input_value.split(",")
    my_input = [
        int(number)
        for number in my_input
        if int(number) > 0 and int(number) <= range_to
    ]

    is_not_success = True
    attempt = 0
    my_input_sorted = set(sorted(my_input))
    len_my_input = len(my_input_sorted)
    partially_results = dict()

    while is_not_success:
        random_choice = get_numbers(len_my_input, range_to)
        attempt, is_not_success = try_match(attempt, random_choice, my_input_sorted)
        partially_results = get_parially_results(
            partially_results, random_choice, my_input_sorted
        )
        attempt += 1

    return f"""Number of attempts: {attempt}.
                <br><br>Detailed information about partially matched before you win:
                <br>{"<br>".join([str(i)for i in partially_results.items()])})"""

@app.route("/")
def index():

    your_numbers = request.args.get("your_numbers", "")

    if your_numbers:
        your_numbers = run_app(your_numbers)
    else:
        your_numbers = ""
    return (
        """<form action="" method="get">
                Your numbers: <input type="text" name="your_numbers">
                <input type="submit" value="Examine your happiness, numbers separated by comma">
            </form>"""
        + your_numbers
    )


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    
