const baseUrl = "http://localhost:8000/venue/"

const getAll = async () => {
    const venues = await fetch(baseUrl);
    return venues.json();
}

const getUrl = async (url) => {
    const venues = await fetch(url);
    return venues.json();
}

const exportObj = {
    getAll,
    getUrl
};

export default exportObj;