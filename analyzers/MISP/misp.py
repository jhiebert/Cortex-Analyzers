#!/usr/bin/env python
from cortexutils.analyzer import Analyzer
from mispclient import MISPClient


class MISPAnalyzer(Analyzer):
    """Searches for given IOCs in configured misp instances. All standard data types are supported."""

    def __init__(self):
        Analyzer.__init__(self)
        self.misp = MISPClient(url=self.getParam('config.url', None, 'No MISP url given.'),
                               key=self.getParam('config.key', None, 'No MISP api key given.'),
                               ssl=self.getParam('config.certpath', True),
                               name=self.getParam('config.name', None))

    def summary(self, raw):

        data = []
        for r in raw['results']:
            for res in r['result']:
                if 'uuid' in res:
                    data.append(res['uuis'])

        # return number of unique events
        if data == []:
            return {'results': 0}
        else:
            return {'results': len(list(set(data)))}

    def run(self):
        if self.data_type == 'hash':
            response = self.misp.search_hash(self.getData())
        elif self.data_type == 'url':
            response = self.misp.search_url(self.getData())
        elif self.data_type == 'domain' or self.data_type == 'fqdn':
            response = self.misp.search_domain(self.getData())
        elif self.data_type == 'mail' or self.data_type == 'mail_subject':
            response = self.misp.search_mail(self.getData())
        elif self.data_type == 'ip':
            response = self.misp.search_ip(self.getData())
        elif self.data_type == 'registry':
            response = self.misp.search_registry(self.getData())
        elif self.data_type == 'filename':
            response = self.misp.search_filename(self.getData())
        else:
            response = self.misp.searchall(self.getData())

        self.report({'results': response})

if __name__ == '__main__':
    MISPAnalyzer().run()