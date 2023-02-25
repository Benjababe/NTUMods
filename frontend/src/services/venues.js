const venueUrl = "http://localhost:8000/venue/";
const timeslotUrl = "http://localhost:8000/timeslot/"

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

const exportObj = {
    getAll,
    getUrl,
    getTimeslots,
};

export default exportObj;