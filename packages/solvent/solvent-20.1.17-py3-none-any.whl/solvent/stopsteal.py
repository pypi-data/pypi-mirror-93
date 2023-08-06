import time

import log
import pomace


URL = "https://action.greene2020.com/stop-the-steal-rd/"


def main():
    submits = 0
    errors = 0

    while errors < 10:
        page = pomace.visit(URL)

        person = pomace.fake.person

        page.fill_full_name(person.first_name + " " + person.last_name)
        page.fill_email(person.email)
        page.fill_zip_code(person.zip_code)
        page.fill_phone_number(person.phone_number)

        result = page.click_stop_the_steal()

        if "If you'd like to enter to win" in result:
            submits += 1
            errors = 0
            log.info(f"Submission count: {submits}")
        else:
            errors += 1
            log.info(f"Error count: {errors}")
