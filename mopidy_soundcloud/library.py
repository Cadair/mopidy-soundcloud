from __future__ import unicode_literals

import logging

from mopidy import backend
from mopidy.models import SearchResult

logger = logging.getLogger(__name__)


class SoundCloudLibraryProvider(backend.LibraryProvider):
    def __init__(self, *args, **kwargs):
        super(SoundCloudLibraryProvider, self).__init__(*args, **kwargs)

    def find_exact(self, **query):
        return self.search(**query)

    def search(self, **query):
        if not query:
            return

        for (field, val) in query.iteritems():

            # TODO: Devise method for searching SoundCloud via artists
            if field == "album" and query['album'] == "SoundCloud":
                return SearchResult(
                    uri='soundcloud:search',
                    tracks=self.backend.sc_api.search(query['artist']) or [])
            elif field == "any":
                return SearchResult(
                    uri='soundcloud:search',
                    tracks=self.backend.sc_api.search(val[0]) or [])
            else:
                return []

    def lookup(self, uri):
        try:
            id = self.backend.sc_api.parse_track_uri(uri)
            return [self.backend.sc_api.get_track(id)]
        except Exception as error:
            logger.error(u'Failed to lookup %s: %s', uri, error)
            return []
