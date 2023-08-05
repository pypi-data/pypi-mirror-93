#!/usr/bin/env python3


class AttId:
    att = 'att'
    centerxy = 'centerxy'
    datapointeid = 'datapointeid'
    datapointseids = 'datapointseids'
    datatypeeid = 'datatypeeid'
    eid = 'eid'
    ffspeed = 'ffspeed'
    fow = 'fow'
    frc = 'frc'
    fromno = 'fromno'
    geom = 'geom'
    geomxy = 'geomxy'
    id = 'id'
    length = 'length'
    mainroad = 'mainroad'
    maxspeed = 'maxspeed'
    name = 'name'
    nlanes = 'nlanes'
    no = 'no'
    roadeid = 'roadeid'
    roads = 'roads'
    tono = 'tono'
    sample = 'sample'
    validfrom = 'validfrom'
    validto = 'validto'
    webatt = 'webatt'
    zoneeid = 'zoneeid'


class Message:
    data = 'data'
    format = 'format'
    timestamp = 'timestamp'
    type = 'type'


class MessageData:
    csvseparator = ';'
    encoding = 'utf-8'

    confidence = 'confidence'
    density = 'density'
    flow = 'flow'
    fluidity = 'fluidity'
    occupancy = 'occupancy'
    speed = 'speed'
    status = 'status'
    traveltime = 'traveltime'

    late = -2
    nan = -1


class MessageFormat:
    json = 'json'
    pandas = 'pandas'


class MessageType:
    separator = ':'

    past = 'past'

    imputed = 'imputed'

    data = 'data'
    dataquality = 'dataquality'
    datapoint = 'datapoint'
    datatype = 'datatype'
    indicator = 'indicator'
    location = 'location'
    mapping = 'mapping'
    traveltime = 'traveltime'

    karrusrd = 'karrusrd'
    metropme = 'metropme'
    road = 'road'
    tomtomfcd = 'tomtomfcd'
    zone = 'zone'


class RequestParam:
    separator = ';'

    area = 'area'
    datatypeeid = 'datatypeeid'
    eid = 'eid'
    fromdatetime = 'fromdatetime'
    frompointeid = 'frompointeid'
    indicator = 'indicator'
    period = 'period'
    topointeid = 'topointeid'
    todatetime = 'todatetime'

    day = 'day'
    week = 'week'
    month = 'month'


class NetworkObjId:
    datapointsroadsmap = 'datapointsroadsmap'
    frcroadsmap = 'frcroadsmap'
    lonlatnodesmatrix = 'lonlatnodesmatrix'
    mainclustersgeom = 'mainclustersgeom'
    newdpmappings = 'newdpmappings'
    newzonemappings = 'newzonemappings'
    omiteddatapoints = 'omiteddatapoints'
    roadclustermap = 'roadclustermap'
    roadsdatamap = 'roadsdatamap'
    roadsffspeedmap = 'roadsffspeedmap'
    roadszonesmap = 'roadszonesmap'
    voronoiroadmap = 'voronoiroadmap'
    zonesdatamap = 'zonesdatamap'
