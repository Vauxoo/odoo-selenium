#!/bin/bash

coverage run /usr/bin/odoo -i test_selenium --test-tags /test_selenium --workers=0 --stop-after-init
coverage report --show-missing
coverage html
coverage xml
