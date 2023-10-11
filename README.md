# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/caprexy/kemono-watcher/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------ | -------: | -------: | ------: | --------: |
| constants.py                        |        5 |        0 |    100% |           |
| input\_panel/\_\_init\_\_.py        |        0 |        0 |    100% |           |
| input\_panel/status\_helper.py      |       21 |       12 |     43% |15, 24-27, 32, 45, 55-58, 63 |
| models/\_\_init\_\_.py              |        0 |        0 |    100% |           |
| models/database\_model.py           |      176 |       18 |     90% |33, 71, 108-111, 153, 167, 178-182, 235-237, 320, 324 |
| models/user\_model.py               |       24 |        2 |     92% |    24, 27 |
| output\_panel/\_\_init\_\_.py       |        0 |        0 |    100% |           |
| output\_panel/output\_controller.py |       60 |        1 |     98% |        71 |
| testing/\_\_init\_\_.py             |        0 |        0 |    100% |           |
| testing/local\_constants.py         |       25 |        0 |    100% |           |
| testing/test\_database.py           |      133 |        2 |     98% |  102, 239 |
| testing/test\_output\_controller.py |       78 |        0 |    100% |           |
| testing/test\_user.py               |       26 |        0 |    100% |           |
|                           **TOTAL** |  **548** |   **35** | **94%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/caprexy/kemono-watcher/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/caprexy/kemono-watcher/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/caprexy/kemono-watcher/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/caprexy/kemono-watcher/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fcaprexy%2Fkemono-watcher%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/caprexy/kemono-watcher/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.