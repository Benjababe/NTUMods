const venueUrl = "/venue/";
const timeslotUrl = "/timeslot/";
const searchUrl = "/venuesearch/"

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