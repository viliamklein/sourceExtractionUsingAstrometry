from pydoc import locate
import numpy as np

def GetJD(YY, MM, DD, UT):
    '''From Sidereal Time Calculator, valid for dates between 1901 - 2099. 
    
    Inputs: 
    YY - year
    MM - month
    DD - day
    UT - UT time (decimal hours)
    
    Output:
    jd - Julian Day
    
    EFY, SWRI, 19-JAN-2022'''
    
    jd = (367*YY) - int((7*(YY+int((MM+9)/12)))/4) + int((275*MM)/9) + DD + 1721013.5 + (UT/24) # Julian Date
    return(jd)

def GetGMST(JD):
    '''From Sidereal Time Calculator, valid for dates between 1901 - 2099. 
    
    Inputs: 
    JD - Julian Date
    
    Output:
    GMST - Greenwich mean sidereal time (decimal hours)
    
    EFY, SWRI, 19-JAN-2022'''
    
    GMST = (18.697374558 + 24.06570982441908*(JD - 2451545)) % 24
    return(GMST)

def GetEL_AZ(DEC, LAT, HA):
    '''From Duffett-Smith, Practical Astronomy with your Calculator.
    
    sin(EL) = sin(DEC)*sin(LAT) + cos(DEC)*cos(LAT)*cos(HA)
    
    and 
    
    cos(AZ) = (sin(DEC) - sin(LAT)*sin(EL))/(cos(LAT)*cos(EL))
    
    Inputs: (decimal degrees)
    DEC - object's declination
    LAT - observer's latitude
    HA -  object's hour angle (HA = LST - RA)
    
    Outputs:
    EL - elevation (deg)
    AZ - azimuth (deg)
    
    EFY, SWRI, 21-JAN-2022
    '''
    
    toRad = np.pi/180.
    toDeg = 180./np.pi
    
    D2 = toRad * DEC
    L2 = toRad * LAT
    H2 = toRad * HA
    
    EL = np.arcsin(np.sin(D2)*np.sin(L2) + np.cos(D2)*np.cos(L2)*np.cos(H2))
    AZ = np.arccos((np.sin(D2) - np.sin(L2)*np.sin(EL))/(np.cos(L2)*np.cos(EL)))
    
    if(np.sin(H2) > 0.0):
        AZ = 2*np.pi - AZ
        
    return(EL*toDeg, AZ*toDeg)

def azEl(time, location, target):

    uLat = location['latitude']
    uLon = location['longitude']
    year = time['year']
    month = time['month']
    day = time['day']
    currHour = time['hour']

    JD = GetJD(year, month, day, currHour)
    gmst = GetGMST(JD)
    LST = gmst + (uLon / 15.)

    sDEC = target['dec']
    sRA = target['ra']
    sHA = LST*15. - sRA # We want hour angle in decimal degrees, not hours
    sEL, sAZ = GetEL_AZ(sDEC, uLat, sHA)

    return sEL, sAZ


def azElRate(time, location, target):

    uLat = location['latitude']
    uLon = location['longitude']
    year = time['year']
    month = time['month']
    day = time['day']
    currHour = time['hour']
    dT = 0.001

    JD = GetJD(year, month, day, currHour)
    gmst = GetGMST(JD)
    LST = gmst + (uLon / 15.)

    JD2 = GetJD(year, month, day, currHour+dT)
    GMST2 = GetGMST(JD2)
    LST2 = GMST2 + (uLon / 15.)

    sDEC = target['dec']
    sRA = target['ra']
    sHA = LST*15. - sRA # We want hour angle in decimal degrees, not hours
    sEL, sAZ = GetEL_AZ(sDEC, uLat, sHA)

    sHA2 = LST2*15 - sRA # We want hour angle in decimal degrees, not hours
    sEL2, sAZ2 = GetEL_AZ(sDEC, uLat, sHA2)

    dEL = (sEL - sEL2)/(dT) # degrees per hour, or arcsec per sec.
    dAZ = (sAZ - sAZ2)/(dT)

    return dEL, dAZ


if __name__ == "__main__":

    import datetime

    location = {}
    location['latitude'] = 40.0373
    location['longitude'] = -105.2281

    year = datetime.datetime.utcnow().year
    month = datetime.datetime.utcnow().month
    day = datetime.datetime.utcnow().day
    hours = datetime.datetime.utcnow().hour
    minute = datetime.datetime.utcnow().minute
    second = datetime.datetime.utcnow().second
    ms = datetime.datetime.utcnow().microsecond
    currHour = np.longdouble(hours + minute/60. + second/3600. + ms/3600./1E6)
    currTime = {'year': year, 'month': month, 'day': day, 'hour': currHour}

    sDEC = -40.00378
    sRA = 120.9032
    target = {'dec': sDEC, 'ra': sRA}

    # dAz, dEl = azElRate(currTime, location, target)
    # print(dAz, dEl)

    # dAz, dEl = azElRate({'year': 2022, 'month': 1, 'day': 21, 'hour': 7.0},
                        # location, target)
    # print(dAz, dEl)
    print(currHour)
    JD = GetJD(year, month, day, currHour)
    print(JD)
    print(GetGMST(JD))
    
    LST = GetGMST(JD) + (location['longitude'] / 15.)
    sHA = LST*15. - sRA # We want hour angle in decimal degrees, not hours

    print(GetEL_AZ(sDEC, location['latitude'], sHA))

    # day = 21
    # minute = 0
    # second = 0
    # ms = 0
    
    # currHour = 7.
    # JD = GetJD(year, month, day, currHour)
    # gmst = GetGMST(JD)
    # LST = gmst + (uLon / 15.)

    # sHA = LST*15. - sRA # We want hour angle in decimal degrees, not hours
    # sEL, sAZ = GetEL_AZ(sDEC, uLat, sHA)

    # print("\nJD: {:8.15f}".format(JD))
    # print("Target Az, El: {:8.5f} deg, {:8.5f} deg".format(sAZ, sEL))

    # dT = 0.001
    # JD2 = GetJD(year, month, day, currHour+dT)
    # GMST2 = GetGMST(JD2)
    # LST2 = GMST2 + (uLon / 15.) # Minus sign is appropriate for W longitudes

    # sHA2 = LST2*15 - sRA # We want hour angle in decimal degrees, not hours
    # sEL2, sAZ2 = GetEL_AZ(sDEC, uLat, sHA2)

    # dEL = (sEL - sEL2)/(dT) # degrees per hour, or arcsec per sec.
    # dAZ = (sAZ - sAZ2)/(dT)

    # print("Rate dAz,dEl: {:8.15f}, {:8.15f} arcsec/sec\n\n".format(dAZ, dEL))


