from gdata.spreadsheet.service import SpreadsheetsService, DocumentQuery, CellQuery

APP_NAME  = 'ISU/ITRC-conglomerator-1.0'
FORM_NAME = 'FORM: Metacourse Request Form'
FORM_COLS = ()
FORM_KEYS = ('tstamp', 'instr', 'email',
            'dept', 'alt_dept', 'cnum',
            'title', 'sects', 'term',
            'year', 'status', 'comments')

class Request:
    def __init__(self, entry):
        self.entry = entry
        for key, col in zip(FORM_KEYS, FORM_COLS):
            setattr(self, key, entry.custom[col].text)
    
    def __str__(self):
        return str.join(', ', ('%s: %s' % (key, getattr(self, key)) for key in FORM_KEYS))
    
    def data(self):
        return dict(zip(FORM_COLS, (getattr(self, key) for key in FORM_KEYS)))

class GoogleConn:
    def __init__(self, usr, pwd, form):
        global FORM_COLS
        self.gc = SpreadsheetsService()
        self.gc.ClientLogin(username=usr, password=pwd, source=APP_NAME)
        query = DocumentQuery()
        query.title = form
        feed = self.gc.GetSpreadsheetsFeed(query=query)
        if not feed.entry: raise Exception, "empty spreadsheet list"
        self.formid = feed.entry[0].id.text.rsplit('/', 1)[1]
#        self.update = feed.entry[0].updated.text
        query = CellQuery()
        query.range = '%c1:%c1' % tuple(i+ord('A') for i in (0, len(FORM_KEYS)-1))
        feed = self.gc.GetCellsFeed(self.formid, query=query)
        FORM_COLS = tuple(''.join(c for c in cell.content.text.lower()
                          if c.isalnum() or c in '-_') for cell in feed.entry)
        self.statcol = FORM_COLS[FORM_KEYS.index('status')]
        
    def get_requests(self):
        feed = self.gc.GetListFeed(self.formid)
        return [Request(row) for row in feed.entry if not row.custom[self.statcol].text]
    
    def update_request(self, request):
        request.entry = self.gc.UpdateRow(request.entry, request.data())
        
def connect(usr, pwd, form=FORM_NAME):
    return GoogleConn(usr, pwd, form)
    