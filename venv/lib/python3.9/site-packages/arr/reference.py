from astropy.units import cgs
import webbrowser
import ads
from typing import Union
from warnings import warn

ads_link = 'https://ui.adsabs.harvard.edu/abs/{bibcode}/'
ext_link = 'https://ui.adsabs.harvard.edu/link_gateway/{bibcode}/'


class Reference:
    def __init__(self, bibcode: Union[bytes, str]):
        try:
            self.bibcode = bibcode.decode()
        except AttributeError:
            self.bibcode = bibcode
            
        self._title      = None
        self._authors    = None
        self._pubdate    = None
        self._abstract   = None
        self._link = ads_link.format(bibcode=self.bibcode)
        self._ext_link = ext_link.format(bibcode=self.bibcode)
    
    def _load(self):
        try:
            self.article = \
                [paper for paper in ads.SearchQuery(bibcode=self.bibcode, fl=['id', 'title','pubdate', 'abstract', 'author'])][0]
        except:
            warn(f"Can't find reference on ADS for {self.bibcode}",UserWarning)
            return

        self._title = self.article.title[0]
        self._authors = self.article.author
        self._pubdate = self.article.pubdate
        self._abstract = self.article.abstract

    def get_citation(self, index: int):
        try:
            return Reference(self.article.citation[index])
        except IndexError:
            return None

    def get_reference(self, index: int):
        try:
            return Reference(self.article.citation[index])
        except IndexError:
            return None

    def show(self):
        if self._link is not None:
            webbrowser.open(self._link + "abstract", new=2)

    def arxiv(self):
        if self._link is not None:
            webbrowser.open(self._ext_link + "EPRINT_PDF", new=2)

    def publisher(self):
        if self._link is not None:
            webbrowser.open(self._ext_link + "PUB_PDF", new=2)

    @property
    def title(self):
        if self._title is None:
            self._load()
        return self._title

    @property
    def authors(self):
        if self._authors is None:
            self._load()
        return self._authors

    @property
    def pubdate(self):
        if self._pubdate is None:
            self._load()
        return self._pubdate

    @property
    def abstract(self):
        if self._abstract is None:
            self._load()
        return self._abstract


    def __repr__(self):
        return self._title