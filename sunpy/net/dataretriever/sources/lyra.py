# Author: Rishabh Sharma <rishabh.sharma.gunner@gmail.com>
# This module was developed under funding provided by
# Google Summer of Code 2014

from urllib.parse import urljoin
from sunpy.util.scraper import Scraper
from ..client import GenericClient

__all__ = ['LYRAClient']


class LYRAClient(GenericClient):
    """
    Provides access to the LYRA/Proba2 data `archive <http://proba2.oma.be/lyra/data/bsd/>`__
    hosted by the `PROBA2 Science Center <http://proba2.oma.be>`__.

    Examples
    --------

    >>> from sunpy.net import Fido, attrs as a
    >>> results = Fido.search(a.Time("2016/1/1", "2016/1/2"),
    ...                       a.Instrument('LYRA'))  #doctest: +REMOTE_DATA
    >>> results  #doctest: +REMOTE_DATA +ELLIPSIS
    <sunpy.net.fido_factory.UnifiedResponse object at ...>
    Results from 1 Provider:
    <BLANKLINE>
    2 Results from the LYRAClient:
         Start Time           End Time      Source Instrument Wavelength
           str19               str19         str6     str4       str3
    ------------------- ------------------- ------ ---------- ----------
    2016-01-01 00:00:00 2016-01-02 00:00:00 Proba2       lyra        nan
    2016-01-01 00:00:00 2016-01-02 00:00:00 Proba2       lyra        nan
    <BLANKLINE>
    <BLANKLINE>

    """
    def _get_url_for_timerange(self, timerange, **kwargs):
        """
        Return URL(s) for corresponding timerange.
        Parameters
        ----------
        timerange : `~sunpy.time.TimeRange`
        Returns
        -------
        list :
            The URL(s) for the corresponding timerange.
        """
        lyra_pattern = ('http://proba2.oma.be/lyra/data/bsd/%Y/%m/%d/'
                        'lyra_%Y%m%d-000000_lev{level}_std.fits')
        lyra_files = Scraper(lyra_pattern, level=kwargs.get('level', 2))
        urls = lyra_files.filelist(timerange)

        return urls

    def _get_url_for_date(self, date, **kwargs):
        """
        Return URL for corresponding date.

        Parameters
        ----------
        date : `astropy.time.Time`, `~datetime.datetime`, `~datetime.date`

        Returns
        -------
        str
            The URL for the corresponding date.
        """

        filename = "lyra_{}-000000_lev{:d}_std.fits".format(
            date.strftime('%Y%m%d'), kwargs.get('level', 2))
        base_url = "http://proba2.oma.be/lyra/data/bsd/"
        url_path = urljoin(date.strftime('%Y/%m/%d/'), filename)

        return urljoin(base_url, url_path)

    def _makeimap(self):
        """
        Helper Function:used to hold information about source.
        """
        self.map_['source'] = 'Proba2'
        self.map_['instrument'] = 'lyra'
        self.map_['physobs'] = 'irradiance'
        self.map_['provider'] = 'esa'

    @classmethod
    def _can_handle_query(cls, *query):
        """
        Answers whether client can service the query.

        Parameters
        ----------
        query : list of query objects

        Returns
        -------
        boolean
            answer as to whether client can service the query
        """
        chkattr = ['Time', 'Instrument', 'Level']
        chklist = [x.__class__.__name__ in chkattr for x in query]
        for x in query:
            if x.__class__.__name__ == 'Instrument' and x.value.lower() == 'lyra':
                return all(chklist)
        return False
