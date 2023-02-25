const baseUrl = "http://localhost:8000/module/"
const searchUrl = "http://localhost:8000/modulesearch/"

const getAll = async () => {
    const modules = await fetch(baseUrl);
    return modules.json();
}

const getUrl = async (url) => {
    const modules = await fetch(url);
    return modules.json();
}

const searchModule = async (searchVal) => {
    const modules = await fetch(`${searchUrl}?query=${encodeURIComponent(searchVal)}`);
    return modules.json();
}

const exportObj = {
    getAll,
    getUrl,
    searchModule
};

export default exportObj;