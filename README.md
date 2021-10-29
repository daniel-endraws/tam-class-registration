# tam-class-registration
A python app to ...
Call with path to json file with parameters to search for class by (currently limited to the below)
### JSON Format
```js
{
    "class1name": {
        "txt_courseNumber": 'course number',
        "s2id_txt_instructor": 'instructor last name'
    },
    "class2name": {
        ...
    }
}
```
## Scrape Info
*Need to use selenium since site uses JS*

Grab number of students enrolled and class capacity given info and output the info

Optionally:
- Message user if there is space in the class
- Auto Enroll in the class

## Auto Enroll
Coming soon

## Dependencies
Name | Documentation | Instillation
-----|---------------|-------------
selenium | [Selenium Site](https://selenium-python.readthedocs.io/) | `pip install selenium`
pandas | [Official Docs](https://pandas.pydata.org/docs/), [One tutorial](https://www.tutorialspoint.com/python_pandas/index.htm) | `pip install pandas`


Grab your selenium driver [here](https://selenium-python.readthedocs.io/installation.html#drivers), code uses chrome driver at `/bin/chromedriver.exe`
