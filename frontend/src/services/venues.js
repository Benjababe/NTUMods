import constants from "./constants";

const venueUrl = `${constants.baseUrl}/venue/`;
const timeslotUrl = `${constants.baseUrl}/timeslot/`;
const searchUrl = `${constants.baseUrl}/venuesearch/`;

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

const venueSearch = async (name, day = "", timeStart = "", timeEnd = "", lat = null, lng = null) => {
    const coordParams = (lat !== null && lng !== null) ? `&lat=${lat}&lng=${lng}` : ""
    const venues = await fetch(`${searchUrl}?name=${name}&day=${day}&start=${timeStart}&end=${timeEnd}${coordParams}`);
    return venues.json();
}

const exportObj = {
    getAll,
    getUrl,
    getTimeslots,
    venueSearch,
};

export default exportObj;