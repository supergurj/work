import csv
import argparse
import re
import math

class DTInfo:

	def __init__(self, className, propName, dataBits ):
		self.className = className
		self.propName = propName
		self.dataBits = dataBits


parser = argparse.ArgumentParser(description='DTI file analysis')
parser.add_argument( "-f", dest="filename", required=True )
parser.add_argument( "-o", dest="outfilename", required=True)
parser.add_argument( "-a", dest="aggmethod", choices = [ 'c', 'f' ], required=True)
args = parser.parse_args()

with open( args.filename , newline='') as csvFile:

	dtiReader = csv.reader( csvFile )
	dti = []
	i = 0

	for row in dtiReader:
		if ( i != 0 ):
			propName = re.sub( r'\:.*', '', row[1] )
			dti.append( DTInfo( row[0], propName, float( row[4] ) / ( 8 ) ) )
		i = i+1


	dti.sort( key = lambda x: (x.className, x.propName) )

	if ( len(dti) > 0 ):

		dtiOut = []
		curDtiOut = DTInfo( dti[0].className, dti[0].propName, dti[0].dataBits )

		for i in range( 1, len( dti ) ):

			dtiElem = dti[i]
			bMatch = False

			if ( dtiElem.className == curDtiOut.className ):
				if ( args.aggmethod == 'c' ):
					curDtiOut.propName = 'na'
					bMatch = True
				elif ( args.aggmethod == 'f' ):
					if ( dtiElem.propName == curDtiOut.propName ):
						bMatch = True


			if ( bMatch ):
				curDtiOut.dataBits = curDtiOut.dataBits + dtiElem.dataBits
			else:
				dtiOut.append( curDtiOut )
				curDtiOut = DTInfo( dtiElem.className, dtiElem.propName, dtiElem.dataBits )

		dtiOut.append( curDtiOut )

		dtiOut.sort( key = lambda x: x.dataBits, reverse = True )

		fOut = open( args.outfilename, "w")

		for dtiElem in dtiOut:
			fOut.write ( dtiElem.className + ", " + dtiElem.propName + ", " + str( math.ceil( dtiElem.dataBits ) ) + '\n' )

		fOut.close()