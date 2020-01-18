import wikipediaapi
import time
from time import strftime
from time import gmtime
from threading import Thread

#settings
startPage = 'Gaz petrolier lichefiat'
endPage = 'Paracetamol'
initWiki = wikipediaapi.Wikipedia('ro')
maxDepth = 10

#Skippable pages, not fair using them
bad_links = ["Wikipedia:", "Ajutor:", "Format:", "WP:", "Categorie:",\
 "Utilizator:", "Fișier:", "Portal:", "Proiect:", "MediaWiki:", "Modul:"]

#global variable declaration
pages = []
parent = {}
pathFound = 0
threads = []

#make variable pages a matrix
for i in range(maxDepth + 2):
    line = []
    pages.append(line)

#function that searches the page given in 'pageName' and ads the links to queue
def searchPage(depth, pageName):
    global pathFound
    try:
        page = initWiki.page(pageName)
        sortedLinks = page.links
    except:
        sortedLinks = {}
    for title, y in sortedLinks.items():
        if(str(title) == endPage):
            parent[endPage] = pageName
            pathFound = 1
        bad = 0
        for i in bad_links:
            if(title.find(i) != -1):
                bad = 1
        if((title in parent) == False and bad == 0):
            parent[title] = pageName
            pages[depth + 1].append(str(title))

#main function
def main():
    currentDepth = 0
    pages[0].append(startPage)
    parent[startPage] = 'NULL'
    startTime = time.time()
    while(currentDepth <= maxDepth):
        threads = []
        print(f"Searching depth {currentDepth}")
        for i in pages[currentDepth]:
            t = Thread(target = searchPage, args = (currentDepth, i))
            threads.append(t)
        [t.start() for t in threads]
        [t.join() for t in threads]
        if(pathFound == 1):
            it = endPage
            print("\nPath: " + it, end = " ")
            while(parent[it] != 'NULL'):
                print("<- " + parent[it], end = " ")
                it = parent[it]
            print("\nTime to finish: " + strftime("%H:%M:%S", gmtime(time.time() - startTime)))
            break
        currentDepth += 1

main()
