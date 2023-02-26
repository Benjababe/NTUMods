import { useEffect, useState } from "react";
import venueService from "../services/venues";
import VenueItem from "./VenueItem";
import VenueTimetable from "./VenueTimetable";
import VenueFreeSearch from "./VenueFreeSearch";

const Venues = () => {
    const [venues, setVenues] = useState(null);
    const [timeslots, setTimeslots] = useState([]);

    useEffect(() => {
        if (venues == null) {
            venueService.getAll().then(venues => {
                setVenues(venues);
            });
        }
    }, [venues]);

    const loadTimeslots = async (venueId) => {
        const timeslots = await venueService.getTimeslots(venueId);
        setTimeslots(timeslots);
    }

    const getUrl = async (url) => {
        const venues = await venueService.getUrl(url);
        setVenues(venues);
    }

    const searchVenue = async (val) => {
        const venues = (val === "")
            ? await venueService.getAll()
            : await venueService.searchVenue(val);
        setVenues(venues);
    }

    const venuesList = (venues == null)
        ? []
        : venues["results"].map((venue) => {
            return <VenueItem key={venue.id} venue={venue} loadTimeslots={loadTimeslots} />;
        });

    return (
        <div className="venue-block">
            <div className="venue-sel-div">
                <div>
                    <input className="txt-search" type="search" placeholder="Venue Name" onChange={(e) => searchVenue(e.target.value)} />
                </div>
                <VenueFreeSearch setVenues={setVenues} />
                <div className="venue-results">
                    <ul className="venue-list">
                        {venuesList}
                    </ul>
                </div>
                <div className="pager venue-pager">
                    {(venues && venues.previous) ? <input type="button" value="Previous" onClick={() => getUrl(venues.previous)} /> : ""}
                    {(venues && venues.next) ? <input type="button" value="Next" onClick={() => getUrl(venues.next)} /> : ""}
                </div>
            </div>
            <div className="timeslot-div">
                {(timeslots.length) ? <VenueTimetable timeslots={timeslots} /> : ""}
            </div>
        </div>
    );
}

export default Venues;