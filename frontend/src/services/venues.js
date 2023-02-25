let venueUrl = "";
let timeslotUrl = "";
let searchUrl = ""

if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
    venueUrl = "http://localhost:8000/venue/";
    venueUrl = "http://localhost:8000/timeslot/";
    venueUrl = "http://localhost:8000/venuesearch/";
} else {
    venueUrl = "/venue/";
    timeslotUrl = "/timeslot/";
    searchUrl = "/venuesearch/"
}

const getAll = async () => {
    const venues = await fetch(venueUrl);
    return venues.json();
}

const getUrl = async (url) => {
    const venues = await fetch(url);
    return venues.json();
}

const getTimeslots = async (venueId) => {
    const timeslots = await fetch(`${timeslotUrl}?venue_id=${venueId}`);
    return timeslots.json();
}

const searchVenue = async (searchVal) => {
    const venues = await fetch(`${searchUrl}?name=${encodeURIComponent(searchVal)}`);
    return venues.json();
}

const exportObj = {
    getAll,
    getUrl,
    getTimeslots,
    searchVenue,
};

export default exportObj;