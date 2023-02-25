const baseUrl = "http://localhost:8000/module/"

const getAll = async () => {
    const modules = await fetch(baseUrl);
    return modules.json();
}

const getUrl = async (url) => {
    const modules = await fetch(url);
    return modules.json();
}

const searchModule = async (searchVal) => {
    const modules = await fetch(`${baseUrl}search/${searchVal}`);
    return modules.json();
}

const exportObj = {
    getAll,
    getUrl
};

export default exportObj;