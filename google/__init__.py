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

    def search(self, search, results):
        if(len(results)<2):
            pass
        answers = self.gsearch.google(search)
        for ans in answers:
            results.append(ans['url'],
                            'zoom-in',
                            self.results_category,
                            "text/html",
                            ans['title'][:45],
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
        pass
