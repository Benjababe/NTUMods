import { useEffect, useState } from "react";
import venueService from "../services/venues";
import VenueItem from "./VenueItem";

const Venues = () => {
    const [venues, setVenues] = useState(null);

    useEffect(() => {
        if (venues == null) {
            venueService.getAll().then(venues => {
                setVenues(venues);
            });
        }
    }, [venues]);

    const getUrl = async (url) => {
        const venues = await venueService.getUrl(url);
        setVenues(venues);
    }

    const venuesList = (venues == null)
        ? []
        : venues["results"].map((venue) => {
            return <VenueItem key={venue.id} venue={venue.name} />;
        });

    return (
        <>
            <div>
                <input type="search" placeholder="Venue Name" />
            </div>
            <div className="venue-results">
                <ul className="venue-list">
                    {venuesList}
                </ul>
            </div>
            <div className="pager venue-pager">
                {(venues && venues.previous) ? <input type="button" value="Previous" onClick={() => getUrl(venues.previous)} /> : ""}
                {(venues && venues.next) ? <input type="button" value="Next" onClick={() => getUrl(venues.next)} /> : ""}
            </div>
        </>
    );
}

export default Venues;