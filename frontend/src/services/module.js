let baseUrl = "";
let searchUrl = "";

if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
    baseUrl = "http://localhost:8000/module/";
    searchUrl = "http://localhost:8000/moduleSearch/";
} else {
    baseUrl = "/module/";
    searchUrl = "/moduleSearch/";
}

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