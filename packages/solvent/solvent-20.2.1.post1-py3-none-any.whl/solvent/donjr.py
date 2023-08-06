import log
import pomace

import random
import time


def main():
    pomace.freeze()
    attempted = completed = failed = 0
    while failed < 10:
        attempted += 1
        person = pomace.fake.person

        log.info(f"Beginning iteration as {person}")
        page = pomace.visit("http://donjr.com")
        page.fill_email_address(person.email_address)
        page = page.click_submit(delay=0.5)

        log.info("Browsing books")
        page = page.click_shop_all()

        log.info("Choosing book")
        page.click_book()

        log.info("Buying book")
        page = page.click_buy_it_now(delay=2, wait=5)

        if "Contact information" not in page:
            log.info("Resetting checkout form")
            page = page.click_change()

        log.info("Checking out")
        page.fill_email(person.email)

        time.sleep(1)
        modal = pomace.shared.browser.find_by_id("shopify-pay-modal")
        if modal and modal.visible:
            log.warn("Handling payment modal")
            page.type_shift_tab()
            page.type_enter()

        page.fill_first_name(person.first_name)
        page.fill_last_name(person.last_name)
        page.fill_address(person.address)
        page.type_enter()

        field = page.fill_zip_code.locator.find()
        if field and field.value:
            page = page.click_continue_to_shipping(delay=1, wait=5)
        else:
            log.error("Incomplete address detected")
            failed += 1
            continue

        log.info("Continuing to payment")
        page = page.click_continue_to_payment()

        log.info("Completing order")
        page.click_paypal()
        page = page.click_complete_order()

        if "paypal" in page.url:
            completed += 1
            failed = 0
        else:
            failed += 1

        log.info(f"Iterations: {attempted=} {completed=} {failed=}")
