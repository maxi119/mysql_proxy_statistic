
skipStart = ["SET", 'set', 'rollback', 'commit']
skipQuery = ["django_session"]

class statObj:
    def __init__(self):
        self.count = 0
        self.max = 0
        self.min = 999999.99
        self.total = 0
        self.qtime = 0
        self.q = ""
        self.rtime = 0

def main():
    import sys
    import re
    from operator import itemgetter, attrgetter, methodcaller
    
    pattern = re.compile( r'(query-time:|response-time:|we got a normal query:)\s*(.*)' )
    patTime = re.compile( r'([0-9\.]+)ms' )

    stat = {}
    objTmp = statObj()
    tmpList = []
    while True:
        try:
            line = sys.stdin.readline()
        except (KeyboardInterrupt, SystemExit) as e:
            break

        if not line:
            break
        g = pattern.match( line )
        if not g:
            continue
       
        if g.groups()[0] == 'we got a normal query:':
            objTmp.q = g.groups()[1]
            lowQ = objTmp.q.lower()
            if lowQ.startswith( "insert"):
                objTmp.q = objTmp.q[: objTmp.q.find( "(" ) ]
            elif lowQ.startswith( "select"):
                objTmp.q = objTmp.q[: lowQ.find( "where" ) ]
        elif g.groups()[0] == 'query-time:':
            #print g.groups()
            objTmp.qtime = float( patTime.match(  g.groups()[1] ).groups()[0] )
        elif  g.groups()[0] == 'response-time:':
            #print g.groups()
            objTmp.rtime = float( patTime.match(  g.groups()[1] ).groups()[0] )
            q = objTmp.q
            skip = False
            for s in skipQuery:
                if s in q:
                    skip = True
                    break
            for s in skipStart:
                if q.startswith( s ):
                    skip = True
                    break
            if skip or len(q)==0:
                continue
            if q not in stat:
                stat[ q ] = statObj()
            objTmp.total =  objTmp.rtime + objTmp.qtime
            stat[ q ].count +=1
            stat[ q ].max = max( stat[ q ].max, objTmp.total )
            stat[ q ].min = min( stat[ q ].min, objTmp.total )
            stat[ q ].total += objTmp.total
            objTmp = statObj()

    summary = {'max':{'q':'','v':0 }, 'min':{'q':'', 'v':99999}, 'total':{'q':'','v':0 }   }
    for key,v in stat.items():
        v.q = key
        tmpList.append( v )

    minList = sorted( tmpList, key=attrgetter( 'min' ) )
    maxList = sorted( tmpList, key=attrgetter( 'max' ), reverse = True )
    totalList = sorted( tmpList, key=attrgetter( 'total'), reverse = True )

    def _printSorted( theList, title, col ):
        print( title )
        print( "      time                count        query" )
        for i in xrange( min( 10, len(theList) ) ):
            row = theList[i]
            print( " %3d  %10.3fms      %5d          %s"%( i+1, getattr(row,col), row.count, row.q[:min(100, len(row.q))] ) )
        print( "\n\n" )

    _printSorted( minList, "Min", "min" )
    _printSorted( maxList, "Max", "max" )
    _printSorted( totalList, "Total", "total" )
#        print( key )
#        print( "max: %.3f min: %.3f total: %.3f avg: %.3f count: %d\n"%( v.max, v.min, v.total, v.total/v.count, v.count ) )
       
#        if summary['max']['v'] < v.max:
#            summary['max']['v'] = v.max
#            summary['max']['q'] = key

#        if summary['min']['v'] > v.min:
#            summary['min']['v'] = v.min
#            summary['min']['q'] = key

#        if summary['total']['v'] < v.total:
#            summary['total']['v'] = v.total
#            summary['total']['q'] = key

#    from pprint import pprint
#    for key, v in summary.items():
#        print( key )
#        pprint( v )





if __name__ == "__main__":
    main()
