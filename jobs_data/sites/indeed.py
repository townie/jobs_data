from indeed import IndeedClient

client = IndeedClient('1439892112925001')

params = {
    'q' : "python",
    'l' : "boston",
    'userip' : "1.2.3.4",
    'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)"
}



url = 'http://www.indeed.com/viewjob?jk=89b6ad7a31f7c4be&qd=Edw9zLy29tPtf_aglDLrzkea4GYpkSu9Dn9RxMjGtc-Au7bNkAhEpP8509-8oVyQct6gb9Hh9FwGl317FwNQL73cXKONUJYtCg03YtTr2S0&indpubnum=1439892112925001&atk=1b94foutl5sn398g'

import requets
requests.get(url)



jobkey='89b6ad7a31f7c4be'