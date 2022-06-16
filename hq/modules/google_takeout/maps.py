from datetime import datetime
import json
import locale
import zipfile

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from hq.common import parse_datetime

from hq.config import GoogleTakeout as config
from hq.modules.google_takeout.utils import get_zip_file_paths

FOLDER_PREFIX = "Histórico de localização"
MAPS_FOLDER_PREFIX = "Maps (Seus lugares)"
SEMANTIC_FOLDERS_PREFIX = "Semantic Location History"

"""
- Histórico de localização
- Maps/Meus lugares marcados
- Maps (Seus lugares)
"""

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


class Saved(BaseModel):
    raw: dict
    latitude: float
    longitude: float
    url: str
    address: Optional[str]
    name: str
    country: Optional[str]

    def __init__(self, raw):
        data = {"raw": raw}

        properties = raw.get("properties", {})
        data["url"] = properties.get("Google Maps URL")

        location = properties.get("Location")
        data["address"] = location.get("Address")
        data["name"] = location.get("Business Name") or properties.get("Title")
        data["country"] = location.get("Country Code")

        coordinates = location.get("Geo Coordinates")
        data["latitude"] = coordinates.get("Latitude")
        data["longitude"] = coordinates.get("Longitude")

        date_str = properties.get("Published")
        data["date_tz"] = parse_datetime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        super().__init__(**data)


class Location(BaseModel):
    raw: dict
    latitudeE7: int
    longitudeE7: int
    accuracy: Optional[int]
    source: Optional[str]
    date_tz: datetime
    altitude: Optional[int]
    device_tag: Optional[str]

    def __init__(self, raw):
        data = {"raw": raw}
        data["latitudeE7"] = raw.get("latitudeE7")
        data["longitudeE7"] = raw.get("longitudeE7")
        data["accuracy"] = raw.get("accuracy")
        data["source"] = raw.get("source")
        data["device_tag"] = raw.get("device_tag")
        data["altitude"] = raw.get("altitude")

        date_str = raw.get("timestamp")
        if '.' in date_str:
            date_tz = parse_datetime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            date_tz = parse_datetime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        data["date_tz"] = date_tz
        super().__init__(**data)


class Place(BaseModel):
    raw: dict
    latitudeE7: int
    longitudeE7: int
    placeId: str
    address: Optional[str]
    name: Optional[str]
    device_tag: Optional[str]
    duration_start: datetime
    duration_end: datetime
    date_tz: datetime

    def __init__(self, raw):
        data = {"raw": raw}

        location = raw.get("location", {})
        if location.get("latitudeE7", None) is None or location.get("longitudeE7", None) is None:
            location = raw["otherCandidateLocations"][0]

        data["latitudeE7"] = location.get("latitudeE7")
        data["longitudeE7"] = location.get("longitudeE7")
        data["placeId"] = location.get("placeId")
        data["address"] = location.get("address")
        data["name"] = location.get("name")
        data["device_tag"] = location.get("device_tag")

        duration_start = raw.get("duration", {}).get("startTimestamp")
        if '.' in duration_start:
            duration_start = parse_datetime(duration_start, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            duration_start = parse_datetime(duration_start, "%Y-%m-%dT%H:%M:%SZ")
        data["date_tz"] = duration_start
        data["duration_start"] = duration_start

        duration_end = raw.get("duration", {}).get("endTimestamp")
        if '.' in duration_end:
            duration_end = parse_datetime(duration_end, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            duration_end = parse_datetime(duration_end, "%Y-%m-%dT%H:%M:%SZ")
        data["duration_end"] = duration_end

        super().__init__(**data)


class ActivitySegment(BaseModel):
    raw: dict
    start_location: Optional[Location]
    end_location: Optional[Location]
    duration_start: datetime
    duration_end: datetime
    date_tz: datetime
    distance: Optional[int]
    activity_type: Optional[str]
    confidence: Optional[str]

    def __init__(self, raw):
        data = {"raw": raw}
        data["start_location"] = None
        data["end_location"] = None

        startLocation = raw.get("startLocation")
        if startLocation:
            startLocation["timestamp"] = raw.get("duration", {}).get("startTimestamp")
            start_loc = Location(startLocation)
            data["start_location"] = start_loc

        endLocation = raw.get("endLocation")
        if endLocation:
            endLocation["timestamp"] = raw.get("duration", {}).get("endTimestamp")
            end_loc = Location(endLocation)
            data["end_location"] = end_loc


        duration_start = raw.get("duration", {}).get("startTimestamp")
        if '.' in duration_start:
            duration_start = parse_datetime(duration_start, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            duration_start = parse_datetime(duration_start, "%Y-%m-%dT%H:%M:%SZ")
        data["date_tz"] = duration_start
        data["duration_start"] = duration_start

        duration_end = raw.get("duration", {}).get("endTimestamp")
        if '.' in duration_end:
            duration_end = parse_datetime(duration_end, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            duration_end = parse_datetime(duration_end, "%Y-%m-%dT%H:%M:%SZ")
        data["duration_end"] = duration_end

        data["distance"] = raw.get("distance")
        data["activity_type"] = raw.get("activityType")
        data["confidence"] = raw.get("confidence")
        super().__init__(**data)


def get_file_paths():
    return get_zip_file_paths(config.export_path)


def process_semantic_locations(input_files=None):
    if not input_files:
        input_files = get_file_paths()
    print("input files", len(input_files))

    for zip_path in input_files:
        zf = zipfile.ZipFile(zip_path)
        location_files = [
            i for i in zf.filelist
            if FOLDER_PREFIX in str(i) and SEMANTIC_FOLDERS_PREFIX in str(i)
        ]
        print("location_files", len(location_files))
        for file_name in location_files:
            with zf.open(file_name) as f:
                content = json.load(f)

                for info in content["timelineObjects"]:
                    placeVisit = info.get("placeVisit")
                    if placeVisit:
                        yield Place(placeVisit)

                    activitySegment = info.get("activitySegment")
                    if activitySegment:
                        yield ActivitySegment(activitySegment)


def process_locations(input_files=None):
    if not input_files:
        input_files = get_file_paths()

    # for each account file export
    include_key = "Records.json"
    for zip_path in input_files:
        zf = zipfile.ZipFile(zip_path)

        location_files = [
            i for i in zf.filelist
            if FOLDER_PREFIX in str(i) and include_key in str(i)
        ]
        # for each one of the found files
        for file_name in location_files:
            with zf.open(file_name) as f:
                content = json.load(f)

                for loc in content["locations"]:
                    yield Location(loc)


def process_saved_locations(input_files=None):
    if not input_files:
        input_files = get_file_paths()

    # for each account file export
    include_key = "Lugares salvos.json"
    for zip_path in input_files:
        zf = zipfile.ZipFile(zip_path)
        location_files = [
            i for i in zf.filelist
            if MAPS_FOLDER_PREFIX in str(i) and include_key in str(i)
        ]
        # for each one of the found files
        for file_name in location_files:
            with zf.open(file_name) as f:
                content = json.load(f)

                for loc in content["features"]:
                    yield Saved(loc)
