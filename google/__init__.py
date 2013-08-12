import logging
import optparse
from search import GoogleSearch
import locale
from locale import gettext as _
locale.textdomain('google')

from singlet.lens import SingleScopeLens, IconViewCategory, ListViewCategory

from google import googleconfig

class GoogleLens(SingleScopeLens):

    class Meta:
        name = 'google'
        description = 'Google Lens'
        search_hint = 'Search Google'
        icon = 'google.svg'
        search_on_blank=True

    # TODO: Add your categories
    results_category = ListViewCategory("Google Search", 'edit-find-symbolic')
    browse_category = ListViewCategory("Find More", 'zoom-original-symbolic')
    gsearch = GoogleSearch()


    def trimTitleNaive(self, titleRaw):
        titleRaw = titleRaw[:50]
        title = ""
        if "-" in titleRaw:
            title = "-".join(titleRaw.split("-")[:2])
        else:
            title = titleRaw
        if "_" in titleRaw:
            title = "_".join(titleRaw.split("_")[:3])
        else:
            title = titleRaw
        return title


    narrowd = ['i','l','I','.','-',',',' ','!',':']

    def trimTitleMono(self,titleRaw):
        raw = titleRaw.strip()
        if "-" in raw:
            title = "-".join(raw.split("-")[:3])
        else:
            title = raw
        if "_" in raw:
            title = "_".join(raw.split("_")[:3])
        else:
            title = raw
        title = ""
        length = 0
        for uchar in raw:
            if uchar>= u'\u4e00' and uchar<=u'\u9fa5' or uchar=="W": #Chinese characters
                length += 3
            elif uchar in self.narrowd:
                length += 1
            elif uchar>=u'\u0041' and  uchar<=u'\u005a': # capital letters
                length += 2
            else:
                length += 1.5
            if length<65:
                title+=uchar
            else:
                break
        return title

    """
    updated: press space to search
    """
    def search(self, search, results):

        if len(search.strip())>=1 and search[-1]==" ":
            answers = self.gsearch.google(search)
            for ans in answers:
                results.append(ans['url'],
                                'zoom-in',
                                self.results_category,
                                "text/html",
                                self.trimTitleMono(ans['title']),
                                ans['synop'],
                                ans['url'])

        results.append(self.gsearch.getURL(search),
                            'zoom-original',
                            self.browse_category,
                            "text/html",
                            "Google",
                            "open browser",
                            self.gsearch.getURL(search)
            )
