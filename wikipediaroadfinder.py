import wikipedia
import wikipediaapi
import time
from time import strftime
from time import gmtime
import concurrent.futures
from queue import Queue
import pickle
import json

# Settings
start_page = 'Ketchup'  # the page where the search starts
end_page = 'Paracetamol'  # the page where the search ends
wiki = wikipediaapi.Wikipedia('ro')  # change to your Wikipedia language
maxDepth = 10

# Skippable pages, not fair using them, change them to your own language to skip them
bad_links = ["Wikipedia:", "Ajutor:", "Format:", "WP:", "Categorie:",  # ro
             "Utilizator:", "Fișier:", "Portal:", "Proiect:", "MediaWiki:", "Modul:",
             "Wikipedia:", "Help:", "Format:", "WP:", "Discuție:",
             "Category:",  # en
             "User:", "File:", "Portal:", "Project:", "MediaWiki:", "Module:"]

# Global variable declaration
pages = [[] for i in range(maxDepth + 1)]
parent = {}
pathFound = 0
executor_pool = concurrent.futures.ThreadPoolExecutor()
page_to_links = {}


def bad_link(link):
    for bad in bad_links:
        if link.find(bad) != -1:
            return True
    return False


def get_page_links(page):
    try:
        links = [link for link in wiki.page(page).links if not bad_link(link)]
        if len(links) != 0:
            return {page: links}
        else:
            return {}
    except:
        return {}


def get_children_links(page, visited):
    children = [link for link in wiki.page(page).links if not bad_link(link)]
    children_links = {}

    threads = []
    for child in children:
        if child not in visited:
            threads.append(executor_pool.submit(get_page_links, child))
    for t in concurrent.futures.as_completed(threads):
        children_links.update(t.result())

    return children_links


def cache(cache_file, timeout=600, starting_page="Wikipedia"):
    page_to_links = {starting_page: [link for link in wiki.page(starting_page).links if not bad_link(link)]}
    q = Queue()
    visited = set()

    q.put(starting_page)
    visited.add(starting_page)

    start_time = time.time()
    while not q.empty() and time.time() - start_time < timeout:
        page = q.get()
        page_to_links.update(get_children_links(page, visited))

        try:
            for child in page_to_links[page]:
                if child not in visited:
                    visited.add(child)
                    q.put(child)
        except:
            pass

    with open(cache_file, 'wb') as write_file:
        pickle.dump(page_to_links, write_file)


def find_path():
    pass


if __name__ == "__main__":
    # cache("caching.bin", starting_page="Balerin", timeout=200)
    with open("caching.bin", 'rb') as read_file:
        page_to_links = pickle.load(read_file)

    # print(len(d))
    # with open("output", 'w') as output:
    #     output.write(json.dumps(d, indent=4, sort_keys=True))
