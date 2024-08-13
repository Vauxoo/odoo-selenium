#!/bin/bash

coverage run /usr/bin/odoo -i test_selenium --test-tags /test_selenium --workers=0 --stop-after-init
TEST_EXIT_CODE=$?

coverage report --show-missing
coverage html
coverage xml

exit "$TEST_EXIT_CODE"
