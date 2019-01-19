from runner import GenericRunner


def test_runner_class():
    url = 'https://mobil.bazos.sk/apple/'
    page_changing_string = ''
    xpath_element_definition = '//table[@class="inzeraty"]'

    runner = GenericRunner(url=url, page_changing_string=page_changing_string, xpath_element_definition=xpath_element_definition)
    runner.scrape()

if __name__ == "__main__":
    test_runner_class()