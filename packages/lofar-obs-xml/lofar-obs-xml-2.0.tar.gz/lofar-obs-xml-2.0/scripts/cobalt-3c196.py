import momxml
import ephem
import sys
from numpy import sin, cos, sqrt, arctan2, arcsin


def lm_from_ra_dec(ra_angle, dec_angle, ra0_angle, dec0_angle):
    l_rad = cos(float(dec_angle))*sin(float(ra_angle - ra0_angle))
    m_rad = sin(float(dec_angle))*cos(float(dec0_angle)) - cos(float(dec_angle))*sin(float(dec0_angle))*cos(float(ra_angle - ra0_angle))
    return (l_rad, m_rad)


def ra_dec_from_lm(l_rad, m_rad, ra0_angle, dec0_angle):
    n_rad  = sqrt(1.0 - l_rad*l_rad - m_rad*m_rad)
    ra_rad = float(ra0_angle) + arctan2(l_rad,
                                        cos(float(dec0_angle))*n_rad - m_rad*sin(float(dec0_angle)))
    dec_rad = arcsin(m*cos(float(dec0_angle)) + sin(float(dec0_angle))*n_rad)
    return (momxml.Angle(rad=ra_rad), momxml.Angle(rad=dec_rad))


def rotate_lm_CCW(l_rad, m_rad, ccw_angle):
    cs = cos(float(ccw_angle))
    ss = sin(float(ccw_angle))

    l_new =  l_rad*cs + m_rad*ss
    m_new = -l_rad*ss + m_rad*cs
    return l_new, m_new
                

start_search_date = momxml.ephem.Date(momxml.next_sunset(sys.argv[1]))

target       = momxml.TargetSource(name      = '3C196',
                                   ra_angle  = momxml.Angle(shms = ('+', 8, 13, 36.0678)),
                                   dec_angle = momxml.Angle(sdms = ('+', 48, 13, 2.581)))

transit_date = momxml.next_date_with_lofar_lst(target.ra_angle.as_rad(), start_search_date)

target.name = '3C196-%4d-%02d-%02d' % transit_date.tuple()[0:3]



cal_fields   = [momxml.TargetSource(name      = '4C45.16',
                                    ra_angle  = momxml.Angle(shms = ('+', 8, 30, 35.8)),
                                    dec_angle = momxml.Angle(sdms = ('+', 45, 43, 30.0)))
                ]
ra_4c45_16    = cal_fields[0].ra_angle
dec_4c45_16   = cal_fields[0].dec_angle
pos_angle_inc = momxml.Angle(deg = 60.0)

antenna_set     = 'HBA_DUAL_INNER'
band            = 'HBA_LOW'
stations        = momxml.station_list('all', exclude=['DE604'])
int_s           = 2.0
chan            = 64
target_subbands = '77..456' # '51..442' # 380 subbands 115 -- 189 MHz
cal_subbands    = '77,99,121,144,166,188,211,233,257,278,299,321,345,367,389,412,434,456'
target_duration_s = 11*3600


for i in range(5):
    l0, m0 = lm_from_ra_dec(ra_4c45_16, dec_4c45_16, target.ra_angle, target.dec_angle)
    rot    = pos_angle_inc*(1+i)
    l, m   = rotate_lm_CCW(l0, m0, rot)
    ra_angle, dec_angle = ra_dec_from_lm(l, m, target.ra_angle, target.dec_angle)
    cal_fields.append(momxml.TargetSource('3C196-'+chr(ord('A')+i),
                                          ra_angle  = ra_angle,
                                          dec_angle = dec_angle))

sys.stderr.write('MAIN: '+str(target) + '\n')
for cal in cal_fields:
    sys.stderr.write(' CAL: '+str(cal)+ '\n')


observations = []
current_date = transit_date - 0.5*target_duration_s*ephem.second

backend = momxml.BackendProcessing(channels_per_subband     = chan,
                                   integration_time_seconds = int_s)

observations.append(momxml.Observation(
        beam_list        = [momxml.Beam(target, target_subbands)] + [momxml.Beam(field, cal_subbands) for field in cal_fields],
        antenna_set      = antenna_set,
        frequency_range  = band,
        start_date       = ephem.Date(current_date).tuple(),
        duration_seconds = target_duration_s,
        stations         = stations,
        clock_mhz        = 200,
        backend = backend,
        bit_mode         = 8))

start_tuple = ephem.Date(current_date).tuple()

folder=momxml.Folder(name='3C196:11h%04d%02d%02d-%02d%02d' % start_tuple[:5],
                     children=observations,
                     grouping_parent=True)

with open('cobalt-3c196-%04d%02d%02d-%02d%02d.xml' % start_tuple[:5], mode='w') as out:
    out.write(momxml.xml([folder],
                         project='COBALT'))
