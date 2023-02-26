import { useState, useRef } from "react";
import { useGeolocated } from "react-geolocated";
import VenueService from "../services/venues";

const VenueSearch = ({ setVenues }) => {
    const [showFreeSearch, setShowFreeSearch] = useState(false);
    const { coords, isGeolocationAvail } =
        useGeolocated({
            positionOptions: {
                enableHighAccuracy: false
            },
            userDecisionTimeout: 5000,
        });

    const nameRef = useRef(null),
        dayRef = useRef(null),
        timeStartRef = useRef(null),
        timeEndRef = useRef(null);

    let times = [];
    for (let i = 8; i < 24; i++) {
        const timeStr = ((i < 10) ? `0${i}` : i) + "00";
        times.push(<option key={i} value={i}>{timeStr}</option>);
    }

    const getVenues = async () => {
        const cond = (showFreeSearch || (nameRef.current.value !== ""));
        const venues = (cond)
            ? await searchVenues()
            : await VenueService.getAll();
        setVenues(venues);
    }

    const searchVenues = async () => {
        const name = nameRef.current.value;
        let venues;

        if (showFreeSearch) {
            const day = dayRef.current.value,
                timeStart = timeStartRef.current.value,
                timeEnd = timeEndRef.current.value;

            const lat = (isGeolocationAvail) ? coords.latitude : null,
                lng = (isGeolocationAvail) ? coords.longitude : null;

            venues = await VenueService.venueSearch(name, day, timeStart, timeEnd, lat, lng);
        }

        else {
            venues = await VenueService.venueSearch(name);
        }

        return venues;
    }

    return (
        <>
            <div>
                <input
                    ref={nameRef}
                    className="txt-search"
                    type="search"
                    placeholder="Venue Name"
                    onChange={getVenues} />
            </div>
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
                                onChange={getVenues}>
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
                                onChange={getVenues}>
                                {times.slice(0, times.length - 1)}
                            </select>
                        </div>
                        <div className="venue-free-search-item">
                            <label htmlFor="venueFreeEndSel">To</label>
                            <select
                                ref={timeEndRef}
                                id="venueFreeEndSel"
                                className="venue-free-sel"
                                onChange={getVenues}>
                                {times.slice(1, times.length)}
                            </select>
                        </div>
                    </div>
                    : ""
                }
            </div>
        </>
    );
};

export default VenueSearch;