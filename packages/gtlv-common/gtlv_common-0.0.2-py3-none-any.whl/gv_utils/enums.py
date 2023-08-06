#!/usr/bin/env python3


class AttId:
    att = 'att'
    centerxy = 'centerxy'
    datapointeid = 'datapointeid'
    datapointseids = 'datapointseids'
    datatypeeid = 'datatypeeid'
    day = 'day'
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
    sampletime = 'sampletime'
    validfrom = 'validfrom'
    validto = 'validto'
    webatt = 'webatt'
    zoneeid = 'zoneeid'


class DbColumn:
    datapoint = 'data_point'
    datatype = 'data_type'
    dataquality = 'data_quality'
    day = 'day'
    eid = 'eid'
    fromtraveltime = 'from_travel_time'
    fromzonepoint = 'from_zone_point'
    imputedindicator = 'imputed_indicator'
    indicator = 'indicator'
    networkdataquality = 'network_data_quality'
    networkindicator = 'network_indicator'
    road = 'road'
    sampletime = 'sample_time'
    totraveltime = 'to_travel_time'
    tozonepoint = 'to_zone_point'
    validfrom = 'valid_from'


class DbTable:
    datapoint = 'data_point'
    datapointdataquality = 'data_point_data_quality'
    datapointimputedindicator = 'data_point_imputed_indicator'
    datapointindicator = 'data_point_indicator'
    datatype = 'data_type'
    networkdataquality = 'network_data_quality'
    networkindicator = 'network_indicator'
    road = 'road'
    roaddatapoint = 'road_data_point'
    roaddataquality = 'road_data_quality'
    roadindicator = 'road_indicator'
    zonepoint = 'zone_point'
    zonepointtraveltime = 'zone_point_travel_time'


class Message:
    data = 'data'
    format = 'format'
    timestamp = 'timestamp'
    kind = 'kind'


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


class MessageKind:
    separator = '-'

    mainprefix = 'gtlv'

    past = 'past'

    imputed = 'imputed'

    dataquality = 'dataquality'
    datapoint = 'datapoint'
    datatype = 'datatype'
    indicator = 'indicator'
    network = 'network'
    traveltime = 'traveltime'

    karrusrd = 'karrusrd'
    metropme = 'metropme'
    road = 'road'
    tomtomfcd = 'tomtomfcd'
    zonepoint = 'zonepoint'


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


class RequestPath(MessageKind):
    separator = '/'

    location = 'location'
    mapping = 'mapping'
    zone = 'zone'


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
