#!/usr/bin/env python3


class DbColumn:
    att = 'att'
    classification = 'classification'
    confidence = 'confidence'
    datapoint = 'data_point'
    datatype = 'data_type'
    dataquality = 'data_quality'
    day = 'day'
    density = 'density'
    eid = 'eid'
    flow = 'flow'
    fluidity = 'fluidity'
    fromtraveltime = 'from_travel_time'
    fromzonepoint = 'from_zone_point'
    geom = 'geom'
    id = 'id'
    imputedindicator = 'imputed_indicator'
    indicator = 'indicator'
    networkdataquality = 'network_data_quality'
    networkindicator = 'network_indicator'
    occupancy = 'occupancy'
    road = 'road'
    sampletime = 'sample_time'
    speed = 'speed'
    totraveltime = 'to_travel_time'
    tozonepoint = 'to_zone_point'
    traveltime = 'travel_time'
    validfrom = 'valid_from'
    validto = 'valid_to'
    webatt = 'web_att'


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


class MessageData(DbColumn):
    csvseparator = ';'
    encoding = 'utf-8'

    status = 'status'

    late = -2
    nan = -1


class AttId(DbColumn):
    centerxy = 'centerxy'
    datapointseids = 'datapoints'
    ffspeed = 'ffspeed'
    fow = 'fow'
    frc = 'frc'
    fromno = 'fromno'
    geomxy = 'geomxy'
    length = 'length'
    mainroad = 'mainroad'
    maxspeed = 'maxspeed'
    name = 'name'
    nlanes = 'nlanes'
    no = 'no'
    roads = 'roads'
    tono = 'tono'
    zone = 'zone'


class MessageFormat:
    json = 'json'
    csv = 'csv'


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
    separator = ','

    datatype = 'datatype'
    eid = 'eid'
    fromdatetime = 'fromdatetime'
    frompoint = 'frompoint'
    indicator = 'indicator'
    period = 'period'
    topoint = 'topoint'
    todatetime = 'todatetime'
    within = 'within'

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
