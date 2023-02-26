import { useState, useRef } from "react";
import { useGeolocated } from "react-geolocated";
import VenueService from "../services/venues";

const VenueFreeSearch = ({ setVenues }) => {
    const [showFreeSearch, setShowFreeSearch] = useState(false);
    const { coords, isGeolocationAvail, isGeolocationEnabled } =
        useGeolocated({
            positionOptions: {
                enableHighAccuracy: false
            },
            userDecisionTimeout: 5000,
        });

    const dayRef = useRef(null),
        timeStartRef = useRef(null),
        timeEndRef = useRef(null);

    let times = [];
    for (let i = 8; i < 24; i++) {
        const timeStr = ((i < 10) ? `0${i}` : i) + "00";
        times.push(<option key={i} value={i}>{timeStr}</option>);
    }

    const searchVenues = async () => {
        const day = dayRef.current.value,
            timeStart = timeStartRef.current.value,
            timeEnd = timeEndRef.current.value;

        console.log(isGeolocationEnabled, isGeolocationAvail);

        const lat = (isGeolocationAvail) ? coords.latitude : null,
            lng = (isGeolocationAvail) ? coords.longitude : null;

        const venues = await VenueService.freeSearchVenue(day, timeStart, timeEnd, lat, lng);
        setVenues(venues);
    }

    return (
        <div className="venue-free-search-container">
            <button
                className="btn-venue btn-venue-free"
                onClick={() => setShowFreeSearch(!showFreeSearch)}>
                Find Free Rooms
            </button>
            {(showFreeSearch) ?
                <div className="venue-free-search-query-container">
                    <div className="venue-free-search-item">
                        <label htmlFor="venueFreeDaySel">Day</label>
                        <select
                            ref={dayRef}
                            id="venueFreeDaySel"
                            className="venue-free-sel"
                            onChange={searchVenues}>
                            <option value="MON">Monday</option>
                            <option value="TUE">Tuesday</option>
                            <option value="WED">Wednesday</option>
                            <option value="THU">Thursday</option>
                            <option value="FRI">Friday</option>
                        </select>
                    </div>
                    <div className="venue-free-search-item">
                        <label htmlFor="venueFreeStartSel">From</label>
                        <select
                            ref={timeStartRef}
                            id="venueFreeStartSel"
                            className="venue-free-sel"
                            onChange={searchVenues}>
                            {times.slice(0, times.length - 1)}
                        </select>
                    </div>
                    <div className="venue-free-search-item">
                        <label htmlFor="venueFreeEndSel">To</label>
                        <select
                            ref={timeEndRef}
                            id="venueFreeEndSel"
                            className="venue-free-sel"
                            onChange={searchVenues}>
                            {times.slice(1, times.length)}
                        </select>
                    </div>
                </div>
                : ""
            }
        </div>
    );
};

export default VenueFreeSearch;