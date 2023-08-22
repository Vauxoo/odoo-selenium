# odoo-selenium
This package provides utilities that make it easy to quickly write and develop Odoo tests using Selenium.

## Usage
To boostrap Selenium you can use `SeleniumMixin`, it contains the following two methods:

* `start_selenium`
* `stop_selenium`

Each method should be called in the `setUp` and `tearDown` of your suite respectively.
Here is a simple example that demonstrates it:

```python
from selenium.webdriver.common.by import By

from odoo.tests import HttpCase, tagged

from odoo_selenium import SeleniumMixin


@tagged("-at_install", "post_install")
class TestSelenium(SeleniumMixin, HttpCase):
    def setUp(self):
        super().setUp()
        # other initialization code
        self.start_selenium()

    def tearDown(self):
        super().tearDown()
        # other teardown code, generally not required
        self.stop_selenium()

    def test_login_page(self):
        self.driver.get(f"{self.base_url()}/web/login")  # base_url() does not exist in 14.0
        email_input = self.driver.find_element(By.ID, "login")

        self.assertEqual("Email", email_input.get_attribute("placeholder"))
```

Note three important things:

* Selenium tests must inherit Odoo's HttpCase and as such, be run only after installation (`post_install`)
* `SeleniumMixin` must come first in the inheritance chain
* `start_selenium` and `stop_selenium` should be called last, after all your custom initialization and teardown code

## Development
If you wish to contribute, it is easy to set up a development environment. Being a simple library meant to be
integrated with Odoo, all that is needed is to clone the source code and start hacking away. Below you can find
a simple overview of the project and its structure.

### Project Structure
The project is divided in three sections, the library itself, tests and the supporting Docker files to run the test
suite.

#### src
All library code should reside inside this folder. This is the code that will be imported by users on their Odoo tests.

#### tests_odoo
These are Odoo modules and form part of the test suite. Because this package is meant to be used as a utility library
for Odoo, testing does not really make sense without Odoo. These modules only provide tests to be run in Odoo and verify
the library integrates well and does not randomly explode.

### Running the Test Suite
Since an Odoo instance is required to run the test suite, the project relies on Docker to provide this instance and
other required infrastructure, like a PostgreSQL server. Running on a Docker container also means the project itself
is installed as users would, meaning this environment is as close to possible as the 'real world'.

To run the test suite you can simply issue the following command:

```shell
docker compose -f .docker/chrome-compose.yaml up --build --abort-on-container-exit --force-recreate
```

Make sure the working directory when running said command is the repository's root. Docker automatically checks for
changed files so nothing needs to be performed on your part (other than running the command above), this makes testing
iterative changes really easy and quick.

By default, the test suite runs against the newest Odoo version. To run the test suite with a different Odoo version it
is as easy as specifying it:

```shell
ODOO_VERSION=15 docker compose -f .docker/chrome-compose.yaml up --build --abort-on-container-exit --force-recreate
```

The command above will run tests against Odoo 15.0. Images are tagged as: `vauxoo/odoo-selenium:${ODOO_VERSION}` so
if you wanted to inspect the image built above, you can simply use:

```shell
docker run -it --rm --entrypoint=/bin/bash vauxoo/odoo-selenium:15
```

**Note: If your tests fail, and you see old code being referenced, you are using an old image! That's why
`--force-recreate` is used.**
