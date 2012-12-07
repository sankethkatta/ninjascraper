import urllib2, urllib, bs4
import sys
def is_semester(string):
    return "Fall " in string or "Spring " in string or "Summer " in string 

def scrape_hkn(abv="CS",course="70"):
    prof_year = {} 
    html = urllib2.urlopen("https://hkn.eecs.berkeley.edu/coursesurveys/course/{0}/{1}".format(abv,course))
    soup = bs4.BeautifulSoup(html) 
    tables = soup.find_all("table")[1] 
    links = tables.find_all("a") 
    current_semester = None 
    current_tuple = ()
    for i in links:
        text = str(i.text)
        if is_semester(text):
            if current_semester:
                prof_year[current_semester] = current_tuple 
                current_tuple = () 
            current_semester = text 
        else:
            current_tuple += (text,) 
    prof_year[current_semester] = current_tuple
    return prof_year 
ways = ["","(solution)","solution"] 

def scrape_ninja(course="70",test="Midterm 1",department="COMPSCI",abv="CS"):
    prof_year = scrape_hkn(abv,course)
    base_url = "http://media.ninjacourses.com/var/exams/1/{0}/{1}%20{2}%20-%20{3}%20{4}%20-%20{5}%20-%20{6}%20{7}.pdf" 
    exists = {}  
    for semester,profs in prof_year.iteritems():
            sem,year = tuple(semester.split()) 
            for prof in profs:
                
                for way in ways:
                    try:
                        prof = prof.split()[-1] 
                        test_split = test.split() 
                        if len(test_split) == 1: 
                            url = base_url.format(department,abv,course,sem,year,prof,test,way) 
                            if not way:
                                url = url[:-7] + ".pdf"
                        elif len(test_split) == 2: 
                            url = base_url.format(department,abv,course,sem,year,prof,test_split[0],test_split[1]) 
                            if way:
                                url = url[:-4] + "%20"+way + url[-4:] 

                            
                        urllib2.urlopen(url) 
                        exists[str(profs + (test,way))+" "+semester ] = url
                    except Exception as e:
                        #print e  
                        pass
    for info,url in exists.iteritems():
        print url
        urllib.urlretrieve(url,info+ ".pdf")

tests = ['Midterm','Midterm 1','Midterm 2', 'Midterm 3','Final']

if (len(sys.argv) > 1):
    for test in tests: 
        scrape_ninja(sys.argv[1],test) 
else:
    for test in tests: 
        scrape_ninja("70",test)
