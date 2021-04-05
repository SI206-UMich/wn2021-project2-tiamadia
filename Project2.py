from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest

# By: Tiara Amadia & Anthony Ho // Nina Yang


def get_titles_from_search_results(filename):

    source_dir = os.path.dirname(__file__)
    fullpath = os.path.join(source_dir, filename) 
    infile = open(fullpath, 'r', encoding="UTF-8")
    soup = BeautifulSoup(infile, "html.parser")
    infile.close()

    list_tuple = []
    rows = soup.find_all("tr", itemtype="http://schema.org/Book")

    for row in rows: 
        each_book = row.find("a", class_= "bookTitle")
        book_title = each_book.find("span", itemprop = "name")
        each_author = row.find("a", class_= "authorName")
        author_name = each_author.find("span", itemprop = "name")
        list_tuple.append((book_title.text.strip(), author_name.text.strip()))
    
    return list_tuple
    
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """


def get_search_links():
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    list_links = []
    rows = soup.find_all("a", class_ = "bookTitle")

    for row in rows: 
        each_link = row.get('href', None)

        list_links.append("https://www.goodreads.com" + each_link)

    return list_links[:10]

    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """


def get_book_summary(book_url):

    chosen_url = book_url
    r = requests.get(chosen_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    book_title = soup.find("h1", id="bookTitle")
    chosen_author = soup.find("a", class_="authorName")
    author_name = chosen_author.find("span", itemprop="name")
    page_num = soup.find("span", itemprop="numberOfPages")

    return (book_title.text.strip(), author_name.text.strip(), int(page_num.text.strip().split(" ")[0]))
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

def summarize_best_books(filepath):

    infile = open(filepath, 'r', encoding='UTF-8')
    soup = BeautifulSoup(infile, 'html.parser')
    infile.close()

    chosen_book = soup.find_all(class_ = "category clearFix")
    list_category = []

    for element in chosen_book:

        chosen_category = element.find(class_="category__copy").text.strip()
        book_title = element.find("img", class_="category__winnerImage").get('alt', None)
        chosen_link = element.find("a").get('href', None)

        list_category.append((chosen_category, book_title, chosen_link))
        
    return list_category

    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    pass


def write_csv(data, filename):

    with open(filename, mode='w') as csvfile:

        data_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(["Book title", "Author Name"])
        
        for element in data:
            data_writer.writerow([element[0], element[1]])

    csvfile.close()

    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    pass


def extra_credit(filepath):

    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    search_urls = get_search_links()

    #search_urls = get_search_links()

    # call get_search_links() and save it to a static variable: search_urls


    def test_get_titles_from_search_results(self):

        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        local_variable_1 = get_titles_from_search_results("search_results.htm")

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(local_variable_1), 20)

        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(local_variable_1), list)

        # check that each item in the list is a tuple
        for item in local_variable_1:
            self.assertEqual(type(item), tuple)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(local_variable_1[0][0], "Harry Potter and the Deathly Hallows (Harry Potter, #7)")
        self.assertEqual(local_variable_1[0][1], "J.K. Rowling")

        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(local_variable_1[len(local_variable_1)-1][0], "Harry Potter: The Prequel (Harry Potter, #0.5)")
        self.assertEqual(local_variable_1[len(local_variable_1)-1][1], "J.K. Rowling")

    def test_get_search_links(self):

        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        for element in TestCases.search_urls:
            self.assertEqual(type(element), str)

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for element in TestCases.search_urls:
            self.assertTrue("goodreads.com/book/show/" in element)

    def test_get_book_summary(self):

        # for each URL in TestCases.search_urls (should be a list of tuples)
        list_tuple = []
        for element in TestCases.search_urls:
            list_tuple.append(get_book_summary(element))

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(list_tuple), 10)            

        # check that each item in the list is a tuple
        for element in list_tuple:
            self.assertEqual(type(element), tuple)

        # check that each tuple has 3 elements
        for element in list_tuple:
            self.assertEqual(len(element), 3)

        # check that the first two elements in the tuple are string
        for element in list_tuple:
            self.assertEqual(type(element[0]), str)
            self.assertEqual(type(element[1]), str)

        # check that the third element in the tuple, i.e. pages is an int
        for element in list_tuple:
            self.assertEqual(type(element[2]), int)

        # check that the first book in the search has 337 pages
        self.assertEqual(list_tuple[0][2], 337)


    def test_summarize_best_books(self):

        # call summarize_best_books and save it to a variable
        source_dir = os.path.dirname(__file__)
        fullpath = os.path.join(source_dir, "best_books_2020.htm")
        best_books = summarize_best_books(fullpath)

        # check that we have the right number of best books (20)
        self.assertEqual(len(best_books), 20)

        # assert each item in the list of best books is a tuple
        for element in best_books:
            self.assertEqual(type(element), tuple)


        # check that each tuple has a length of 3
        for element in best_books:
            self.assertEqual(len(element), 3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books[len(best_books)-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))


    def test_write_csv(self):

        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        chosen_titles = get_titles_from_search_results("search_results.htm")

        # call write csv on the variable you saved and 'test.csv'
        write_csv(chosen_titles, "test.csv")

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        f = open('test.csv')
        csv_reader = csv.reader(f, delimiter=',')
        csv_lines = [r for r in csv_reader]

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)

        # check that the header row is correct
        self.assertEqual(csv_lines[0],["Book title","Author Name"])

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1],['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[len(csv_lines)-1],['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])

        f.close()


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



