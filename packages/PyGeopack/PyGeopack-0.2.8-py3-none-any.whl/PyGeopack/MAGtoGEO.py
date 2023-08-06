import numpy as np
from ._CFunctions import _CMAGtoGEOUT,_CMAGtoGEOUT_LL
from ._CTConv import _CTConv


def MAGtoGEOLL(MLon, MLat, Date, ut, V=None):
	'''
	Converts from magnetic to geographic longitude and latitude.
	
	Inputs
	======
	MLon	: Array or scalar of magnetic longitude(s), in degrees.
	MLat	: Array or scalar of magnetic latitude(s), in degrees.
	Date	: Integer dat in format yyyymmdd.
	ut	: Time in hours (ut = hh + mm/60 + ss/3600).
	
	Returns
	=======
	lon	: Geographic longitude.
	lat	: Geographic latitude.
	
	'''
	#Convert input variables to appropriate numpy dtype:
	_MLon = _CTConv(MLon,'c_double_ptr')
	_MLat = _CTConv(MLat,'c_double_ptr')
	_n = _CTConv(_MLon.size,'c_int')
	if V is None:
		Vx = np.zeros(_n) + np.nan
		Vy = np.zeros(_n) + np.nan
		Vz = np.zeros(_n) + np.nan
	else:
		Vx = np.zeros(_n) + V[0]
		Vy = np.zeros(_n) + V[1]
		Vz = np.zeros(_n) + V[2]
	_Vx = _CTConv(Vx,'c_double_ptr')
	_Vy = _CTConv(Vy,'c_double_ptr')
	_Vz = _CTConv(Vz,'c_double_ptr')
	_Date = _CTConv(np.zeros(_n) + Date,'c_int_ptr')
	_ut = _CTConv(np.zeros(_n) + ut,'c_float_ptr')
	
	_Lon = np.zeros(_n,dtype="float64")
	_Lat = np.zeros(_n,dtype="float64")
				
				

	_CMAGtoGEOUT_LL(_MLon, _MLat, _n, _Vx, _Vy, _Vz, _Date, _ut, _Lon, _Lat)

	return _Lon,_Lat


def MAGtoGEO(Xin, Yin, Zin, Date, ut, V=None):
	'''
	Converts from magnetic to geographic coordinates
	
	Inputs
	======
	Xin	: Array or scalar of x coordinates in R_E.
	Yin	: Array or scalar of y coordinates in R_E.
	Zin	: Array or scalar of z coordinates in R_E.
	Date	: Integer dat in format yyyymmdd.
	ut	: Time in hours (ut = hh + mm/60 + ss/3600).
	
	Returns
	=======
	Xout,You,Zout	: x, y and z coordinates in R_E
	
	'''
	
	#Convert input variables to appropriate numpy dtype:
	_Xin = _CTConv(Xin,'c_double_ptr')
	_Yin = _CTConv(Yin,'c_double_ptr')
	_Zin = _CTConv(Zin,'c_double_ptr')
	_n = _CTConv(_Xin.size,'c_int')
	if V is None:
		Vx = np.zeros(_n) + np.nan
		Vy = np.zeros(_n) + np.nan
		Vz = np.zeros(_n) + np.nan
	else:
		Vx = np.zeros(_n) + V[0]
		Vy = np.zeros(_n) + V[1]
		Vz = np.zeros(_n) + V[2]
	_Vx = _CTConv(Vx,'c_double_ptr')
	_Vy = _CTConv(Vy,'c_double_ptr')
	_Vz = _CTConv(Vz,'c_double_ptr')
	_Date = _CTConv(np.zeros(_n) + Date,'c_int_ptr')
	_ut = _CTConv(np.zeros(_n) + ut,'c_float_ptr')
	
	_Xout = np.zeros(_n,dtype="float64")
	_Yout = np.zeros(_n,dtype="float64")
	_Zout = np.zeros(_n,dtype="float64")


	_CMAGtoGEOUT(_Xin, _Yin, _Zin, _n, _Vx, _Vy, _Vz, _Date, _ut, _Xout, _Yout, _Zout)

	return _Xout, _Yout, _Zout
